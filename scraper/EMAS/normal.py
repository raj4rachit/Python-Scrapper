import requests
from bs4 import BeautifulSoup

url = 'https://www.danfoss.com/en/products/dps/'
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
directoryListing = soup.find('div', class_="product-segments-item")

print(directoryListing)