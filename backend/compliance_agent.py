import os
import json
import re

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def compliance_node(state):

    prompt = f"""
You are an Indian Legal Compliance Agent.

Analyze the contract for:

1. DPDP Act 2023 compliance
2. IT Act 2000 compliance
3. Employment law concerns
4. Data privacy concerns
5. Notice period issues
6. Non-compete issues

Return ONLY JSON array.

Format:

[
    {{
        "law":"DPDP Act 2023",
        "issue":"Missing consent clause",
        "severity":"High"
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
                "content": state["contract_text"][:15000]
            }
        ]
    )

    content = response.choices[0].message.content

    content = re.sub(r"```json", "", content)
    content = re.sub(r"```", "", content)

    try:
        compliance = json.loads(content)
    except:
        compliance = []

    return {
        "compliance": compliance
    }