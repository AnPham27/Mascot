import requests
from bs4 import BeautifulSoup

req = requests.get("https://data.perpetualmotion.org/web-app/standings/1957")

soup = BeautifulSoup(req.text, "lxml")

table = soup.find("table", class_="activeStandings table table-condensed table-striped f-small")

headers = table.find_all("th")
titles = []
for i in headers:
    title = i.text
    titles.append(title)


print(titles)
print(soup.prettify())