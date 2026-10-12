import json
from typing import Dict, Any

class ReportGenerator:
    def __init__(self, scan_results: Dict[str, Any], report_type: str = "json"):
        self.results = scan_results
        self.report_type = report_type

    def generate(self) -> str:
        if self.report_type == "json":
            return json.dumps(self.results, indent=4)
        elif self.report_type == "html":
            return self._generate_html()
        return json.dumps(self.results)

    def _generate_html(self) -> str:
        target = self.results.get("target", "Unknown")
        status = self.results.get("status", "completed")
        findings = self.results.get("findings", [])
        
        findings_html = ""
        for f in findings:
            severity = f.get("severity", "Low")
            color = "text-yellow-400" if severity == "Medium" else "text-red-400" if severity == "High" else "text-blue-400"
            findings_html += f"""
            <div style="background: #18181b; border: 1px solid #27272a; padding: 15px; margin-bottom: 10px; border-radius: 8px;">
                <h4 style="margin: 0 0 5px 0; color: #fff;">{f.get('type')}</h4>
                <p style="margin: 0 0 5px 0; font-size: 14px;" class="{color}">Severity: {severity}</p>
                <p style="margin: 0; color: #a1a1aa; font-size: 14px;">{f.get('message')}</p>
            </div>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Shardex WebGuard AI Report - {target}</title>
    <style>
        body {{ background-color: #09090b; color: #f4f4f5; font-family: sans-serif; padding: 40px; }}
        .container {{ max-width: 800px; margin: auto; background: #121214; border: 1px solid #27272a; padding: 30px; border-radius: 12px; }}
        h1 {{ color: #c084fc; font-size: 24px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Shardex WebGuard AI Report</h1>
        <p><strong>Target URL:</strong> {target}</p>
        <p><strong>Status:</strong> {status}</p>
        <hr style="border: 0; border-top: 1px solid #27272a; margin: 20px 0;">
        <h3>Findings ({len(findings)})</h3>
        {findings_html if findings_html else '<p style="color: #a1a1aa;">No issues found.</p>'}
    </div>
</body>
</html>
"""
