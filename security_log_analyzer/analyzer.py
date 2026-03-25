from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

SEVERITY_BONUS = {
    "INFO": 0,
    "WARN": 1,
    "WARNING": 1,
    "ERROR": 2,
    "CRITICAL": 3,
    "UNKNOWN": 0,
}


def classify_risk(score: int) -> str:
    if score >= 8:
        return "high"
    if score >= 4:
        return "medium"
    return "low"


class LogAnalyzer:
    def __init__(self, rules: Dict[str, Dict[str, Any]]) -> None:
        self.rules = rules

    def detect_matches(self, record: Dict[str, str]) -> Dict[str, Any]:
        text = f"{record.get('source', '')} {record.get('message', '')}".lower()
        matched_categories: List[str] = []
        matched_keywords: List[str] = []
        score = SEVERITY_BONUS.get(record.get("level", "UNKNOWN").upper(), 0)

        for category, rule in self.rules.items():
            weight = int(rule.get("weight", 1))
            keywords = rule.get("keywords", [])
            category_hit = False
            for keyword in keywords:
                if keyword.lower() in text:
                    matched_keywords.append(keyword)
                    category_hit = True
            if category_hit:
                matched_categories.append(category)
                score += weight

        return {
            **record,
            "score": score,
            "risk_level": classify_risk(score),
            "categories": matched_categories,
            "keywords": matched_keywords,
            "matched": bool(matched_categories),
        }

    def analyze(self, records: List[Dict[str, str]]) -> Dict[str, Any]:
        analyzed_records = [self.detect_matches(record) for record in records]
        matched_events = [record for record in analyzed_records if record["matched"]]

        category_counter = Counter()
        risk_counter = Counter()
        level_counter = Counter()

        for event in matched_events:
            category_counter.update(event["categories"])
            risk_counter.update([event["risk_level"]])
            level_counter.update([event["level"]])

        return {
            "summary": {
                "total_logs": len(records),
                "matched_events": len(matched_events),
                "unmatched_logs": len(records) - len(matched_events),
                "category_statistics": dict(category_counter),
                "risk_distribution": dict(risk_counter),
                "log_level_distribution": dict(level_counter),
            },
            "events": matched_events,
        }
