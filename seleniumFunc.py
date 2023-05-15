from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.common.by import By


def openChrome(userLogin, passwordLogin, proxy):
    options = webdriver.ChromeOptions()
    prefs = {"credentials_enable_service": False,
            "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)
    if proxy != "None":
        options.add_argument("--proxy-server=" + proxy)
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-blink-features")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
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

    return driver

def getCookies(driver):
    cookie_string = ""
    for cookie in driver.get_cookies():
        name = cookie['name']
        value = cookie['value']
        cookie_string  += f"{name}={value}; "