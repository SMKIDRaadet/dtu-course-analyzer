import os
import sys
from playwright.sync_api import sync_playwright

# 1. Get credentials from GitHub Secrets (Environment Variables)
USERNAME = os.environ.get("DTU_USERNAME")
PASSWORD = os.environ.get("DTU_PASSWORD")

if not USERNAME or not PASSWORD:
    print("Error: DTU_USERNAME and DTU_PASSWORD environment variables must be set.")
    sys.exit(1)

url = "https://kurser.dtu.dk"

with sync_playwright() as p:
    print("Launching browser...")
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # 2. Go to Kurser.dtu.dk (This will redirect to the CAS login page)
    print(f"Navigating to {url}...")
    page.goto(url)

    # 3. Handle Login
    # Wait for the login form. Selectors based on standard DTU CAS login.
    # Note: These selectors might need adjustment if DTU changes their login page.
    try:
        print("Logging in...")
        # Most CAS systems use 'username' and 'password' as name attributes
        page.wait_for_selector('input[name="username"]', timeout=10000)
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        
        # Click the login button (looking for type="submit" or button tag)
        page.click('button[type="submit"], input[type="submit"]')
        
        # 4. Wait for redirect back to kurser.dtu.dk
        print("Waiting for redirect...")
        page.wait_for_url("https://kurser.dtu.dk/*", timeout=30000)
        
        # 5. Extract Cookie
        cookies = context.cookies()
        session_cookie = next((c for c in cookies if c["name"] == "ASP.NET_SessionId"), None)

        if session_cookie:
            print("Session cookie found!")
            # Write to secret.txt as scraper.py expects
            with open("secret.txt", "w") as f:
                f.write(session_cookie["value"])
            print("Successfully wrote secret.txt")
        else:
            print("Error: ASP.NET_SessionId cookie not found after login.")
            sys.exit(1)

    except Exception as e:
        print(f"Login failed: {e}")
        # Take a screenshot for debugging if running in CI
        page.screenshot(path="login_error.png")
        sys.exit(1)

    browser.close()