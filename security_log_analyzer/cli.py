from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analyzer import LogAnalyzer
from .exporter import export_report
from .parser import read_logs
from .rules import load_rules


def infer_format(output: str | None, explicit_format: str | None) -> str:
    if explicit_format:
        return explicit_format.lower()
    if output:
        suffix = Path(output).suffix.lower().lstrip(".")
        if suffix in {"json", "csv"}:
            return suffix
    return "json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cyber Log Analyzer CLI")
    parser.add_argument("--input", required=True, help="Path to the input log file")
    parser.add_argument("--rules", help="Path to custom keyword rules in JSON format")
    parser.add_argument("--output", default="analysis_report.json", help="Path to the exported report")
    parser.add_argument("--format", choices=["json", "csv"], help="Export format, inferred from output suffix if omitted")
    parser.add_argument("--print", action="store_true", dest="print_report", help="Print report summary to console")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        records = read_logs(args.input)
        rules = load_rules(args.rules)
        analyzer = LogAnalyzer(rules)
        report = analyzer.analyze(records)
        export_format = infer_format(args.output, args.format)
        export_report(report, args.output, export_format)

        if args.print_report:
            print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        else:
            print(f"Analysis completed. Report exported to: {args.output}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
