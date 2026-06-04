import os
import json
import re

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def negotiation_node(state):

    prompt = f"""
You are an expert contract negotiation agent.

Given identified risks,
suggest safer contract language.

Return ONLY JSON.

Format:

[
    {{
        "clause":"Unlimited Liability",
        "proposed_clause":"Liability shall not exceed fees paid during previous 12 months."
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
                "content": json.dumps(
                    state["risks"],
                    indent=2
                )
            }
        ]
    )

    content = response.choices[0].message.content

    content = re.sub(r"```json", "", content)
    content = re.sub(r"```", "", content)

    try:
        negotiations = json.loads(content)
    except:
        negotiations = []

    return {
        "negotiations": negotiations
    }