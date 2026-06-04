from groq import Groq
import os
from retrieval import analyze_contract_risk
from dotenv import load_dotenv
from langsmith import Client,traceable
from langsmith.evaluation import evaluate

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def complete_eval(user_text,ops):
    prompt = f"""You are an expert Contract Risk Analyzer Judge. 
    Task:
    Check if the "Outputs" correctly identify risks present in the "Text".
    Rules:
    - Return 1 ONLY if outputs are factually correct and relevant to the text
    - Return 0 if incorrect, missing key risks, or hallucinated
    - Output must be exactly one character: 0 or 1
    Text: {user_text}
    Outputs to be checked: {ops}
    Return: <Value should be 0 or 1 ONLY NOTHING ELSE>"""
    
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages= [{"role":"system","content":"You are an expert Contract Risk Analyzer Judge",},{"role":"user","content":prompt}]
    ).choices[0].message.content

    if response == "1":
        return True
    elif response == "0":
        return False
    else:
        return False



    