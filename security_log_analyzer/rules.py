from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_RULES_PATH = Path(__file__).resolve().parent.parent / "config" / "default_keywords.json"


def load_rules(path: str | None = None) -> Dict[str, Dict[str, Any]]:
    """Load keyword-based risk rules from a JSON file."""
    rules_path = Path(path) if path else DEFAULT_RULES_PATH
    if not rules_path.exists():
        raise FileNotFoundError(f"Rules file not found: {rules_path}")

    with rules_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Rules file must contain a JSON object.")

    for category, rule in data.items():
        if not isinstance(rule, dict):
            raise ValueError(f"Rule for category '{category}' must be an object.")
        if "keywords" not in rule or "weight" not in rule:
            raise ValueError(f"Rule for category '{category}' must contain 'keywords' and 'weight'.")
        if not isinstance(rule["keywords"], list):
            raise ValueError(f"Keywords for category '{category}' must be a list.")

    return data
