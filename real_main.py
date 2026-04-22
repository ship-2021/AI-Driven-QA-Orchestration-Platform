# real_main.py
import subprocess
import sys
import json
import os
from datetime import datetime
from jinja2 import Template

# Import your existing modules
from agents.requirement_agent import parse_requirements
from agents.test_case_agent import generate_test_cases
from agents.script_agent import generate_script, save_script
from mcp_selector import choose_ui_tool   # reuse the MCP selector (will be adapted)
from bias_monitor import BiasMonitor

# -------------------------------
# CONFIGURATION – CHANGE THESE TO TEST ANY REAL SITE
# -------------------------------
TARGET_UI_URL = "https://www.saucedemo.com/"
TARGET_API_URL = "https://jsonplaceholder.typicode.com"

# Example requirement (you can modify this)
REQUIREMENT = f"""
Test the following real systems:

1. UI: {TARGET_UI_URL}
   - Login with valid credentials (username: standard_user, password: secret_sauce) should succeed and show inventory page.
   - Login with invalid credentials (e.g., wrong password) should show an error message.

2. API: {TARGET_API_URL}
   - GET /posts/1 should return status 200 and a JSON object with id=1.
   - POST /posts with title, body, userId should return status 201 and contain the created id.
"""

# -------------------------------
# Helper: Execute a generated script
# -------------------------------
def execute_script(script_path: str):
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

# -------------------------------
# Helper: Decide tool (UI vs API) – you can enhance with MCP
# -------------------------------
def decide_tool(test_case_title: str, test_case_type: str) -> str:
    if "login" in test_case_title.lower() or "ui" in test_case_type.lower():
        return choose_ui_tool(test_case_title)   # returns playwright/selenium/mock
    else:
        return "api"   # for API tests

# -------------------------------
# Main orchestrator
# -------------------------------
def main():
    print("🤖 Real QA Orchestrator (with real websites)")
    print("=" * 60)

    # Step 1: Parse requirement into spec
    print("\n📝 Requirement:\n", REQUIREMENT)
    spec = parse_requirements(REQUIREMENT)
    print("\n📋 Structured Spec:\n", json.dumps(spec, indent=2))

    # Step 2: Generate test cases
    test_cases = generate_test_cases(spec)
    print(f"\n🧪 Generated {len(test_cases)} test cases.")

    # Prepare results list
    results = []
    os.makedirs("../AI-Driven-QA-Orchestration-Platform/generated_tests", exist_ok=True)

    # Step 3: For each test case, generate and execute script
    for tc in test_cases:
        print(f"\n--- Executing {tc['id']}: {tc['title']} ---")
        tool = decide_tool(tc['title'], tc.get('type', 'api'))
        print(f"🔧 Tool selected: {tool}")

        # Generate script code
        code = generate_script(tc, tool, base_url=TARGET_API_URL, ui_url=TARGET_UI_URL)
        script_path = f"../AI-Driven-QA-Orchestration-Platform/generated_tests/{tc['id']}.py"
        save_script(tc['id'], code)

        # Execute the script
        passed, stdout, stderr = execute_script(script_path)
        results.append({
            "id": tc['id'],
            "title": tc['title'],
            "type": tc.get('type', 'unknown'),
            "tool": tool,
            "passed": passed,
            "stdout": stdout,
            "stderr": stderr
        })
        print(f"   {'✅ PASS' if passed else '❌ FAIL'}")

    # Step 4: Bias compliance gate (uses existing dataset)
    print("\n🔍 Running AI Bias Compliance Gate...")
    monitor = BiasMonitor()
    bias_compliant = monitor.is_compliant()

    # Step 5: Build final report dictionary
    report = {
        "test_suite": "Real Website QA",
        "timestamp": datetime.now().isoformat(),
        "target_ui": TARGET_UI_URL,
        "target_api": TARGET_API_URL,
        "total_tests": len(test_cases),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
        "bias_compliant": bias_compliant,
        "details": results
    }

    # Save JSON report
    with open("reports/real_report.json", "w") as f:
        json.dump(report, f, indent=2)

    # Generate and save HTML report
    html_template = """
    <!DOCTYPE html>
    <html>
    <head><title>QA Real Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .pass { color: green; }
        .fail { color: red; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
    </head>
    <body>
        <h1>Real Website Test Execution Report</h1>
        <p><strong>Suite:</strong> {{ report.test_suite }}</p>
        <p><strong>Timestamp:</strong> {{ report.timestamp }}</p>
        <p><strong>UI Target:</strong> {{ report.target_ui }}</p>
        <p><strong>API Target:</strong> {{ report.target_api }}</p>
        <p><strong>Passed:</strong> {{ report.passed }} / {{ report.total_tests }}</p>
        <p><strong>Bias Compliant:</strong> {{ report.bias_compliant }}</p>
        <h2>Test Case Details</h2>
        <table>
            <tr><th>ID</th><th>Title</th><th>Type</th><th>Tool</th><th>Status</th><th>Output</th></tr>
            {% for tc in report.details %}
            <tr>
                <td>{{ tc.id }}</td>
                <td>{{ tc.title }}</td>
                <td>{{ tc.type }}</td>
                <td>{{ tc.tool }}</td>
                <td class="{{ 'pass' if tc.passed else 'fail' }}">{{ "PASS" if tc.passed else "FAIL" }}</td>
                <td><pre>{{ tc.stdout[:200] }}{{ '...' if tc.stdout|length > 200 else '' }}</pre></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    template = Template(html_template)
    html_content = template.render(report=report)
    with open("reports/real_report.html", "w") as f:
        f.write(html_content)

    print("\n📊 Reports saved to reports/real_report.json and reports/real_report.html")

    # Final exit code: fail if any test failed OR bias non-compliant
    if not bias_compliant or report["failed"] > 0:
        print("\n❌ Pipeline failed due to test failures or bias non-compliance.")
        sys.exit(1)
    else:
        print("\n🎉 All tests passed and bias compliant!")

if __name__ == "__main__":
    os.makedirs("reports", exist_ok=True)
    main()