from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from urllib.parse import urljoin

URL = "https://www.scrapethissite.com/pages/forms/"

def setup() -> WebDriver:
    driver = webdriver.Chrome()
    return driver

def extract_links(element_pagination) -> list[str]:
    links = []
    for item in element_pagination.children:
        if item and item != "\n":
            
            if "aria-label" in item.find("a").attrs:
                continue

            link = item.find("a")["href"]
            links.append(link)

    return links

def make_url(link: str) -> str:
    URL_BASE = "https://www.scrapethissite.com"
    return urljoin(URL_BASE, link)

if __name__ == "__main__":
    with setup() as driver:
        driver.get(URL)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        pagination = soup.find(class_="pagination")

        links = extract_links(pagination)

        for link in links:
            new_link = make_url(link)
            driver.get(new_link)



        
    