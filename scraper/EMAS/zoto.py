import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv

# Automatically install ChromeDriver
chromedriver_autoinstaller.install()

# URL of the website
url = 'https://www.zomato.com/ahmedabad'
domain = 'https://www.zomato.com'

# Configure the WebDriver
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
# chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
# chrome_options.add_argument("--window-size=1920x1080")  # Sets the window size
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the website
    driver.get(url)

    # Function to scroll down the page
    def smooth_scroll_down(driver, step=200):
        current_height = driver.execute_script("return document.body.scrollHeight")
        for y in range(0, current_height, step):
            driver.execute_script(f"window.scrollTo(0, {y});")
            time.sleep(0.05)  # Short sleep to mimic user scroll
        time.sleep(2)  # Longer sleep at the end to allow last bits of data to load


    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Add a delay to allow content to load

    # Wait for the main content to be loaded
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'jumbo-tracker')))

    # Initialize variable to keep track of loaded content
    old_content_height = 0

    # Loop until no new content is loaded
    while True:
        # Scroll down to trigger lazy loading
        #smooth_scroll_down(driver)
        scroll_down(driver)

        # Get the current height of the content
        new_content_height = driver.execute_script("return document.body.scrollHeight")

        # Check if new content is loaded
        if new_content_height == old_content_height:
            break  # Break the loop if no new content is loaded
        else:
            old_content_height = new_content_height


    # Get the page source after waiting
    temp_data = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(temp_data, "html.parser")

    # Find all the elements you want to scrape
    directoryListing = soup.find_all('div', class_="jumbo-tracker")

    # Write data to CSV file
    csv_filename = 'restaurant_details.csv'
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Image URL', 'Website Link', 'Rating', 'Price', 'Distance', 'Address', 'Phone', 'Open Hours'])  # Write header row

        # Iterate over each element
        for restaurant in directoryListing:
            # Extracting restaurant details
            name = restaurant.find('h4', class_='sc-1hp8d8a-0').text.strip() if restaurant.find('h4', class_='sc-1hp8d8a-0') else ''
            image_url = restaurant.find('img', class_='sc-s1isp7-5').get('src') if restaurant.find('img', class_='sc-s1isp7-5') else ''
            website_link = domain + restaurant.find('a', class_='sc-RWGNv').get('href') if restaurant.find('a', class_='sc-RWGNv') else ''
            rating = restaurant.find('div', class_='sc-1q7bklc-1').text.strip() if restaurant.find('div', class_='sc-1q7bklc-1') else ''
            price = restaurant.find('p', class_='sc-jkPxnQ').text.strip() if restaurant.find('p', class_='sc-jkPxnQ') else ''
            distance = restaurant.find('div', class_='min-basic-info-right').text.strip() if restaurant.find('div', class_='min-basic-info-right') else ''

            # Navigate to the restaurant's webpage to get more details
            driver.get(website_link)
            time.sleep(2)  # Add a delay to allow content to load

            # Parse the webpage of the restaurant
            restaurant_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract additional details such as address, phone number, and opening hours
            dImage = restaurant_soup.find('img', class_='sc-s1isp7-5').get('src')
            resultImage = dImage.split("?")
            image_url = resultImage[0]
            address = restaurant_soup.find('p', class_='sc-1hez2tp-0 clKRrC').text.strip() if restaurant_soup.find('p',class_='sc-1hez2tp-0 clKRrC') else ''
            phone = restaurant_soup.find('p', class_='sc-1hez2tp-0 fanwIZ').text.strip() if restaurant_soup.find('p',class_='sc-1hez2tp-0 fanwIZ') else ''
            opening_hours = restaurant_soup.find('span',class_='sc-kasBVs dfwCXs').text.strip() if restaurant_soup.find('span', class_='sc-kasBVs dfwCXs') else ''
            print(name)

            # Write row to CSV file
            writer.writerow([name, image_url, website_link, rating, price, distance, address, phone, opening_hours])

    print(f"Data has been written to '{csv_filename}' successfully.")

except Exception as e:
    print("Error:", e)
finally:
    # Quit the WebDriver
    driver.quit()
