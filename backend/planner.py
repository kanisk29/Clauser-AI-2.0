import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def fallback_plan(
    contract_type,
    industry,
    persona,
    custom_knowledge
):

    return {
        "contract_type": contract_type,
        "main_intent": "Analyze contract risks",
        "required_agents": [
            "risk_agent",
            "judge_agent"
        ],
        "retrieval_required": bool(custom_knowledge),
        "retrieval_topics": [
            "liability",
            "termination",
            "confidentiality"
        ],
        "reasoning": "Fallback plan generated"
    }


def create_plan(
    contract_text,
    contract_type,
    industry,
    persona,
    custom_knowledge=None
):

    system_prompt = f"""
You are an expert legal workflow planner.

Your job is to decide how a multi-agent legal system should analyze a contract.

Return ONLY valid JSON.

Required keys:

contract_type
main_intent
required_agents
retrieval_required
retrieval_topics
reasoning

Rules:

required_agents must be chosen from:

[
"risk_agent",
"compliance_agent",
"retrieval_agent",
"judge_agent"
]

retrieval_required must be true or false.

retrieval_topics must be a list.

Do not return markdown.
Do not return explanations outside JSON.

Context:

Contract Type: {contract_type}
Industry: {industry}
Persona: {persona}
Knowledge Base Available:
{"Yes" if custom_knowledge else "No"}
"""

    user_prompt = f"""
Contract:

{contract_text[:12000]}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        content = response.choices[0].message.content

        content = re.sub(
            r"```json",
            "",
            content
        )

        content = re.sub(
            r"```",
            "",
            content
        )

        content = content.strip()

        plan = json.loads(content)

        return plan

    except Exception as e:

        print(
            "Planner Error:",
            str(e)
        )

        return fallback_plan(
            contract_type,
            industry,
            persona,
            custom_knowledge
        )