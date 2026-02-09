import streamlit as st
import tempfile

# Parser
from src.parser.policy_parser import _clean_text

# Compliance
from src.compliance.gap_engine import evaluate_control
from src.compliance.grouping import group_by_function
from src.compliance.scoring import compute_compliance_score

# LLM
from src.llm.llm_runner import run_llm_on_gaps

import json
from pathlib import Path

# -------------------------
# Load Controls
# -------------------------
ROOT_DIR = Path(__file__).resolve().parent
CONTROLS_PATH = ROOT_DIR / "data" / "controls" / "nist_controls.json"

with open(CONTROLS_PATH, "r", encoding="utf-8") as f:
    CONTROLS = json.load(f)

# -------------------------
# UI
# -------------------------
st.set_page_config(page_title="Policy Gap Analyzer", layout="wide")

st.title("📜 Policy Gap Analyzer")
st.subheader("AI-powered compliance gap analysis & policy improvement")

uploaded_file = st.file_uploader(
    "Upload your policy document (TXT / PDF / DOCX)",
    type=["txt", "pdf", "docx"]
)

analyze = st.button("🔍 Analyze Policy")

if uploaded_file and analyze:
    with st.spinner("Analyzing policy..."):
        # Read file
        raw_text = uploaded_file.read().decode("utf-8", errors="ignore")
        policy_text = _clean_text(raw_text)

        clauses = policy_text.lower().split(".")

        # -------------------------
        # Run Compliance
        # -------------------------
        results = []
        for control in CONTROLS:
            results.append(evaluate_control(control, clauses))

        summary = compute_compliance_score(results)

        st.success("Analysis complete!")

        # -------------------------
        # Compliance Summary
        # -------------------------
        st.header("📊 Compliance Summary")
        st.metric("Compliance %", summary["compliance_percentage"])
        st.metric("Maturity Level", summary["maturity_level"])

        # -------------------------
        # Run LLM
        # -------------------------
        llm_outputs = run_llm_on_gaps(results)

        # -------------------------
        # Display Results
        # -------------------------
        st.header("🚨 Risk Explanations")

        for item in llm_outputs:
            st.subheader(f"{item['control_id']} — {item['control_name']}")
            st.write(item["risk_explanation"])

        st.header("✍️ Rewritten Policy Sections")

        for item in llm_outputs:
            with st.expander(f"{item['control_id']} — Improved Policy"):
                st.text(item["rewritten_policy"])

        st.header("🗺️ Improvement Roadmap")

        for item in llm_outputs:
            st.subheader(f"{item['control_id']} — {item['control_name']}")
            st.text(item["improvement_roadmap"])
