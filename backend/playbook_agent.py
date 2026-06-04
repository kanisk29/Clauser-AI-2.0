import os
import json
import re

from dotenv import load_dotenv
from groq import Groq

from retrieval import vecdb

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def playbook_node(state):

    if not state["custom_knowledge"]:

        return {
            "playbook_conflicts": []
        }

    docs = vecdb.similarity_search(
        query=f"""
        {state["contract_type"]}
        {state["industry"]}
        {state["persona"]}
        """,
        k=5
    )

    retrieved_text = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = f"""
You are a Playbook Validation Agent.

Compare the contract against company policy.

Identify:

1. Policy conflicts
2. Missing protections
3. Liability violations
4. Payment term conflicts
5. Confidentiality conflicts

Return ONLY JSON.

Format:

[
 {{
   "policy":"Liability Cap",
   "contract_clause":"Unlimited liability",
   "severity":"High",
   "recommendation":"Cap liability to 12 months fees"
 }}
]
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
PLAYBOOK:

{retrieved_text}

CONTRACT:

{state["contract_text"][:12000]}
"""
            }
        ]
    )

    content = response.choices[0].message.content

    content = re.sub(r"```json", "", content)
    content = re.sub(r"```", "", content)

    try:
        conflicts = json.loads(content)
    except:
        conflicts = []

    return {
        "playbook_conflicts": conflicts
    }