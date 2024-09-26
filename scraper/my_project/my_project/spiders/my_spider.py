import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['https://www.emaselectric.com/products/a--control-units-and-pilot-lights/b--b-series-plastic']

    custom_settings = {
        'FEED_FORMAT': 'csv',  # Sets the feed export format as CSV
        'FEED_URI': 'product.csv',  # Sets the location of the output file
        'FEED_EXPORT_FIELDS': ['Product Code', 'Product Name','Product Link']
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
            # Using explicit wait to ensure elements are loaded
            wait = WebDriverWait(self.driver, 10)
            elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product")))
            for element in elements:
                product_code = element.find_element(By.CSS_SELECTOR, " .thumbnail .product-code").text
                product_name = element.find_element(By.CSS_SELECTOR, " .thumbnail .caption").text
                details_link = element.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                #yield scrapy.Request(url=details_link, callback=self.parse_details, meta={'product_code': product_code, 'product_name': product_name})

                yield {
                    'Product Code': product_code,
                    'Product Name': product_name,
                    'Product Link': details_link
                }
        except Exception as e:
            self.logger.error(f"Error processing page: {e}")

    def parse_details(self, response):
        self.driver.get(response.url)
        try:
            wait = WebDriverWait(self.driver, 10)
            # Update the selector to match the price element on the product detail page
            price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".shop.details")))
            product_name = price_element.find_element(By.CSS_SELECTOR, " .product-details .caption-full h3").text
            #standard = price_element.find_element(By.CSS_SELECTOR, " .product-details .caption-full span.label-default").text
            yield {
                'Product Code': response.meta['product_code'],
                'Product Name': product_name
            }
        except Exception as e:
            self.logger.error(f"Error processing details page for {response.meta['product_code']}: {e}")

    def closed(self, reason):
        self.driver.quit()

