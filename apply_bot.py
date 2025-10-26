import time
import logging
import json
import tempfile
import shutil
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
        email_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="email"]'))
        )
        email_field.send_keys(credentials['email'])
        logging.info("Email address entered.")

        print("Please enter your password in the browser window and press Enter to continue...")
        WebDriverWait(browser, timeout=300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-automation-id='My_Account_portlet']"))
        )
        logging.info("Login successful.")
        return True
    except TimeoutException:
        logging.error("Login failed. The script timed out waiting for the password or the next page.")
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
        browser.find_element(By.XPATH, '//input[contains(@id,"preferredName")]').send_keys(profile["preferred_name"])
        browser.find_element(By.XPATH, '//input[contains(@id,"address")]').send_keys(profile["address"])
        browser.find_element(By.XPATH, '//input[contains(@id,"email")]').send_keys(profile["email"])
        browser.find_element(By.XPATH, '//input[contains(@id,"phone")]').send_keys(profile["phone"])
        browser.find_element(By.XPATH, '//input[contains(@id,"howDidYouHear")]').send_keys(profile["how_heard"])
        browser.find_element(By.XPATH, '//input[contains(@id,"prevWellsFargoEmployee")]').send_keys(profile["prev_wf_employee"])
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error filling out personal information: {e}")
        return False

    # --- Step 2: My Experience ---
    try:
        for i, exp in enumerate(work_experience):
            if i > 0:
                add_experience_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Add Work Experience"]'))
                )
                add_experience_button.click()
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'(//input[contains(@id,"jobTitle")])[{i+1}]'))
                )

            browser.find_element(By.XPATH, f'(//input[contains(@id,"jobTitle")])[{i+1}]').send_keys(exp["job_title"])
            browser.find_element(By.XPATH, f'(//input[contains(@id,"company")])[{i+1}]').send_keys(exp["company"])
            browser.find_element(By.XPATH, f'(//input[contains(@id,"location")])[{i+1}]').send_keys(exp["location"])
            browser.find_element(By.XPATH, f'(//input[contains(@id,"fromDate")])[{i+1}]').send_keys(exp["from"])
            browser.find_element(By.XPATH, f'(//input[contains(@id,"toDate")])[{i+1}]').send_keys(exp["to"])
            browser.find_element(By.XPATH, f'(//textarea[contains(@id,"roleDescription")])[{i+1}]').send_keys(exp["description"])
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error filling out work experience: {e}")
        return False

    # --- Step 3: Education ---
    try:
        for i, edu in enumerate(education):
            if i > 0:
                add_education_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Add Education"]'))
                )
                add_education_button.click()
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'(//input[contains(@id,"school")])[{i+1}]'))
                )
            browser.find_element(By.XPATH, f'(//input[contains(@id,"school")])[{i+1}]').send_keys(edu["school"])
            browser.find_element(By.XPATH, f'(//input[contains(@id,"degree")])[{i+1}]').send_keys(edu["degree"])
            browser.find_element(By.XPATH, f'(//input[contains(@id,"fieldOfStudy")])[{i+1}]').send_keys(edu["field"])
            browser.find_element(By.XPATH, f'(//input[contains(@id,"gpa")])[{i+1}]').send_keys(edu["gpa"])
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error filling out education: {e}")
        return False

    # --- Step 4: Languages ---
    try:
        for lang in languages:
            browser.find_element(By.XPATH, '//input[contains(@id,"language")]').send_keys(lang["language"])
            browser.find_element(By.XPATH, '//input[contains(@id,"languageFluency")]').send_keys(lang["fluency"])
            browser.find_element(By.XPATH, '//input[contains(@id,"languageReading")]').send_keys(lang["reading"])
            browser.find_element(By.XPATH, '//input[contains(@id,"languageSpeaking")]').send_keys(lang["speaking"])
            browser.find_element(By.XPATH, '//input[contains(@id,"languageWriting")]').send_keys(lang["writing"])
    except NoSuchElementException as e:
        logging.error(f"Error filling out languages: {e}")
        return False

    # --- Step 5: Resume/CV upload ---
    try:
        file_input_elem = browser.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input_elem.send_keys(resume_path)
    except NoSuchElementException as e:
        logging.error(f"Error uploading resume: {e}")
        return False

    # --- Step 6: Application Questions ---
    for question, answer in app_questions.items():
        try:
            radio_xpath = f'//input[@type="radio" and @value="{answer}"]'
            browser.find_element(By.XPATH, radio_xpath).click()
        except NoSuchElementException as e:
            logging.error(f"Error answering application question '{question}': {e}")
            return False

    # --- Step 7: Voluntary Disclosures ---
    try:
        browser.find_element(By.XPATH, '//select[contains(@id,"citizenship")]').send_keys(vol_dis["citizenship_status"])
        browser.find_element(By.XPATH, '//input[contains(@id,"nationality")]').send_keys(vol_dis["nationality"])
        browser.find_element(By.XPATH, '//select[contains(@id,"gender")]').send_keys(vol_dis["gender"])
    except NoSuchElementException as e:
        logging.error(f"Error filling out voluntary disclosures: {e}")
        return False

    # --- Step 8: Terms and Final Submit ---
    try:
        browser.find_element(By.XPATH, '//input[@type="checkbox"]').click()
        browser.find_element(By.XPATH, '//button[contains(text(),"Submit")]').click()
        logging.info(f"Application submitted successfully for {browser.current_url}")
        return True
    except NoSuchElementException as e:
        logging.error(f"Error submitting application for {browser.current_url}: {e}")
        return False

def main():
    """Main function to run the application bot."""
    config = load_config()
    chromedriver_path = config['paths']['chromedriver']

    user_data_dir = None
    try:
        browser, user_data_dir = start_browser(chromedriver_path)

        if not config['job_urls']:
            logging.error("No job URLs found in the configuration file.")
            return

        # Login is handled once at the beginning
        browser.get(config['job_urls'][0])
        apply_button = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-automation-id='applyButton']"))
        )
        apply_button.click()

        if not handle_login(browser, config['credentials']):
            return

        # Apply to the first job
        if not apply_to_job(browser, config):
            logging.error(f"Failed to apply to the first job: {config['job_urls'][0]}")

        # Apply to the rest of the jobs
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
