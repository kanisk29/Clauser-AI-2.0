import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def executive_summary_node(state):

    prompt = f"""
You are a Senior Legal Review Agent.

Create a concise executive summary.

Include:

1. Contract purpose
2. Main obligations
3. Top 3 risks
4. Overall recommendation

Return plain text only.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content":
                f"""
CONTRACT:

{state["contract_text"][:12000]}

RISKS:

{state["risks"]}

COMPLIANCE:

{state["compliance"]}

PLAYBOOK CONFLICTS:

{state["playbook_conflicts"]}
"""
            }
        ]
    )

    summary = response.choices[0].message.content

    return {
        "executive_summary": summary
    }