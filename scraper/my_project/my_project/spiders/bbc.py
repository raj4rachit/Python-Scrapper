import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BbcSpider(scrapy.Spider):
    name = 'bbc'
    start_urls = ['https://www.bbc.com/sport/cricket']

    custom_settings = {
        'FEED_FORMAT': 'csv',  # Sets the feed export format as CSV
        'FEED_URI': 'cricket.csv',  # Sets the location of the output file
        'FEED_EXPORT_FIELDS': ['Product Name','Product Link']
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
            elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".e1gp961v0")))
            for element in elements:
                # Check if the anchor element exists within the headline element
                anchor_element = element.find_element(By.CSS_SELECTOR, " .exn3ah91")
                if anchor_element:
                    product_link = anchor_element.get_attribute('href')
                    product_name = anchor_element.text.strip()

                    yield {
                        'Product Name': product_name,
                        'Product Link': product_link,
                    }
                else:
                    self.logger.error("Anchor element not found within the headline element.")
        except Exception as e:
            self.logger.error(f"Error processing page: {e}")


    def closed(self, reason):
        self.driver.quit()

