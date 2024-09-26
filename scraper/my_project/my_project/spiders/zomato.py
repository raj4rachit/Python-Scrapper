import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Zomato(scrapy.Spider):
    name = 'zomato'
    allowed_domains = ['zomato.com']
    start_urls = ['https://www.zomato.com/ahmedabad']

    custom_settings = {
        'FEED_FORMAT': 'csv',  # Sets the feed export format as CSV
        'FEED_URI': 'zomato.csv',  # Sets the location of the output file
    }

    def __init__(self):
        chromedriver_path = './chromedriver.exe'
        service = Service(chromedriver_path)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        try:
            # Extract data from the current page
            wait = WebDriverWait(self.driver, 10)
            restaurants = response.css('div.jumbo-tracker')
            print(restaurants)

            for restaurant in restaurants:
                name = restaurant.css('a.dIvKTC::text').get()
                yield {
                    'name': name,
                }
        except Exception as e:
            self.logger.error(f"Error processing page: {e}")

    # def parse(self, response):
    #     self.driver.get(response.url)
    #     try:
    #         # Using explicit wait to ensure elements are loaded
    #         wait = WebDriverWait(self.driver, 10)
    #         elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product")))
    #         for element in elements:
    #             product_code = element.find_element(By.CSS_SELECTOR, " .thumbnail .product-code").text
    #             product_name = element.find_element(By.CSS_SELECTOR, " .thumbnail .caption").text
    #             details_link = element.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
    #             #yield scrapy.Request(url=details_link, callback=self.parse_details, meta={'product_code': product_code, 'product_name': product_name})
    #
    #             yield {
    #                 'Product Code': product_code,
    #                 'Product Name': product_name,
    #                 'Product Link': details_link
    #             }
    #     except Exception as e:
    #         self.logger.error(f"Error processing page: {e}")


    def closed(self, reason):
        self.driver.quit()

