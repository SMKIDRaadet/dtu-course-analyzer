import os
import sys
from playwright.sync_api import sync_playwright

# 1. Get credentials from GitHub Secrets
USERNAME = os.environ.get("DTU_USERNAME")
PASSWORD = os.environ.get("DTU_PASSWORD")

if not USERNAME or not PASSWORD:
    print("Error: DTU_USERNAME and DTU_PASSWORD environment variables must be set.")
    sys.exit(1)

# Use forceLogin to help trigger the redirect, but we will also click if needed
url = "https://kurser.dtu.dk/?forceLogin=true"

with sync_playwright() as p:
    print("Launching browser...")
    # Add user_agent to look like a real browser
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    page = context.new_page()

    try:
        print(f"Navigating to {url}...")
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # 2. Trigger Redirect (If not already on the login page)
        # We check if we are already on the ADFS page (sts.ait.dtu.dk)
        if "sts.ait.dtu.dk" not in page.url and "auth.dtu.dk" not in page.url:
            print("Not on login page yet. Searching for 'Log in' button...")
            
            # DTU often has a 'Log på' or 'Log in' link in the header
            login_button = page.locator("a", has_text="Log på").or_(page.locator("a", has_text="Log in"))
            
            if login_button.count() > 0 and login_button.first.is_visible():
                print("Clicking 'Log in' button to trigger redirect...")
                login_button.first.click()
            else:
                print("No login button found. Assuming we might be redirecting automatically...")

        # 3. Handle ADFS Login Form
        print("Waiting for login fields...")
        
        # ADFS usually uses 'userNameInput' or 'UserName'. We allow multiple options.
        # Added '#userNameInput' specifically for the URL you shared.
        username_selector = 'input[id="userNameInput"], input[name="UserName"], input[name="username"], input[type="email"]'
        
        # Wait up to 30s for the redirect to finish and field to appear
        page.wait_for_selector(username_selector, state="visible", timeout=30000)
        
        print(f"Found username field. Logging in as {USERNAME}...")
        page.locator(username_selector).first.fill(USERNAME)
        
        # ADFS password field is often 'passwordInput'
        password_selector = 'input[id="passwordInput"], input[name="Password"], input[name="password"], input[type="password"]'
        page.locator(password_selector).first.fill(PASSWORD)
        
        print("Submitting login form...")
        # ADFS submit button is often 'submitButton'
        submit_selector = 'span[id="submitButton"], button[id="submitButton"], input[type="submit"]'
        
        # Sometimes you have to press Enter, sometimes click. We try clicking first.
        if page.locator(submit_selector).count() > 0:
            page.click(submit_selector)
        else:
            page.keyboard.press("Enter")
        
        # 4. Wait for redirect back to kurser.dtu.dk
        print("Waiting for redirect back to course site...")
        # We wait until the URL contains 'kurser.dtu.dk' and NOT 'sts.ait.dtu.dk'
        page.wait_for_url(lambda u: "kurser.dtu.dk" in u and "sts.ait.dtu.dk" not in u, timeout=60000)
        
        # 5. Extract Cookie
        cookies = context.cookies()
        session_cookie = next((c for c in cookies if c["name"] == "ASP.NET_SessionId"), None)

        if session_cookie:
            print("SUCCESS: Session cookie found!")
            with open("secret.txt", "w") as f:
                f.write(session_cookie["value"])
            print("Cookie saved to secret.txt")
        else:
            print("FAILURE: Login flow finished, but ASP.NET_SessionId cookie was not found.")
            # Debug: print cookies to see if we got something else
            print("Cookies present:", [c["name"] for c in cookies])
            sys.exit(1)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        # Save screenshot for debugging
        page.screenshot(path="login_error.png")
        sys.exit(1)

    finally:
        browser.close()