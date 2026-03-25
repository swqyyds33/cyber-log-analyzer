from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict


def export_json(report: Dict[str, Any], output_path: str) -> None:
    path = Path(output_path)
    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)


def export_csv(report: Dict[str, Any], output_path: str) -> None:
    path = Path(output_path)
    fieldnames = [
        "timestamp",
        "level",
        "source",
        "risk_level",
        "score",
        "categories",
        "keywords",
        "raw",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for event in report.get("events", []):
            row = {
                "timestamp": event.get("timestamp"),
                "level": event.get("level"),
                "source": event.get("source"),
                "risk_level": event.get("risk_level"),
                "score": event.get("score"),
                "categories": ", ".join(event.get("categories", [])),
                "keywords": ", ".join(event.get("keywords", [])),
                "raw": event.get("raw"),
            }
            writer.writerow(row)


def export_report(report: Dict[str, Any], output_path: str, fmt: str) -> None:
    fmt = fmt.lower()
    if fmt == "json":
        export_json(report, output_path)
    elif fmt == "csv":
        export_csv(report, output_path)
    else:
        raise ValueError(f"Unsupported export format: {fmt}")
