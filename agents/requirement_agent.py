from langchain_ollama import OllamaLLM
import json

def parse_requirement(text: str) -> dict:
    llm = OllamaLLM(model="llama3.2:1b", temperature=0)
    prompt = f"""
    Convert this requirement into a JSON object with keys: feature, endpoints, expected_behaviors, negative_cases.
    Requirement: {text}
    """
    response = llm.invoke(prompt)
    try:
        return json.loads(response)
    except:
        # fallback
        return {
            "feature": "Loan API",
            "endpoints": ["GET /loans/{id}", "POST /loans"],
            "expected_behaviors": ["200 for existing loan", "404 for missing"],
            "negative_cases": ["missing user_id", "amount negative"]
        }