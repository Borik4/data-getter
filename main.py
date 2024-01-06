import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

FILE_PATH = os.environ.get("FILE_PATH", "test.txt")

with open(FILE_PATH, "r") as file:
    elems = [i.replace("\n", "") for i in file.readlines()]

print(elems)
lis = {}

# Launch the Chrome browser with Selenium
driver = webdriver.Chrome()
for st in elems:
    lis[st] = []


    url = f"https://www.amazon.com/s?k={st.replace(' ', '+')}"

    driver.get(url)
    # time.sleep(2000)

    # Find all the computer product elements on the page
    computer_products = driver.find_elements(By.CSS_SELECTOR,
                                             ".a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")

    urls = [computer_product.get_attribute("href") for computer_product in computer_products[::2]]

    # computer_products[0].click()
    for url in urls[:10]:
        driver.get(url)
        driver.implicitly_wait(3)
        try:
            computer_product = driver.find_elements(By.CSS_SELECTOR, ".a-section.a-spacing-small.a-spacing-top-small")[
                1]
            computer_products = computer_product.find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME,
                                                                                                 "tbody").find_elements(
                By.TAG_NAME, "tr")
        except Exception as e:
            print(url)
            continue


        params = {"url": url}

        for elem in computer_products:
            el = elem.find_elements(By.CSS_SELECTOR, ".a-span3")
            em = elem.find_elements(By.CSS_SELECTOR, ".a-span9")
            params[el[0].text] = em[0].text

        price_elem = driver.find_elements(By.CSS_SELECTOR,
                                          ".a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay")
        if not price_elem:
            continue
        price = price_elem[0].text.replace("\n", ".")

        params["price"] = price

        lis[st].append(params)
        print(params)


def get_data(driver, url):
    driver.get(url)
    driver.implicitly_wait(3)
    try:
        computer_product = driver.find_elements(By.CSS_SELECTOR, ".a-normal.a-spacing-micro")[0]
    except Exception:
        return

    computer_products = computer_product.find_elements(By.CSS_SELECTOR, ".a-spacing-small")

    params = {"url": url}

    for elem in computer_products:
        el = elem.find_elements(By.CSS_SELECTOR, ".a-span3")
        em = elem.find_elements(By.CSS_SELECTOR, ".a-span9")
        params[el[0].text] = em[0].text

    price_elem = driver.find_elements(By.CSS_SELECTOR,
                                      ".a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay")
    if not price_elem:
        return
    price = price_elem[0].text.replace("\n", ".")

    params["price"] = price

    lis[st].append(params)
    print(params)


with open("response.txt", "w") as f:
    f.write(json.dumps(lis))
