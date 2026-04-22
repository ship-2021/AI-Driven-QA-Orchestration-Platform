```python
import requests
from playwright.sync_api import sync_playwright

def test_get_non_existent_loan():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Send GET request to non-existent loan endpoint
        response = requests.get('http://localhost:5001/loans/999')

        # Check if the response status code is 404 (Not Found)
        assert response.status_code == 404

        # Close the browser and context
        page.close()
        browser.close(context)
```