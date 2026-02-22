import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

BROWSERSTACK_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

TARGET_URL = "https://elpais.com/opinion/"