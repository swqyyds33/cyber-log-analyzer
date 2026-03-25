from __future__ import annotations

import re
from typing import Dict, List

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>[A-Z]+)\s+"
    r"(?P<source>[\w\-.]+)\s+"
    r"(?P<message>.*)$"
)


def parse_log_line(line: str) -> Dict[str, str]:
    """Parse a single log line into a normalized dict."""
    clean_line = line.strip()
    match = LOG_PATTERN.match(clean_line)
    if match:
        return {
            "timestamp": match.group("timestamp"),
            "level": match.group("level"),
            "source": match.group("source"),
            "message": match.group("message"),
            "raw": clean_line,
        }

    return {
        "timestamp": "UNKNOWN",
        "level": "UNKNOWN",
        "source": "UNKNOWN",
        "message": clean_line,
        "raw": clean_line,
    }


def read_logs(file_path: str) -> List[Dict[str, str]]:
    """Read and parse all non-empty lines from a log file."""
    records: List[Dict[str, str]] = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(parse_log_line(line))
    return records
