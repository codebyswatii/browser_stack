import time
import random
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

if not os.path.exists("article_images"):
    os.makedirs("article_images")

from selenium.webdriver.support.ui import WebDriverWait

def run_scraper(driver,prefix):
    wait = WebDriverWait(driver, 20)

    driver.get("https://elpais.com/opinion/")
    time.sleep(3)

    # Accept cookies if popup appears
    try:
        iframe = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        accept_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar')]"))
        )
        accept_btn.click()

        driver.switch_to.default_content()
    except Exception as e:
        print("Cookie popup handling error:", e)
        driver.switch_to.default_content()

    time.sleep(2)

    # -------------------------
    # Collect First 5 Valid Article Links
    # -------------------------
    links = []
    articles = driver.find_elements(By.CSS_SELECTOR, "article h2 a")

    for a in articles:
        link = a.get_attribute("href")

        # Strong filter to avoid section pages
        if link and "/202" in link and link.endswith(".html"):
            if link not in links:
                links.append(link)

        if len(links) == 5:
            break

    print("\nCollected Article Links:")
    for l in links:
        print(l)

    print("\n" + "=" * 100)

    # -------------------------
    # Function to Translate Text using MyMemory API

    def translate_text(text):
        url = "https://api.mymemory.translated.net/get"
        
        params = {
            "q": text,
            "langpair": "es|en"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data["responseData"]["translatedText"]
        except Exception as e:
            print("Translation error:", e)
            return "Translation Failed"
    #-------------------------
    for idx, url in enumerate(links):
        print("\n" + "=" * 100)
        print(f"\nARTICLE {idx+1}")
        print("-" * 100)
        print("URL:", url)

        driver.get(url)
        # time.sleep(3)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))



        try:
            continue_btn = driver.find_elements(By.ID, "capping-continue")
            if continue_btn:
                continue_btn[0].click()
                print("Subscription overlay handled.")
        except:
            pass


        title = "Title Not Found"

        try:
            title_element = driver.find_element(By.CSS_SELECTOR, "h1.a_t")

        # Use JavaScript to extract full innerText safely
            title = driver.execute_script("return arguments[0].innerText;", title_element).strip()

        except Exception as e:
            print("Title extraction error:", e)
            title = "Title Not Found"

        print("\nTitle (Spanish):")
        print(title)

        translated_title = translate_text(title)

        print("\nTitle (English):")
        print(translated_title)

        # ---- Get Content ----
        try:
            content_div = driver.find_element(
                By.CSS_SELECTOR, "div[data-dtm-region='articulo_cuerpo']",
            )
            driver.execute_script("arguments[0].scrollIntoView();", content_div)
            time.sleep(2)
            content = content_div.text

            # If body exists but is empty → use summary
            if not content.strip():
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.a_st")))
                    summary = driver.find_element(By.CSS_SELECTOR, "h2.a_st")
                    content = driver.execute_script(
                        "return arguments[0].innerText;", summary
                    ).strip()
                except:
                    pass

        
        except Exception:
            print("Primary content selector failed. Trying gallery layout fallback...")

            try:
                text_container = driver.find_element(By.CSS_SELECTOR, "div.a_e_txt")

                content = driver.execute_script(
                    "return arguments[0].innerText;", text_container
                ).strip()

                if not content:
                    content = "Could not load article content."

            except:
                content = "Could not load article content."



        print("\nContent (Spanish):")
        print(content)


        # ---- Download Cover Image ----
        try:
            img_element = driver.find_element(By.CSS_SELECTOR, "img._re.a_m-h")

            srcset = img_element.get_attribute("srcset")

            if srcset:
                # Split multiple resolutions
                sources = srcset.split(",")

                # Take highest resolution (last entry)
                highest_res_url = sources[-1].strip().split(" ")[0]
                img_url = highest_res_url
            else:
                # fallback to src
                img_url = img_element.get_attribute("src")

            # Download image
            img_data = requests.get(img_url, timeout=10).content

            safe_title = "".join(c if c.isalnum() else "_" for c in title)[:50]
            file_path = f"article_images/{prefix}_{idx+1}_{safe_title}.jpg"

            with open(file_path, "wb") as f:
                f.write(img_data)

            print("✅ High-resolution image saved:", file_path)

        except Exception as e:
            print("Image download error:", e)

