import os, time, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

EMAIL    = os.environ["NAUKRI_EMAIL"]
PASSWORD = os.environ["NAUKRI_PASSWORD"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait   = WebDriverWait(driver, 20)

try:
    driver.get("https://www.naukri.com/nlogin/login")
    wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
    driver.find_element(By.ID, "usernameField").send_keys(EMAIL)
    driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

    driver.get("https://www.naukri.com/mnjuser/profile")
    headline = wait.until(EC.presence_of_element_located((By.ID, "resumeHeadline")))
    text     = headline.get_attribute("value") or ""
    new_text = text.strip() if text.endswith(" ") else text + " "
    headline.clear()
    headline.send_keys(new_text)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Save')]"))).click()
    logging.info("✅ Profile refreshed.")

finally:
    driver.quit()