from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def open_chrome_headless_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    # userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    # options.add_argument(f'user-agent={userAgent}')
    # prefs = {"profile.default_content_setting_values.notifications" : 2}
    # options.add_experimental_option("prefs",prefs)
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--head")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    return driver