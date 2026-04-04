import time
import logging
from concurrent.futures import ThreadPoolExecutor
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup

from urllib.parse import urljoin

from model.team import Team
from dao.team_dao import save

logging.basicConfig(
    datefmt="%H:%M:%S",
    format="[{levelname}] - {asctime} - {message}", style="{",
    level=logging.INFO
)

URL = "https://www.scrapethissite.com/pages/forms/"

def setup() -> WebDriver:
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    return driver

def extract_links(html) -> list[str]:
    html = get_soup(html)
    pagination = html.find(class_="pagination")

    links = []
    for item in pagination.children:
        if item and item != "\n":
            
            if "aria-label" in item.find("a").attrs: # next link 
                continue

            link = item.find("a")["href"]
            links.append(link)

    return links

def get_soup(html) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

def make_url(link: str) -> str:
    URL_BASE = "https://www.scrapethissite.com"
    return urljoin(URL_BASE, link)

def normalize(text: str, to_int=False) -> str | int:
    return int(text.strip()) if to_int else text.strip() 

def create_team(row) -> Team:
    name = normalize(row.find(class_="name").text)
    year = normalize(row.find(class_="year").text, to_int=True)
    wins = normalize(row.find(class_="wins").text, to_int=True)
    losses = normalize(row.find(class_="losses").text, to_int=True)
    ot_losses = normalize(row.find(class_="ot-losses").text)
    pct = normalize(row.find(class_="pct").text)
    gf = normalize(row.find(class_="gf").text, to_int=True)
    ga = normalize(row.find(class_="ga").text, to_int=True)
    diff = normalize(row.find(class_="diff").text)

    return Team(
        name, year, wins, losses, ot_losses, pct, gf, ga, diff
    )

def extract_teams(html: BeautifulSoup) -> list[Team]:
    table = html.find("table")
    teams_rows = table.find("tbody").find_all(class_="team")
    teams: list[Team] = []
    for team_row in teams_rows:
        team = create_team(team_row)
        teams.append(team)
    
    return teams
    
if __name__ == "__main__":  
    with setup() as driver:
        driver.get(URL)

        links = extract_links(driver.page_source)
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            for link in links:
                new_link = make_url(link)
                driver.get(new_link)
                time.sleep(0.5)

                html = get_soup(driver.page_source)
                teams = extract_teams(html)

                for team in teams:
                    executor.submit(save, team)

            



        
    