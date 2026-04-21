from langchain_ollama import OllamaLLM
import json

def generate_test_cases(spec: dict) -> list:
    llm = OllamaLLM(model="llama3.2:1b", temperature=0.3)
    prompt = f"""
    From this spec: {json.dumps(spec)}
    Generate 3-5 test cases. Each test case must have: id, title, type (positive/negative/boundary), preconditions, steps, expected_result.
    Output as a JSON array.
    """
    response = llm.invoke(prompt)
    try:
        return json.loads(response)
    except:
        return [
            {"id": "TC001", "title": "Get existing loan", "type": "positive", "steps": ["GET /loans/1"], "expected": "200 OK, loan data"},
            {"id": "TC002", "title": "Get non‑existent loan", "type": "negative", "steps": ["GET /loans/999"], "expected": "404 Not found"},
        ]