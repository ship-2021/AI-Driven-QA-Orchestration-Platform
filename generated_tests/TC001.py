```python
import requests
from playwright.sync_api import sync_playwright

def test_get_existing_loan():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the base URL
        page.goto('http://localhost:5001')

        # Click on the GET /loans/1 link
        page.click('#get-loan-link')

        # Wait for the response
        page.wait_for_selector('#response', timeout=10)

        # Get the expected output
        output = page.get_text('#expected-output')

        # Close the browser context and page
        browser.close()
        context.close()
        page.close()

        # Check if the expected output matches the actual output
        assert output == '200, loan data'
```