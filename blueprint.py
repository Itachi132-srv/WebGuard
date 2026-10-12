from typing import List, Dict, Any
from playwright.sync_api import sync_playwright

class BlueprintRunner:
    def __init__(self, target_url: str, steps: List[Dict[str, Any]]):
        self.target_url = target_url
        self.steps = steps

    def execute(self) -> Dict[str, Any]:
        results = {
            "target": self.target_url,
            "status": "passed",
            "executed_steps": 0,
            "findings": [],
            "logs": []
        }
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                results["logs"].append(f"Navigating to base URL: {self.target_url}")
                page.goto(self.target_url, timeout=10000)
                results["executed_steps"] += 1

                for idx, step in enumerate(self.steps):
                    action = step.get("action")
                    selector = step.get("selector")
                    value = step.get("value")
                    
                    results["logs"].append(f"Executing step {idx+1}: {action} on {selector or 'page'}")

                    if action == "click":
                        page.click(selector, timeout=5000)
                    elif action == "fill":
                        page.fill(selector, value, timeout=5000)
                    elif action == "assert_text":
                        content = page.text_content(selector)
                        if value not in content:
                            results["findings"].append({
                                "type": "Functional Inconsistency",
                                "severity": "Medium",
                                "message": f"Expected text '{value}' not found in selector '{selector}'. Found: '{content[:50]}...'"
                            })
                            results["status"] = "failed"
                    elif action == "wait":
                        page.wait_for_timeout(int(value))
                        
                    results["executed_steps"] += 1

            except Exception as e:
                results["status"] = "error"
                results["findings"].append({
                    "type": "Execution Error",
                    "severity": "High",
                    "message": f"Blueprint halted due to exception: {str(e)}"
                })
                results["logs"].append(f"Error: {str(e)}")
            finally:
                browser.close()
                
        return results
