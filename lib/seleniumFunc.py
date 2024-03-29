from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.common.by import By
from proxy_ext import proxies
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from webdriver_manager.chrome import ChromeDriverManager

def openChrome(userLogin, passwordLogin, proxy, headless=None, cookie_result=None):
    options = webdriver.ChromeOptions()
    # chrome_service = ChromeService(ChromeDriverManager().install())
    # chrome_service.creationflags = CREATE_NO_WINDOW
    prefs = {"credentials_enable_service": False,
            "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)

    if proxy != "None":

    
        proxies_extension = proxies(proxy)
        options.add_extension(proxies_extension)

    # if headless is None:

    #     options.add_argument("--headless=new")

    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-blink-features")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # driver = webdriver.Chrome(options=options, service=chrome_service)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    sleep(3)
    driver.implicitly_wait(10)
    driver.get("https://designhub.miricanvas.com/login")

    email = driver.find_element(By.XPATH, "//input[@placeholder='Email']")

    for i in userLogin:

        email.send_keys(i)
        sleep(random.uniform(0.1, 0.3))
    sleep(1)
    passw = driver.find_element(By.XPATH, "//input[@placeholder='Password']")

    for i in passwordLogin:

        passw.send_keys(i)
        sleep(random.uniform(0.1, 0.3))
    sleep(1)
    driver.find_element(By.XPATH, "//button[text()='Log In']").click()
    if headless is not None:
        sleep(5)
        cookie = getCookies(driver)
        cookie_result.put(cookie)
    return driver

def getCookies(driver):
    cookie_string = ""

    for cookie in driver.get_cookies():

        name = cookie['name']
        value = cookie['value']
        cookie_string  += f"{name}={value}; "

    return cookie_string


def UploadtoMiris(driver, path):
    try:

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Select File or Folder']")))
        sleep(2)
        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(path)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']")))
        sleep(2)

        return True
    
    except:

        return False
