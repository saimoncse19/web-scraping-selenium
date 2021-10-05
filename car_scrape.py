"""

   Author: Saimon
   Date: October 5, 2021

   Task: Scraping edmunds.com (a website with strong anti-scraping mechanism)


"""


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


# driver setup
def set_up_browser(url: str):
    browser = webdriver.Chrome(ChromeDriverManager().install())

    browser.get("https://www.edmunds.com/cars-for-sale-by-owner")
    return browser


if __name__ == '__main__':
    zip_code = 49682
    driver = set_up_browser("https://www.edmunds.com/cars-for-sale-by-owner")
    driver.execute_script(f"""document.querySelector("input[name='zip']").value='{zip_code}'""")
    time.sleep(2)






