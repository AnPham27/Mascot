import requests
from bs4 import BeautifulSoup

req = requests.get("https://data.perpetualmotion.org/allSports/schedule.php?leagueID=1957")

soup = BeautifulSoup(req.text, "lxml")

