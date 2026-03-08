import os, time, logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL    = os.environ["NAUKRI_EMAIL"]
PASSWORD = os.environ["NAUKRI_PASSWORD"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
# NOTE: undetected_chromedriver handles headless differently
options.add_argument("--headless=new")

driver = uc.Chrome(options=options)
wait   = WebDriverWait(driver, 30)

try:
    logging.info("Navigating to Naukri login...")
    driver.get("https://www.naukri.com/nlogin/login")
    
    # Extra wait for JS-heavy page to load
    time.sleep(4)

    wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
    driver.find_element(By.ID, "usernameField").send_keys(EMAIL)
    time.sleep(1)
    driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    time.sleep(6)
    logging.info("Login submitted, navigating to profile...")

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
    # Save screenshot for debugging
    try:
        driver.save_screenshot("debug_screenshot.png")
        logging.info("Screenshot saved as debug_screenshot.png")
    except:
        pass
    raise

finally:
    driver.quit()