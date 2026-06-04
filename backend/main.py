from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from graph import graph
from ingestion import extract_text_from_file, file_indexer

app = FastAPI(title="Clauser AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {
        "status": "running",
        "project": "Clauser AI"
    }


@app.post("/analyze")
async def analyze(
    contract_type: str = Form(...),
    industry: str = Form(...),
    persona: str = Form(...),
    contract_file: UploadFile = File(...),
    playbook_file: UploadFile = File(None)
):

    contract_temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(contract_file.filename)[1]
    )

    contract_temp.write(await contract_file.read())
    contract_temp.close()

    custom_knowledge = None

    if playbook_file:

        playbook_temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(playbook_file.filename)[1]
        )

        playbook_temp.write(await playbook_file.read())
        playbook_temp.close()

        file_indexer(
            playbook_temp.name,
            playbook_file.filename
        )

        custom_knowledge = "available"

    text = extract_text_from_file(
        contract_temp.name
    )

    result = graph.invoke(
        {
            "contract_text": text,
            "contract_type": contract_type,
            "industry": industry,
            "persona": persona,
            "custom_knowledge": custom_knowledge
        }
    )

    try:
        os.remove(contract_temp.name)
    except:
        pass

    return result["final_output"]