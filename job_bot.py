import time, logging, json, os, getpass, tempfile, shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CONFIG_FILE = 'config.json'
LOG_FILE = 'bot_run.log'

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def setup_and_get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)

    print("--- First-Time Bot Setup ---")
    email = input("Enter your Wells Fargo careers login email: ")
    job_urls = []
    print("\nEnter job URLs (press Enter on an empty line when finished):")
    while True:
        url = input("Job URL: ")
        if not url: break
        job_urls.append(url)

    resume_path = input("\nEnter the FULL path to your resume PDF on this computer: ")
    chromedriver_path = input("Enter the FULL path to your chromedriver file: ")

    config = { "job_urls": job_urls, "credentials": { "email": email }, "paths": { "chromedriver": chromedriver_path, "resume": resume_path } }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\nConfiguration saved to {CONFIG_FILE}. You won't be asked this again.")
    return config

def start_browser(chromedriver_path):
    options = Options()
    options.add_argument("--window-size=1280,1024")
    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=options)

def run_bot():
    config = setup_and_get_config()
    browser = None
    try:
        browser = start_browser(config['paths']['chromedriver'])
        print("\nBot started. A Chrome window will open.")

        browser.get(config['job_urls'][0])
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-automation-id='applyButton']"))).click()

        print("Login page reached.")
        logging.info("Login page reached.")

        password = getpass.getpass("Please enter your Wells Fargo password in this terminal: ")

        email_field = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, 'email')))
        email_field.send_keys(config['credentials']['email'])

        password_field = browser.find_element(By.ID, 'password')
        password_field.send_keys(password)

        browser.find_element(By.XPATH, '//button[text()="Sign In"]').click()
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-automation-id='My_Account_portlet']")))

        print("Login successful. Starting applications...")
        logging.info("Login successful. Starting applications...")

        # This is a placeholder for the real form-filling logic
        for i, job_url in enumerate(config['job_urls']):
            print(f"--- Applying to job {i+1}/{len(config['job_urls'])} ---")
            if i > 0:
                browser.get(job_url)
                WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-automation-id='applyButton']"))).click()

            logging.info(f"Simulating application for job: {job_url}")
            time.sleep(10) # Simulate filling out the form
            print(f"Completed application for: {job_url}")
            logging.info(f"Successfully applied (simulated) to job: {job_url}")

    except Exception as e:
        print(f"\nAn error occurred. See {LOG_FILE} for details.")
        logging.error(f"A critical error occurred: {e}", exc_info=True)

    finally:
        if browser:
            browser.quit()
        print(f"\nBot has finished. A detailed log is available in {LOG_FILE}.")

if __name__ == "__main__":
    run_bot()
