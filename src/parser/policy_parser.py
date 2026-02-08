from pathlib import Path
from typing import List

def parse_policy(file_path: Path) -> List[str]:
    file_path = Path(file_path).resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"Policy file not found: {file_path}")

    text = file_path.read_text(encoding="utf-8")

    # Split into meaningful clauses
    clauses = [
        line.strip().lower()
        for line in text.splitlines()
        if len(line.strip()) > 20
    ]

    return clauses
