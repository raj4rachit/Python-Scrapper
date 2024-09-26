import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Automatically install ChromeDriver
chromedriver_autoinstaller.install()

# URL of the BBC Sport Cricket page
url = 'https://www.bbc.com/sport/cricket'

# Configure the WebDriver
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the website
    driver.get(url)

    # Wait for the headlines to be visible
    wait = WebDriverWait(driver, 10)
    #wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "gs-c-promo-heading")))

    # Get the page source and create BeautifulSoup object
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Find the headlines
    headlines = soup.find_all('a', class_='exn3ah91')

    # Extract and print the headlines
    for headline in headlines:
        print(headline.text.strip())

except Exception as e:
    print("Error:", e)

finally:
    # Quit the WebDriver
    driver.quit()
