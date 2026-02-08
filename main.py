import asyncio
import os
import sys
from typing import List, Dict

# Import components (Do NOT modify these imports)
from src.parser.policy_parser import parse_policy
from src.compliance.control_loader import load_controls
from src.compliance.gap_engine import evaluate_control
from src.llm.llm_engine import Phi3PolicyDraftingEngine


class MockUploadFile:
    """
    Simulates FastAPI UploadFile behavior for local file reading.
    """
    def __init__(self, filepath: str):
        self.filename = os.path.basename(filepath)
        self.filepath = filepath
        self.file = open(self.filepath, "rb")

    async def read(self) -> bytes:
        self.file.seek(0)
        return self.file.read()

    def close(self):
        self.file.close()


async def main():
    try:
        # 1. Load Policy Document
        policy_path = "data/sample_policies/weak_policy.txt"
        if not os.path.exists(policy_path):
            print(f"Error: Policy file not found at {policy_path}")
            sys.exit(1)

        print(f"Loading policy from: {policy_path}")
        
        # Create mock file object
        policy_file = MockUploadFile(policy_path)
        
        try:
            # 2. Parse Policy
            print("Parsing policy...")
            policy_text = await parse_policy(policy_file)
            
            if not policy_text or policy_text.startswith("Error"):
                print(f"Policy parsing failed: {policy_text}")
                sys.exit(1)
                
        finally:
            policy_file.close()

        # 3. Load NIST Controls
        print("Loading NIST controls...")
        try:
            controls = load_controls()
        except ImportError:
            # Fallback if control_loader is empty/broken (for user context)
            print("Error: Could not load controls from src.compliance.control_loader")
            sys.exit(1)

        if not controls:
            print("No controls loaded.")
            sys.exit(1)

        # 4. Run Gap Detection
        print("Running gap analysis...")
        gaps = []
        
        # Prepare policy clauses (gap_engine expects clauses list, joins them internally)
        # We pass the full text as a single clause since parsing is handled
        # policy_text is a single strong string
        
        for control in controls:
            # evaluate_control(control: Dict, clauses: List[str]) -> Dict
            result = evaluate_control(control, [policy_text])
            
            if result["status"] != "ADEQUATE":
                gaps.append(result)

        print(f"Found {len(gaps)} gaps to address.\n")

        # 5. Generate LLM Responses
        if gaps:
            print("Initializing LLM Engine (Phi-3)...")
            try:
                llm = Phi3PolicyDraftingEngine()
            except Exception as e:
                print(f"Failed to initialize LLM engine: {e}")
                sys.exit(1)

            print("Generating remediation plans...\n")
            print("=" * 60)

            for gap in gaps:
                print(f"CONTROL: {gap['control_name']} ({gap['control_id']})")
                print(f"STATUS: {gap['status']}")
                print(f"SEVERITY: {gap['severity']}")
                print("-" * 60)

                # Explain Risk
                try:
                    explanation = llm.explain_gap(gap)
                    print("RISK EXPLANATION:")
                    print(explanation)
                    print()
                except Exception as e:
                    print(f"Error generating explanation: {e}")

                # Rewrite Policy
                try:
                    policy_clause = llm.rewrite_policy(gap)
                    print("PROPOSED POLICY:")
                    print(policy_clause)
                    print()
                except Exception as e:
                    print(f"Error drafting policy: {e}")

                # Roadmap
                try:
                    roadmap = llm.generate_roadmap(gap)
                    print("IMPROVEMENT ROADMAP:")
                    print(roadmap)
                except Exception as e:
                    print(f"Error generating roadmap: {e}")

                print("=" * 60)
                print()

    except Exception as e:
        print(f"Critical System Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
