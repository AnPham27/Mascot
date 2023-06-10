import requests
from bs4 import BeautifulSoup
from datetime import date
import calendar



try:
    source = requests.get("https://data.perpetualmotion.org/allSports/schedule.php?leagueID=1957")
    #source = requests.get("https://data.perpetualmotion.org/web-app/standings/1955")
    source.raise_for_status()

    soup = BeautifulSoup(source.text, 'html.parser')

except Exception as e:
    print(e)

number = soup.find("table", class_="teamlist f-small").find_all(id="team_num_cell")
team = soup.find("table", class_="teamlist f-small").find_all("a")

numbers = []
teams = []



index = 0
for i in number:
    numbers.append(i.text)

for i in team:
    
    teams.append(i.text.replace("The ", ''))


dictionary = dict(zip(numbers, teams))

#{'1': 'Butterfingers', '6': 'DISCount Athletes', '2': 'Hammerrhoids', '7': 'Huck Dynasty', '3': '5 Alive', 
# '8': 'Hammer Time', '4': 'Uppercuts', '9': 'Handle With Care', '5': 'Huck Tales', '10': 'Deborah'}


# Get today's date
today = date.today()
d2 = today.strftime("%B %d")
date = f"{calendar.day_name[today.weekday()]}, {d2}"

#day = soup.find("table").find_all("th", id="week_header")
day = soup.find("table", class_="schedule").find_all("th", id="week_header")
days = []

for i in day:
    days.append(i.text)


print(date)
print(days)


