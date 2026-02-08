from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import io

# Import parser
from .parser.policy_parser import parse_policy

app = FastAPI(title="Policy Gap Analyzer API")

# Configure CORS
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

# ---------------------------------------------------------
# Control Loader Logic (Consolidated)
# ---------------------------------------------------------

def load_controls() -> List[Dict]:
    """
    Returns a list of NIST 800-53 controls.
    """
    return [
        {
            "id": "AC-1",
            "name": "Access Control Policy and Procedures",
            "function": "Protect",
            "intent": "Ensure formal policies exist to manage access to systems.",
            "status": "Not Started"
        },
        {
            "id": "AC-2",
            "name": "Account Management",
            "function": "Protect",
            "intent": "Manage system accounts, including creation, activation, modification, disabling, and removal.",
            "status": "Not Started"
        },
        {
            "id": "AU-2",
            "name": "Audit Events",
            "function": "Detect",
            "intent": "Determine that the information system is capable of auditing defined events.",
            "status": "Not Started"
        },
        {
            "id": "IR-4",
            "name": "Incident Handling",
            "function": "Respond",
            "intent": "Implement an incident handling capability for security incidents.",
            "status": "Not Started"
        },
        {
            "id": "CP-9",
            "name": "System Backup",
            "function": "Recover",
            "intent": "Conduct backups of user-level information and system-level information.",
            "status": "Not Started"
        },
        {
            "id": "RA-3",
            "name": "Risk Assessment",
            "function": "Identify",
            "intent": "Conduct an assessment of risk, including the likelihood and magnitude of harm.",
            "status": "Not Started"
        }
    ]

def get_control_by_id(control_id: str) -> Dict:
    controls = load_controls()
    for c in controls:
        if c["id"] == control_id:
            return c
    return None

# ---------------------------------------------------------
# Gap Analysis Logic (Consolidated)
# ---------------------------------------------------------

def analyze_gap(policy_text: str) -> List[Dict]:
    """
    Analyzes the policy text against loaded controls.
    Refined keyword matching logic.
    """
    controls = load_controls()
    results = []
    
    policy_text_lower = policy_text.lower()
    
    for control in controls:
        status = "Non-Compliant"
        missing = "Policy does not address this control."
        risk = f"Without {control['name']}, the organization is at risk of unauthorized access or data loss."
        rewrite = f"The organization shall implement {control['name']} to ensure {control['intent']}."
        
        # Enhanced Mock Logic with more keywords
        if control["id"] == "AC-1":
            if "access control policy" in policy_text_lower or "access management policy" in policy_text_lower:
                status = "Compliant"
                missing = "None"
            elif "access" in policy_text_lower:
                status = "Partial"
                missing = "Mentioned but lacks formal policy structure."
                
        elif control["id"] == "AC-2":
            if "account management" in policy_text_lower and "provisioning" in policy_text_lower:
                status = "Compliant"
                missing = "None"
            elif "account" in policy_text_lower:
                 status = "Partial"
                 missing = "Lacks specific de-provisioning procedures."
                 
        elif control["id"] == "AU-2":
             if "audit" in policy_text_lower and "logs" in policy_text_lower:
                 status = "Compliant"
                 missing = "None"
        
        elif control["id"] == "IR-4":
            if "incident response" in policy_text_lower and "handling" in policy_text_lower:
                status = "Compliant"
                missing = "None"
                
        elif control["id"] == "CP-9":
            if "backup" in policy_text_lower and "restoration" in policy_text_lower:
                status = "Compliant"
                missing = "None"
            elif "backup" in policy_text_lower:
                status = "Partial"
                missing = "Lacks restoration testing requirements."
                
        elif control["id"] == "RA-3":
            if "risk assessment" in policy_text_lower:
                status = "Compliant"
                missing = "None"
        
        results.append({
            "id": control["id"],
            "name": control["name"],
            "function": control["function"],
            "status": status,
            "missing_elements": missing,
            "risk_explanation": risk,
            "suggested_rewrite": rewrite,
            "nist_mapping": f"NIST 800-53 {control['id']}"
        })
        
    return results

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Policy Gap Analyzer API is running."}

@app.get("/controls")
def get_controls():
    """Returns all NIST controls."""
    return load_controls()

@app.get("/controls/{control_id}")
def get_control_detail(control_id: str):
    """Returns details for a specific control."""
    control = get_control_by_id(control_id)
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    return control

@app.post("/analyze")
async def analyze_policy_endpoint(file: UploadFile = File(...)):
    """
    Accepts a policy file, parses it, and returns gap analysis results.
    """
    try:
        # 1. Parse policy text
        policy_text = await parse_policy(file)
        
        # 2. Run gap analysis
        analysis_results = analyze_gap(policy_text)
        
        return {
            "filename": file.filename,
            "results": analysis_results
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/roadmap")
def get_roadmap():
    """
    Returns a mock roadmap based on NIST functions.
    """
    return [
        {"function": "Identify", "status": "In Progress", "completion": 40, "next_step": "Complete Asset Inventory"},
        {"function": "Protect", "status": "Not Started", "completion": 0, "next_step": "Implement MFA"},
        {"function": "Detect", "status": "In Progress", "completion": 20, "next_step": "Deploy SIEM"},
        {"function": "Respond", "status": "Planned", "completion": 0, "next_step": "Draft IR Plan"},
        {"function": "Recover", "status": "Planned", "completion": 0, "next_step": "Test Backups"},
    ]
