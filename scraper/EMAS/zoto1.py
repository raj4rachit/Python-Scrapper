import time

import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Automatically install ChromeDriver
chromedriver_autoinstaller.install()

# Set up Chrome options
#chrome_options = Options()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
chrome_options.add_argument("--window-size=1920x1080")  # Sets the window size

# Specify the path to ChromeDriver
# chromedriver_path = r'chromedriver.exe'  # Update this path
# service = Service(executable_path=chromedriver_path)
#
# # Initialize the driver
# driver = webdriver.Chrome(service=service, options=chrome_options)

driver = webdriver.Chrome(options=chrome_options)

# Your scraping code here
driver.get("https://www.zomato.com/ahmedabad")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)  # Add a delay to allow content to load
#WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'jumbo-tracker')))
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.jumbo-tracker')))

#webdriver.support.ui.WebDriverWait(driver, 10)

try:
    # Get the page source after waiting
    temp_data = driver.page_source
    print(temp_data)
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(temp_data, "html.parser")

    # Find all elements with class "provider-info"
    directoryListings = soup.find_all('div', class_="jumbo-tracker")

    # Print the first element found
    if directoryListings:
        print(directoryListings[0])
    else:
        print("No provider info found.")
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
