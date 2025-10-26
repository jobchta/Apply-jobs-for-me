import time
import logging
import json
import tempfile
import shutil
import os
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

logging.basicConfig(level=logging.INFO, filename="wellsfargo_apply_log.txt", filemode="w")

def load_config(filepath='config.json'):
    """Loads the configuration from a JSON file."""
    with open(filepath, 'r') as config_file:
        return json.load(config_file)

def start_browser(chromedriver_path):
    """Starts the Chrome browser with the specified options."""
    user_data_dir = tempfile.mkdtemp()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1920')
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=chrome_options), user_data_dir

def handle_login(browser, credentials):
    """Handles the login process."""
    try:
        password = os.environ.get('WELLS_FARGO_PASSWORD')
        if not password:
            password = getpass.getpass("Wells Fargo Careers password: ")

        email_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="email"]'))
        )
        email_field.send_keys(credentials['email'])

        password_field = browser.find_element(By.XPATH, '//input[@id="password"]')
        password_field.send_keys(password)

        login_button = browser.find_element(By.XPATH, '//button[text()="Sign In"]')
        login_button.click()

        WebDriverWait(browser, timeout=60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-automation-id='My_Account_portlet']"))
        )
        logging.info("Login successful.")
        return True
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Login failed: {e}")
        return False

def apply_to_job(browser, config):
    """Fills out and submits the job application."""
    profile = config['profile']
    work_experience = config['work_experience']
    education = config['education']
    languages = config['languages']
    app_questions = config['app_questions']
    vol_dis = config['vol_dis']
    resume_path = config['paths']['resume']

    # --- Step 1: My Information ---
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[contains(@id,"legalName")]')))
        browser.find_element(By.XPATH, '//input[contains(@id,"legalName")]').send_keys(profile["legal_name"])
        # ... (rest of the form filling logic)
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error filling out personal information: {e}")
        return False

    # ... (rest of the form filling logic for all sections) ...

    try:
        browser.find_element(By.XPATH, '//button[contains(text(),"Submit")]').click()
        logging.info(f"Application submitted successfully for {browser.current_url}")
        return True
    except NoSuchElementException as e:
        logging.error(f"Error submitting application for {browser.current_url}: {e}")
        return False

def main():
    """Main function to run the application bot."""
    if not os.path.exists('config.json'):
        print("Configuration file not found. Please run 'python3 setup.py' first.")
        return

    config = load_config()
    chromedriver_path = config['paths']['chromedriver']

    user_data_dir = None
    try:
        browser, user_data_dir = start_browser(chromedriver_path)

        if not config['job_urls']:
            logging.error("No job URLs found in the configuration file.")
            return

        browser.get(config['job_urls'][0])
        apply_button = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-automation-id='applyButton']"))
        )
        apply_button.click()

        if not handle_login(browser, config['credentials']):
            return

        if not apply_to_job(browser, config):
            logging.error(f"Failed to apply to the first job: {config['job_urls'][0]}")

        for job_url in config['job_urls'][1:]:
            browser.get(job_url)
            apply_button = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-automation-id='applyButton']"))
            )
            apply_button.click()
            if not apply_to_job(browser, config):
                logging.error(f"Failed to apply to job: {job_url}")

    finally:
        if 'browser' in locals() and browser:
            browser.quit()
            logging.info("Browser closed.")
        if user_data_dir:
            shutil.rmtree(user_data_dir)
            logging.info(f"Cleaned up user data directory: {user_data_dir}")

if __name__ == "__main__":
    main()
