import subprocess, sys, json, os, io
from datetime import datetime
from jinja2 import Template
from agents.requirement_agent import parse_requirement
from agents.test_case_agent import generate_test_cases
from agents.script_agent import generate_script
from bias_monitor import BiasMonitor

# Force UTF-8 for stdout (fix Unicode errors)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://localhost:5001"
REQUIREMENT_TEXT = """
The loan API must allow:
- Fetch a loan by ID (returns 200 with loan data if exists, 404 if not)
- Create a new loan with user_id and amount. Loans with amount <= 10000 are approved, others rejected.
- Return proper HTTP status codes and error messages.
"""

def run_script(script_code: str, test_id: str):
    script_path = f"generated_{test_id}.py"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_code)
    print(f"\n[DEBUG] Script for {test_id}:\n{'='*50}\n{script_code}\n{'='*50}")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=10)
    print(f"[DEBUG] stdout:\n{result.stdout}")
    print(f"[DEBUG] stderr:\n{result.stderr}")
    os.remove(script_path)
    return result.returncode == 0, result.stdout, result.stderr

def main():
    os.makedirs("reports", exist_ok=True)
    print("🤖 3‑Agent QA Orchestrator (Requirement → Test Case → Script)")

    spec = parse_requirement(REQUIREMENT_TEXT)
    print("📋 Spec:", json.dumps(spec, indent=2))

    test_cases = generate_test_cases(spec)
    print(f"🧪 Generated {len(test_cases)} test cases.")

    results = []
    for tc in test_cases:
        print(f"\n--- {tc['id']}: {tc['title']} ---")
        tool = "api"
        print(f"🔧 Tool: {tool}")
        script = generate_script(tc, tool, BASE_URL)
        passed, out, err = run_script(script, tc['id'])
        results.append({
            "id": tc['id'],
            "title": tc['title'],
            "type": tc.get("type", "unknown"),
            "tool": tool,
            "passed": passed,
            "stdout": out,
            "stderr": err
        })
        print("   ✅ PASS" if passed else "   ❌ FAIL")

    print("\n🔍 Running bias compliance...")
    monitor = BiasMonitor()
    bias_ok = bool(monitor.is_compliant())
    #bias_ok = bias_ok_raw

    report = {
        "suite": "Loan API QA",
        "timestamp": datetime.now().isoformat(),
        "total": len(test_cases),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
        "bias_compliant": bias_ok,
        "details": results
    }

    # Helper to convert numpy types for JSON
    def convert_numpy(obj):
        if hasattr(obj, 'tolist'):
            return obj.tolist()
        if hasattr(obj, 'item'):
            return obj.item()
        raise TypeError

    with open("reports/result.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=convert_numpy)
    print("DEBUG report keys:", report.keys())
    # Build HTML using f-strings (no Jinja2)
    html_lines = [
        "<html><body>",
        "<h1>QA Report</h1>",
        f"<p>Passed: {report['passed']}/{report['total']}</p>",
        f"<p>Bias compliant: {report['bias_compliant']}</p>",
        "<ul>"
    ]
    for tc in report['details']:
        status = "PASS" if tc['passed'] else "FAIL"
        html_lines.append(f"<li>{tc['id']}: {tc['title']} - {status}</li>")
    html_lines.append("</ul></body></html>")
    html = "\n".join(html_lines)

    with open("reports/minimal.html", "w") as f:
        f.write("<html><body>Test</body></html>")

    with open("reports/result.html", "w", encoding="utf-8") as f:
        f.write(html)
        f.flush()
        os.fsync(f.fileno())
    print("DEBUG: HTML written, file size:", os.path.getsize("reports/result.html"))
    with open("reports/result.html", "r", encoding="utf-8") as f_check:
        content = f_check.read()
    print(f"DEBUG: File content length = {len(content)}")
    print("DEBUG: First 200 chars of file content:")
    print(content[:200])

    print("\n📊 Reports saved to reports/")
    sys.exit(0 if (bias_ok and report["failed"] == 0) else 1)



if __name__ == "__main__":
    main()