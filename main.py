from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, InvalidArgumentException, WebDriverException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
import db_functions

def configure_webdriver(user_settings):
    """
    Configures a Selenium webdriver with the provided user settings.

    Args:
        user_settings (UserSettings): A UserSettings object containing the desired configuration for the webdriver.

    Returns:
        chrome_options (Options): A Selenium Options object configured with the desired settings.
    """
    # Create an instance of the Chrome Options class and set the desired settings
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_settings.user_agent}')
    # Handle decoding error if proxy is provided
    if user_settings.proxy:
        try:
            proxy = user_settings.proxy
            chrome_options.add_argument(f'--proxy-server={proxy}')
        except UnicodeDecodeError:
            print('Error: Invalid byte sequence in proxy.')
    if user_settings.webgl_enabled:
        chrome_options.add_argument('--enable-webgl')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return chrome_options


# тут должны быть функции авторизации в линке
def initialize_webdriver(options, max_attempts=10):
    attempts = 0
    timer = 5
    while attempts < max_attempts:
        refresh_flag = True
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get("https://www.linkedin.com/")
            wait = WebDriverWait(driver, timer)
            wait.until(EC.presence_of_element_located((By.ID, "session_key")))
            return driver
        except (WebDriverException, TimeoutException):
            # if refresh_flag:
            #     driver.refresh()
            #     refresh_flag = False
            #     timer = 10
            #     wait = WebDriverWait(driver, timer)
            #     wait.until(EC.presence_of_element_located((By.ID, "session_key")))
            #     return driver
            # else:
            attempts += 1
            driver.quit()
    raise Exception("Failed to initialize webdriver after multiple attempts.")


def login_to_linkedin(driver, username, password, retries=5):
    timeout = 15
    #чекаем а тали страница
    print(username, "Это кто входит")
    if "linkedin.com/authwall" in driver.current_url:
        sign_in = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".authwall-join-form__form-toggle--bottom.form-toggle")))
        sign_in.click()
    for _ in range(retries):
        try:
            username_field = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "session_key")))
            username_field.send_keys(username)
            password_field = driver.find_element(By.ID, "session_password")
            password_field.send_keys(password)
            login_button = driver.find_element(By.CSS_SELECTOR, "[data-id='sign-in-form__submit-btn']")
            login_button.click()
            time.sleep(7)
            break
        except TimeoutException as e:
            if _ == retries - 1:
                raise e
            else:
                print(f"Timeout exception encountered. Retrying {_ + 1} of {retries}...")
                driver.close()
        except ElementNotInteractableException as e:
            print(e)
            return False

flag = True
while flag:
    bot_id = input("Введи номер бота: ")
    user_settings = db_functions.UserSettings.get_user_settings(bot_id)
    options = configure_webdriver(user_settings)
    driver = initialize_webdriver(options)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "title")))
    login = login_to_linkedin(driver, user_settings.login, user_settings.password)
    commands = True
    while commands:
        input_command = input("Введите команду: exit чтобы выйти из бота off чтобы закончить программу: ")
        if input_command == "exit":
            driver.close()
            commands = False
        elif input_command == "off":
            commands = False
            flag = False
        else:
            print("Не верная команда")
