# AI-Driven QA Orchestration Platform

[![Pipeline Status](https://gitlab.com/your-username/qa-orchestrator/badges/main/pipeline.svg)](https://gitlab.com/your-username/qa-orchestrator/-/pipelines)

 – Demonstrates automated test strategy, AI‑powered test generation, financial compliance (bias gate), and CI/CD integration.

## 📌 Overview

This platform orchestrates a complete QA pipeline:

1. **Requirement Agent** (Ollama + LangChain) – parses natural language requirements into structured test specifications.
2. **Test Case Agent** (Ollama) – generates positive, negative, and edge test cases.
3. **Script Generation Agent** (Ollama) – writes executable Python code (API or UI) using `requests` or `playwright`.
4. **Execution Engine** – runs scripts against a real financial API (loan approval system).
5. **Bias Compliance Gate** (Fairlearn) – enforces demographic parity (fair lending metric).
6. **Reporting** – produces JSON and HTML reports.
7. **CI/CD** – GitLab/GitHub Actions pipeline that runs the bias check on every merge request.

The architecture is modular, extensible, and ready for **UI testing** (Playwright/Selenium) via the MCP tool selector.

## 🏗 Architecture

```mermaid
graph TD
    A[Natural Language Requirement] --> B[Requirement Agent]
    B --> C[Test Case Agent]
    C --> D[Script Generation Agent]
    D --> E[Execution Engine]
    E --> F[Loan API (Flask SUT)]
    F --> G[Bias Compliance Gate]
    G --> H[HTML/JSON Report]
    H --> I[CI/CD Fail if bias > threshold]

    🚀 Quick Start
    Prerequisites
    Python 3.11+

    Ollama installed and running

    Pull the model: ollama pull llama3.2:1b

    Installation
    bash
    git clone https://gitlab.com/your-username/qa-orchestrator.git
    cd qa-orchestrator
    python -m venv venv
    source venv/bin/activate   # or .\venv\Scripts\activate on Windows
    pip install -r requirements.txt
    playwright install chromium   # for UI tests (optional)

    Run the System Under Test (SUT)
    bash
    python real_sut.py
    # Starts a loan API on http://localhost:5001

    python main.py

    Output:

    Test cases generated and executed

    Bias compliance score

    Reports saved in reports/result.json and reports/result.html

    View Reports
    Open reports/result.html in a browser.

    aunch Dashboard (Streamlit)
    bash
    streamlit run dashboard.py
    
    Project Structure
    text
    qa-orchestrator/
    ├── .gitlab-ci.yml                # CI/CD pipeline
    ├── requirements.txt              # Dependencies
    ├── real_sut.py                   # Flask loan API (System Under Test)
    ├── main.py                       # Main orchestrator
    ├── dashboard.py                  # Streamlit dashboard
    ├── bias_monitor.py               # Fairness compliance gate
    ├── mcp_selector.py               # LLM-based tool selection (Playwright/Selenium/API)
    ├── agents/
    │   ├── requirement_agent.py      # Parses requirements into spec
    │   ├── test_case_agent.py        # Generates test cases
    │   └── script_agent.py           # Writes executable scripts
    ├── reports/                      # Generated reports (ignored by git)
    └── README.md
    🧪 
    Example
    Requirement input (hardcoded in main.py):
    
    text
    The loan API must allow:
    - Fetch a loan by ID (returns 200 with loan data if exists, 404 if not)
    - Create a new loan with user_id and amount. Loans with amount <= 10000 are approved, others rejected.
    - Return proper HTTP status codes and error messages.
    Generated test cases (example):
    
    json
    [
      {"id": "TC001", "title": "Get existing loan", "type": "positive"},
      {"id": "TC002", "title": "Get non-existent loan", "type": "negative"}
    ]
    Generated script (for TC001):
    
    python
    import requests
    def run_test():
        response = requests.get('http://localhost:5001/loans/1')
        if response.status_code == 200:
            print("PASS")
            exit(0)
        else:
            print("FAIL")
            exit(1)
    if __name__ == "__main__":
        run_test()
    Execution result:
    
    text
    --- TC001: Get existing loan ---
       ✅ PASS
    --- TC002: Get non‑existent loan ---
       ✅ PASS
    🔍 Running bias compliance...
    📊 Demographic parity difference: 0.1908
    ✅ Compliant? True
    🔒 Financial Compliance Gate
    The bias_monitor.py uses demographic parity difference from fairlearn, a metric required by fair lending regulations (ECOA). It:
    
    Loads the UCI Adult Income dataset (public, simulates loan applications).
    
    Trains a simple Random Forest model.
    
    Compares approval rates between male and female groups.
    
    Fails the pipeline if the difference exceeds 0.8 (configurable).
    
    In a real financial system, you would replace the dataset with your own and adjust the threshold.
    
    🧠 MCP Tool Selector
    The mcp_selector.py lets the LLM decide which automation tool to use based on the test description:
    
    playwright – modern web UI (JavaScript heavy)
    
    selenium – legacy web apps
    
    api – backend API tests
    
    To enable it, replace tool = "api" in main.py with:
    
    python
    from mcp_selector import choose_ui_tool
    tool = choose_ui_tool(tc['title'])
    
    🔁 CI/CD Pipeline (GitLab / GitHub)
    
   
   
    GitHub Actions (.github/workflows/qa.yml)
    yaml
    name: QA Pipeline
    on: [push, pull_request]
    jobs:
      bias:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with: { python-version: '3.11' }
          - run: pip install -r requirements.txt
          - run: python bias_monitor.py
      full:
        runs-on: ubuntu-latest
        needs: bias
        steps:
          - uses: actions/checkout@v4
          - run: pip install -r requirements.txt
          - run: python main.py
   
   
    🐳Docker (Optional)
    bash
    docker build -t qa-orchestrator .
    docker run -p 8501:8501 qa-orchestrator
    Or with docker-compose:
    
    bash
    docker-compose up --build
    📈 Extensibility for UI Testing
    The script generation agent supports playwright and selenium out of the box. To test a real UI:
    
    Set tool = "playwright" in main.py (or use MCP selector).
    
    Update the prompt in agents/script_agent.py to include the target URL.
    
    The LLM will generate a Playwright script that you can execute.
    
      
    
    
    🙏 Acknowledgements
    Ollama for local LLMs
    
    LangChain for agent framework
    
    Fairlearn for fairness metrics
    
    Flask for the SUT
    
    
   
  
