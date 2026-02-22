import threading
from selenium import webdriver
from main import run_scraper
from config import BROWSERSTACK_URL



# URL = "https://elpais.com/opinion/"

def run_test(os_name, os_version, browser_name=None, browser_version=None, device_name=None):
    bstack_options = {
        "os": os_name,
        "osVersion": os_version,
        "sessionName": f"{os_name} Test",
    }

    session_prefix = bstack_options["sessionName"].replace(" ", "_")
    options = webdriver.ChromeOptions()

    if device_name:
        # Mobile device
        options.set_capability("browserName", "Chrome")
        bstack_options["deviceName"] = device_name
        bstack_options["realMobile"] = "true"
    else:
        # Desktop browser
        options.set_capability("browserName", browser_name)
        options.set_capability("browserVersion", browser_version)

    options.set_capability("bstack:options", bstack_options)

    # driver = webdriver.Remote(
    #     command_executor=f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
    #     options=options
    # )

    driver = webdriver.Remote(
    command_executor=BROWSERSTACK_URL,
    options=options
    )

    try:
        # driver.get(URL)
        # print(f"{bstack_options['sessionName']} → {driver.title}")
        run_scraper(driver, session_prefix)
    finally:
        driver.quit()


threads = []

configs = [
    ("Windows", "11", "Chrome", "latest", None),
    ("Windows", "10", "Firefox", "latest", None),
    ("OS X", "Ventura", "Safari", "latest", None),
    ("iOS", "16", None, None, "iPhone 14"),
    ("Android", "13.0", None, None, "Samsung Galaxy S23"),
]

for config in configs:
    t = threading.Thread(target=run_test, args=config)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All 5 parallel tests completed.")