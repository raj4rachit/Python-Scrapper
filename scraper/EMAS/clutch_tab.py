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
url = 'https://clutch.co/it-services/new-york-state?related_services=field_pp_sl_it_strategy2'
domain = 'https://clutch.co'

# Configure the WebDriver
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
# chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
# chrome_options.add_argument("--window-size=1920x1080")  # Sets the window size
driver = webdriver.Chrome(options=chrome_options)

try:

    # Function to scrape company details
    def scrape_company(cLink):
        driver.execute_script(f"window.open('{cLink}', '_blank');")  # Open a new tab with the company's link

    # Write data to CSV file
    csv_filename = 'details_1.csv'
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #writer.writerow(['Name', 'Image URL', 'Website Link', 'Rating', 'Price', 'Distance', 'Address', 'Phone', 'Open Hours'])  # Write header row
        writer.writerow(['Name', 'Website Link', 'Total Reviews'])

        while True:
            # Navigate to the website
            driver.get(url)

            # Wait for the main content to be loaded
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'directory2')))

            # Get the page source after waiting
            temp_data = driver.page_source

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(temp_data, "html.parser")

            # Find all the elements you want to scrape
            directoryListing = soup.find_all('li', class_="provider-row")

            # Iterate over each element
            for company in directoryListing:
                # Extracting details
                name = company.find('a', class_='provider__title-link').text.strip() if company.find('a', class_='provider__title-link') else ''
                cLink = domain + company.find('a', class_='provider__title-link').get('href') if company.find('a', class_='provider__title-link') else ''

                if cLink:
                    # Open a new tab for each company
                    scrape_company(cLink)

            # Switch between all tabs and scrape data
            for i in range(1, len(driver.window_handles)):  # Skip the first tab (index 0)
                driver.switch_to.window(driver.window_handles[i])
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile_main')))

                # Extract the HTML content and parse it with BeautifulSoup
                temp_data_1 = driver.page_source
                soup1 = BeautifulSoup(temp_data_1, "html.parser")

                # Find company details in the profile section
                companyListing = soup1.find('div', class_="profile_content")
                companyListings = companyListing.find_all('section', class_="profile-scroll-spy-section")

                for companyData in companyListings:
                    reviewData = companyData.find('div', class_="metrics-total-reviews")
                    total_review_count = reviewData.find('span',
                                                         class_="sg-colored-card--accent").text.strip() if reviewData and reviewData.find(
                        'span', class_="sg-colored-card--accent") else ''

                    # Write the extracted data to the CSV file
                    writer.writerow([name, cLink, total_review_count])


            # next page url
            next_page = soup.find('a', class_="sg-pagination-v2-next").get('href') if soup.find('a', class_="sg-pagination-v2-next") else '#'
            if next_page == '#':
                break

            url = domain + next_page

    # Optionally close all tabs
    driver.quit()
    print(f"Data has been written to '{csv_filename}' successfully.")

except Exception as e:
    print("Error:", e)
finally:
    # Quit the WebDriver
    driver.quit()
