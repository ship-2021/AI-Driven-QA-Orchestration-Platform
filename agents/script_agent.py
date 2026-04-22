# agents/script_agent.py
from langchain_ollama import OllamaLLM
import re

def clean_llm_code(raw_code: str) -> str:
    """Extract clean Python code from LLM output."""
    # Remove any leading/trailing whitespace
    raw_code = raw_code.strip()
    # Remove markdown code blocks (```python ... ``` or ``` ... ```)
    # Pattern: ```(python)?\n(.*?)\n```
    pattern = r'```(?:python)?\s*\n(.*?)\n```'
    match = re.search(pattern, raw_code, re.DOTALL)
    if match:
        raw_code = match.group(1).strip()
    else:
        # If no code block, remove any stray backticks and the word "python"
        raw_code = re.sub(r'^```python\s*', '', raw_code)
        raw_code = re.sub(r'\s*```$', '', raw_code)
        raw_code = raw_code.replace('```', '').replace('python', '')
    # Remove any lines that are not valid Python (e.g., "Here is the code:")
    lines = raw_code.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip lines that are obvious explanations (heuristic)
        if stripped.startswith('Here') or stripped.startswith('The code') or stripped == '':
            continue
        cleaned_lines.append(line)
    raw_code = '\n'.join(cleaned_lines).strip()
    # Ensure the script has a main guard
    if "if __name__ == '__main__':" not in raw_code:
        raw_code += "\n\nif __name__ == '__main__':\n    run_test()"
    return raw_code

def generate_script(test_case: dict, tool: str, base_url: str) -> str:
    llm = OllamaLLM(model="llama3.2:1b", temperature=0)  # faster than llama3.2
    if tool == "api":
        prompt = f"""
Write Python code using the 'requests' library to test this API test case.
Base URL: {base_url}
Test case: {test_case}
Requirements:
- Define a function `run_test()`.
- Print "PASS" and exit(0) if the test passes.
- Print "FAIL" and exit(1) if it fails.
- Do NOT include any markdown formatting, explanations, or backticks.
- Output ONLY the raw Python code.
"""
    else:
        prompt = f"Write Python code using playwright for {test_case}. No markdown."

    raw_output = llm.invoke(prompt)
    clean_code = clean_llm_code(raw_output)
    return clean_code