from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

# Parser
from src.parser.policy_parser import parse_policy
#llm
from src.llm.llm_runner import run_llm_on_gaps


# Compliance engine (YOUR WORK)
from src.compliance.gap_engine import evaluate_control
from src.compliance.grouping import group_by_function
from src.compliance.scoring import compute_compliance_score

app = FastAPI(title="Policy Gap Analyzer API")

# -------------------------
# CORS
# -------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Load Controls (NIST CSF)
# -------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
CONTROLS_PATH = ROOT_DIR / "data" / "controls" / "nist_controls.json"


def load_controls():
    with open(CONTROLS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------
# Compliance Runner
# -------------------------
def run_compliance(policy_text: str):
    """
    Runs deterministic compliance analysis.
    """
    clauses = policy_text.lower().split(".")
    controls = load_controls()

    results = []
    for control in controls:
        results.append(evaluate_control(control, clauses))

    return {
        "grouped_results": group_by_function(results),
        "summary": compute_compliance_score(results),
        "raw_results": results,
    }


# -------------------------
# Endpoints
# -------------------------
@app.get("/")
def root():
    return {"message": "Policy Gap Analyzer API is running."}


@app.post("/analyze")
async def analyze_policy(file: UploadFile = File(...)):
    """
    Upload a policy file and receive compliance gap analysis.
    """
    try:
        policy_text = await parse_policy(file)
        compliance_output = run_compliance(policy_text)

        return {
            "filename": file.filename,
            "compliance": compliance_output,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
