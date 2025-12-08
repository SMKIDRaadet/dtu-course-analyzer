import os
import sys
from playwright.sync_api import sync_playwright

# 1. Get credentials from GitHub Secrets
USERNAME = os.environ.get("DTU_USERNAME")
PASSWORD = os.environ.get("DTU_PASSWORD")

if not USERNAME or not PASSWORD:
    print("Error: DTU_USERNAME and DTU_PASSWORD environment variables must be set.")
    sys.exit(1)

url = "https://kurser.dtu.dk"

with sync_playwright() as p:
    print("Launching browser...")
    # Headless=True for CI/CD
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # 2. Go to Kurser.dtu.dk and wait for network to be idle (handles redirects)
        print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle", timeout=60000)

        # 3. Handle Login
        print("Waiting for login form...")
        
        # Robust selector: tries name="username", id="username", or type="email"
        # Increased timeout to 30 seconds to allow for slow redirects
        username_selector = 'input[name="username"], input[id="username"], input[name="UserName"], input[type="email"]'
        
        page.wait_for_selector(username_selector, state="visible", timeout=30000)
        
        # Fill credentials
        print("Filling credentials...")
        page.locator(username_selector).first.fill(USERNAME)
        page.fill('input[name="password"], input[id="password"], input[type="password"]', PASSWORD)
        
        # Click login (looks for common submit buttons)
        print("Clicking login...")
        page.click('button[type="submit"], input[type="submit"], button:has-text("Login"), button:has-text("Log på")')
        
        # 4. Wait for redirect back to kurser.dtu.dk
        print("Waiting for valid session cookie...")
        # We wait until we are back on the course site
        page.wait_for_url("https://kurser.dtu.dk/**", timeout=60000)
        
        # 5. Extract Cookie
        cookies = context.cookies()
        session_cookie = next((c for c in cookies if c["name"] == "ASP.NET_SessionId"), None)

        if session_cookie:
            print("Session cookie found!")
            with open("secret.txt", "w") as f:
                f.write(session_cookie["value"])
            print("Successfully wrote secret.txt")
        else:
            print("Error: ASP.NET_SessionId cookie not found after login.")
            # Debug: print all cookies found to see what went wrong
            print("Cookies found:", [c["name"] for c in cookies])
            sys.exit(1)

    except Exception as e:
        print(f"Login failed: {e}")
        # Capture screenshot for debugging in GitHub Artifacts
        page.screenshot(path="login_error.png")
        print("Screenshot saved to login_error.png")
        sys.exit(1)

    finally:
        browser.close()