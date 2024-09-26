import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
import chromedriver_autoinstaller
import random

class ClutchSpider(scrapy.Spider):
    name = 'clutch'
    allowed_domains = ['clutch.co']
    start_urls = ['https://clutch.co/']

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        # Add more user agents
    ]

    def __init__(self):
        # chromedriver_path = './chromedriver.exe'
        # service = Service(chromedriver_path)
        # chrome_options = Options()

        # Randomly select a user agent
        user_agent = random.choice(self.user_agents)
        headers = {'User-Agent': user_agent,
                   'Referer':self.start_urls[0],
                   'Accept-Language': 'en-US,en;q=0.8',
                   "X-RapidAPI-Key": "d29bfcaa58mshb83bad7f06085bbp1111f6jsn552ad0502200",
                   "X-RapidAPI-Host": "scrapers-proxy2.p.rapidapi.com"
        }

        # Automatically install ChromeDriver
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Uncomment to run headless
        chrome_options.add_argument(f'user-agent={user_agent}')
        #self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):

        return scrapy.Request(
            url='https://clutch.co/it-services/new-york-state?related_services=field_pp_sl_it_strategy2',
            callback=self.parse_target_page,
            cookies=response.headers.get('Set-Cookie'),
            headers={'Referer': 'https://clutch.co/'}
        )

    def parse_target_page(self, response):
        self.driver.get(response.url,headers=self.headers)
        try:
            # Wait until the provider-info div is present
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "provider-info")))

            # Use scrapy Selector to parse the HTML directly with Selenium
            sel = Selector(text=self.driver.page_source)

            # Extract company names
            company_names = sel.css('.provider-info--header .company .company_info .ppc-website-link::text').getall()

            for company_name in company_names:
                yield {'Company Name': company_name.strip()}  # Strip whitespace

        except Exception as e:
            self.logger.error(f"Error processing page: {e}")
        finally:
            self.driver.quit()  # Ensure driver closes even if there's an error

    def closed(self, reason):
        if self.driver:
            self.driver.quit()
