from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_page_source(url):
    chrome_options = Options()
    prefs = {
        "profile.managed_default_content_settings.images": 2,
    }
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path="driver\\chromedriver.exe", chrome_options=chrome_options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return page_source
