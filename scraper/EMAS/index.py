import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

# Automatically install ChromeDriver
chromedriver_autoinstaller.install()

# URL of your React website
#url = "https://www.emaselectric.com/products/a--control-units-and-pilot-lights/b--b-series-plastic"
url='https://clutch.co/it-services/new-york-state?related_services=field_pp_sl_it_strategy2'

# Configure the WebDriver
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
# Navigate to the website
driver.get(url)
webdriver.support.ui.WebDriverWait(driver, 10)



# Wait for the element you want to scrape to be visible
try:
    temp_data = driver.page_source
    soup = BeautifulSoup(temp_data, "html.parser")
    directoryListing = soup.find('div', class_="provider-info")
    print(directoryListing)
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
