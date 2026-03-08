import os, time, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL    = os.environ["NAUKRI_EMAIL"]
PASSWORD = os.environ["NAUKRI_PASSWORD"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

options = Options()
options.binary_location = "/usr/local/bin/chrome"   # pinned Chrome binary
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Point directly to pinned chromedriver — no webdriver_manager needed
service = Service(executable_path="/usr/local/bin/chromedriver")
driver  = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
wait = WebDriverWait(driver, 30)

try:
    logging.info("Navigating to Naukri login...")
    driver.get("https://www.naukri.com/nlogin/login")
    time.sleep(4)

    wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
    driver.find_element(By.ID, "usernameField").send_keys(EMAIL)
    time.sleep(1)
    driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(6)

    logging.info("Navigating to profile page...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(4)

    headline = wait.until(EC.presence_of_element_located((By.ID, "resumeHeadline")))
    text     = headline.get_attribute("value") or ""
    new_text = text.strip() if text.endswith(" ") else text + " "
    headline.clear()
    time.sleep(1)
    headline.send_keys(new_text)
    time.sleep(1)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Save')]"))).click()
    time.sleep(3)
    logging.info("✅ Profile refreshed successfully.")

except Exception as e:
    logging.error(f"❌ Failed: {e}")
    try:
        driver.save_screenshot("debug_screenshot.png")
        logging.info("Screenshot saved.")
    except:
        pass
    raise

finally:
    driver.quit()