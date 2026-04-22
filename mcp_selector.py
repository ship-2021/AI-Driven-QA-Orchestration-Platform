# mcp_selector.py
from langchain_ollama import OllamaLLM

def choose_ui_tool(test_description: str) -> str:
    llm = OllamaLLM(model="llama3.2:1b", temperature=0)
    prompt = f"""You are an automation architect. Based on the test description, choose the best tool: playwright, selenium, or mock.
Test: "{test_description}"
Output only the tool name (playwright/selenium/mock)."""
    response = llm.invoke(prompt).strip().lower()
    if response in ["playwright", "selenium", "mock"]:
        return response
    return "playwright"  # default

if __name__ == "__main__":
    desc = input("Describe the UI test: ")
    print(f"LLM recommends: {choose_ui_tool(desc)}")