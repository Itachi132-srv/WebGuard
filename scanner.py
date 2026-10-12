import requests
from typing import Dict, Any

def run_security_scan(target_url: str) -> Dict[str, Any]:
    findings = []
    try:
        response = requests.get(target_url, timeout=5, allow_redirects=True)
        headers = response.headers
        
        if "Content-Security-Policy" not in headers:
            findings.append({
                "type": "Missing Security Header",
                "severity": "Medium",
                "header": "Content-Security-Policy",
                "message": "CSP header is missing, leaving the app vulnerable to XSS injections."
            })
            
        if "X-Frame-Options" not in headers:
            findings.append({
                "type": "Missing Security Header",
                "severity": "Low",
                "header": "X-Frame-Options",
                "message": "X-Frame-Options header not set, potential clickjacking risk."
            })
            
        if "Strict-Transport-Security" not in headers and target_url.startswith("https"):
            findings.append({
                "type": "Transport Security",
                "severity": "Medium",
                "header": "Strict-Transport-Security",
                "message": "HSTS header missing on secure transport connection."
            })
            
        return {
            "target": target_url,
            "status_code": response.status_code,
            "findings_count": len(findings),
            "findings": findings,
            "summary": "Security scan completed successfully."
        }
    except Exception as e:
        return {
            "target": target_url,
            "status": "error",
            "message": str(e),
            "findings": []
        }
