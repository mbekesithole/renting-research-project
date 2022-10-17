import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

GOOGLE_FORM_URL = "https://forms.gle/xs3cxre7XvqBmMLE8"
ZILLOW_URL = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22mapBounds%22%3A%7B%22north%22%3A37.8826759178948%2C%22east%22%3A-122.23248568896484%2C%22south%22" \
             "%3A37.66775178944106%2C%22west%22%3A-122.63417331103516%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22" \
             "%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1" \
             "%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C" \
             "%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22rad%22%3A%7B%22value%22%3A%222022-11-01%22%7D%7D%2C%22isListVisible%22" \
             "%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D "

header = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
}
response = requests.get(url=ZILLOW_URL, headers=header)
zillow_page = response.text

soup = BeautifulSoup(zillow_page, "html.parser")

all_address_elements = soup.select(".property-card-link address")
addresses_list = [address.get_text().split(" | ")[-1] for address in all_address_elements]

all_price_elements = soup.select(".hRqIYX span")
all_prices = [price.get_text().split("+")[0].split("/")[0] for price in all_price_elements if "$" in price.text]

all_link_elements = soup.select(".property-card-data a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

service = Service("C:\\Development\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

for i in range(len(all_links)):
    driver.get(GOOGLE_FORM_URL)

    time.sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                            '1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                          '1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                         '1]/div/div[1]/input')
    submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address.send_keys(addresses_list[i])
    price.send_keys(all_prices[i])
    link.send_keys(all_links[i])
    submit_btn.click()
