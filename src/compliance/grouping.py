from collections import defaultdict
from typing import List, Dict

def group_by_function(results: List[Dict]) -> Dict[str, List[Dict]]:
    grouped = defaultdict(list)

    for result in results:
        grouped[result["nist_function"]].append(result)

    return dict(grouped)
