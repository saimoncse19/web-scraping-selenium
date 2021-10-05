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
import pandas as pd


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

    # selecting cars
    cars = driver.find_elements_by_class_name("usurp-inventory-card-vdp-link")

    pages_to_nav = inventory_count // len(cars)

    # Target pages links to navigate
    pages_links = [f"{paginate_url}{num}" for num in range(2, pages_to_nav)]

    # getting all the required URLs
    all_required_car_urls = []

    # 1st page
    for car in cars:
        all_required_car_urls.append(car.get_attribute('href'))

    for link in pages_links[:1]:
        driver.get(link)
        _cars = driver.find_elements_by_class_name("usurp-inventory-card-vdp-link")
        for car in _cars:
            all_required_car_urls.append(car.get_attribute('href'))

    # fields to scrape
    names = []
    prices = []
    vin_numbers = []
    vehicle_summaries = []
    top_specs = []

    # Only scrapping first 200 cars' details
    for link in all_required_car_urls[:20]:
        driver.get(link)

        # getting car name and saving it
        car_name = driver.find_element_by_xpath('//*[@class="not-opaque text-black d-inline-block mb-0 size-24"]')
        names.append(car_name.text) if car_name.text else names.append(None)

        # getting car price and saving it
        car_price = driver.find_element_by_xpath('//*[@data-test="vdp-price-row"]')
        prices.append(car_price.text) if car_price.text else None

        # getting vin number
        req_url = str(driver.current_url)
        car_vin = req_url.split('vin/')[1].split('/')[0] if req_url and 'vin/' in req_url else None
        vin_numbers.append(car_vin)

        # summary
        car_summary = driver.find_elements_by_xpath("""//*[contains(text(),'Vehicle Summary')]/following-sibling::div/div/div/div[2]""")
        final_summary = ''
        for summary in car_summary:
            final_summary += f" {summary.text}"
        vehicle_summaries.append(final_summary)

        # top features
        final_top_feature = ''
        top_features = driver.find_elements_by_xpath("//*[contains(text(),'Comfort & Convenience')]/following-sibling::div//ul")

        if top_features:
            for feature in top_features:
                final_top_feature += f' {feature.text}'
        else:
            final_top_feature = ''
        top_specs.append(final_top_feature)

    # export to csv/xlsx
    df = pd.DataFrame({
        'Name': names,
        'Price': prices,
        'VIN number': vin_numbers,
        'Vehicle Summary': vehicle_summaries,
        'Top Specs': top_specs
    })

    file = "output/car_data.xlsx"
    df.to_excel(file)

    driver.quit()







