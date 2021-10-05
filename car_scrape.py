"""

   Author: Saimon
   Date: October 5, 2021

   Task: Scraping edmunds.com (a website with strong anti-scraping mechanism)


"""


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


# driver setup
def set_up_browser(url: str):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    browser.maximize_window()
    WebDriverWait(browser, 10000).until(ec.visibility_of_element_located((By.TAG_NAME, 'body')))
    return browser


if __name__ == '__main__':
    zip_code = int(input("Enter Zip Code: "))
    radius = int(input("Enter radius range: 1 to 6: "))
    driver = set_up_browser("https://www.edmunds.com/cars-for-sale-by-owner")

    # inputting zip code
    zip_set = driver.find_element_by_name('zip')
    for _ in range(0, 6):
        zip_set.send_keys(Keys.BACKSPACE)

    zip_set.send_keys(f'{zip_code}')
    zip_set.send_keys(Keys.ENTER)
    time.sleep(2)

    # selecting radius
    rad = driver.find_element_by_id("search-radius-range-min")
    rad.send_keys(radius)
    time.sleep(1)
    rad.send_keys(Keys.ENTER)
    time.sleep(2)

    # inventory count: finding total filtered cars
    inventory_count = driver.find_element_by_class_name("inventory-count")
    inventory_count = str(inventory_count.text).split(" ")[0].replace(",", "")
    inventory_count = int(inventory_count)

    # pages to navigate...
    paginate_url = driver.find_element_by_xpath("//*[contains(@class, 'pagination-btn srp-text')]").get_attribute('href')[:-1]
    print(paginate_url)

    # selecting cars
    cars = driver.find_elements_by_class_name("usurp-inventory-card-vdp-link")

    pages_to_nav = inventory_count // len(cars)

    # Target pages links to navigate
    pages_links = [f"{paginate_url}{num}" for num in range(2, pages_to_nav)]

    # getting all the required URLs
    all_required_car_urls = []
    all_cars = [cars]

    for car in cars:
        print(car.get_attribute('href'))

    for link in pages_links[:3]:
        driver.get(link)
        _cars = driver.find_elements_by_class_name("usurp-inventory-card-vdp-link")
        all_cars.append(_cars)







