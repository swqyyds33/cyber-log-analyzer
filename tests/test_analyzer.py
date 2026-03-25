import unittest

from security_log_analyzer.analyzer import LogAnalyzer
from security_log_analyzer.parser import parse_log_line
from security_log_analyzer.rules import load_rules


class TestCyberLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.rules = load_rules()
        self.analyzer = LogAnalyzer(self.rules)

    def test_parse_log_line(self):
        line = "2026-03-20 10:16:05 WARN auth-service Failed login for admin from 10.10.1.8"
        parsed = parse_log_line(line)
        self.assertEqual(parsed["level"], "WARN")
        self.assertEqual(parsed["source"], "auth-service")
        self.assertIn("Failed login", parsed["message"])

    def test_detect_matches(self):
        record = parse_log_line(
            "2026-03-20 10:17:42 WARN web-gateway SQL injection attempt detected from 10.0.0.8"
        )
        result = self.analyzer.detect_matches(record)
        self.assertTrue(result["matched"])
        self.assertIn("injection", result["categories"])
        self.assertGreaterEqual(result["score"], 5)

    def test_analyze_summary(self):
        records = [
            parse_log_line("2026-03-20 10:16:05 WARN auth-service Failed login for admin from 10.10.1.8"),
            parse_log_line("2026-03-20 10:22:55 INFO dns-resolver Normal DNS query from 192.168.1.25"),
        ]
        report = self.analyzer.analyze(records)
        self.assertEqual(report["summary"]["total_logs"], 2)
        self.assertEqual(report["summary"]["matched_events"], 1)


if __name__ == "__main__":
    unittest.main()
