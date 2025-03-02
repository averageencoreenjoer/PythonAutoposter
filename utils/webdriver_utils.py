from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(options=None):
    if options is None:
        options = webdriver.ChromeOptions()
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)