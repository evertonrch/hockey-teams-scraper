import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from bs4 import BeautifulSoup

from urllib.parse import urljoin

from model.team import Team

URL = "https://www.scrapethissite.com/pages/forms/"

def setup() -> WebDriver:
    driver = webdriver.Chrome()
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

def create_team(row) -> Team:
    name = row.find(class_="name").text.strip()
    year = row.find(class_="year").text.strip()
    wins = row.find(class_="wins").text.strip()
    losses =row.find(class_="losses").text.strip()
    ot_losses = row.find(class_="ot-losses").text.strip()
    pct = row.find(class_="pct").text.strip()
    gf = row.find(class_="gf").text.strip()
    ga = row.find(class_="ga").text.strip()
    diff = row.find(class_="diff").text.strip()

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

def load_db(teams: list[Team]) -> None:
    pass

if __name__ == "__main__":
    with setup() as driver:
        driver.get(URL)

        links = extract_links(driver.page_source)

        for link in links:
            new_link = make_url(link)
            driver.get(new_link)
            time.sleep(0.5)

            html = get_soup(driver.page_source)
            teams = extract_teams(html)
            



        
    