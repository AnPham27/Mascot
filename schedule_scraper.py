import requests
from bs4 import BeautifulSoup
from datetime import date
import calendar


def get_schedule():
    
    try:
        source = requests.get("https://data.perpetualmotion.org/allSports/schedule.php?leagueID=1957")
        #source = requests.get("https://data.perpetualmotion.org/web-app/standings/1955")
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')

    except Exception as e:
        print(e)

    # Get today's date
    today = date.today()
    d2 = today.strftime("%B %d")
    today_date = f"{calendar.day_name[today.weekday()]}, {d2}"
    
    # today_date = "Thursday, June 15"

    number = soup.find("table", class_="teamlist f-small").find_all(id="team_num_cell")
    team = soup.find("table", class_="teamlist f-small").find_all("a")

    numbers = []
    teams = []



  
    for i in number:
        numbers.append(i.text)

    for i in team:
        
        teams.append(i.text.replace("The ", ''))


    dictionary = dict(zip(numbers, teams))

    #{'1': 'Butterfingers', '6': 'DISCount Athletes', '2': 'Hammerrhoids', '7': 'Huck Dynasty', '3': '5 Alive', 
    # '8': 'Hammer Time', '4': 'Uppercuts', '9': 'Handle With Care', '5': 'Huck Tales', '10': 'Deborah'}




    #day = soup.find("table").find_all("th", id="week_header")
    day = soup.find("table", class_="schedWeek table table-condensed table-striped table-responsive f-small").find_all_next("th", id="week_header")
    days = []
   
    
    for i in day:
        days.append(i.text)
    # print(days)

    
    if today_date in days:
        print("yes")
    else:
        return("There are no games today! Check again on Thursday")
    

    #print(days)

    # nums =[]
    # field_num = soup.find("tbody").find_all(id="field_name")

    # for i in field_num:
    #     nums.append(i.text)


    # left_team = soup.find("tbody").find_all_next("a")
    opponent = soup.find("tbody").find_all_next("a")
    opponents = []
    count = 0
    for i in opponent:
        #opponents.append(days[len(opponents)])
        opponents.append(i.text) 
        count+= 1   


    count = 0
    # Field #, LEFT , RIGHT, LEFT, RIGHT 
    #      0 ,   1 ,    2,     3 ,   4

    split_arrays = []
    chunk_size = 5
    n = len(opponents)


    for i in range(0, n, chunk_size):
        sub_array = []

        for j in range(i, min(i + chunk_size, n)):
            
            sub_array.append(opponents[j])
        

        #sub_array.insert(0, days[count])
        split_arrays.append(sub_array)

    #date each game: 
    # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
    # 0  ,    1 ,     2,     3 ,    4 ,   5
    for i, group in enumerate(split_arrays):
        group.insert(0, days[i // 5])

    #print(split_arrays)


    #games we are playing
    flagged_arrays = []

    for sub_array in split_arrays:
        if '4' in sub_array:
            flagged_arrays.append(sub_array)

    #print(flagged_arrays)

   
    current_games = []

    for array in flagged_arrays:
        if array[0] == today_date:
            current_games.append(array)

    
    #print(current_games)
  
    #
    # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
    # 0  ,    1 ,     2,     3 ,    4 ,   5

    first = []
    second = []

    for i in range (len(current_games)):
        for j in range (len(current_games[0])):

            if j < 4 and current_games[i][j] == '4':
                first.append(current_games[i])
            
            if j > 3 and current_games[i][j] == '4':
                second.append(current_games[i])

        
    # print(first)
    # print(second)


    colour = ''

    #first game colour 
    if '4' == first[0][2] or '4' == first[0][4]:
        colour = 'Dark'
        first.append(colour)

    if '4' == first[0][3] or '4' == first[0][5]:
        colour = 'White'
        first.append(colour)

    if '4' == second[0][2] or '4' == second[0][4]:
        colour = 'Dark'
        second.append(colour)

    if '4' == second[0][3] or '4' == second[0][5]:
        colour = 'White'
        second.append(colour)


    # print(first)
    # print(second)


    #two cases if games are on separate fields 
    # and if games are on the same field


    message = ""

    #first game 
    if first[1] == 'Dark':
        message = f"@everyone {today_date}: our first game we are playing against **{dictionary[first[0][3]]}** wearing **{first[1]}** on **{first[0][1]}**. "

    else:   
        message = f"@everyone {today_date}: our first game we are playing against **{dictionary[first[0][5]]}** wearing **{first[1]}** on **{first[0][1]}**. "

    #second game
    if second[1] == 'Dark':
        message += f"In our second game, we are playing against **{dictionary[second[0][5]]}** wearing **{second[1]}** on **{second[0][1]}**. "

    else:   
        message += f"In our second game, we are playing against **{dictionary[second[0][4]]}** wearing **{second[1]}** on **{second[0][1]}**. "

    return message  


def get_upcoming_schedule(upcoming_date):
    try:
        source = requests.get("https://data.perpetualmotion.org/allSports/schedule.php?leagueID=1957")
        #source = requests.get("https://data.perpetualmotion.org/web-app/standings/1955")
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')

    except Exception as e:
        print(e)

    # # Get today's date
    # today = date.today()
    # d2 = today.strftime("%B %d")
    # today_date = f"{calendar.day_name[today.weekday()]}, {d2}"

    today_date = upcoming_date

    number = soup.find("table", class_="teamlist f-small").find_all(id="team_num_cell")
    team = soup.find("table", class_="teamlist f-small").find_all("a")

    numbers = []
    teams = []


    for i in number:
        numbers.append(i.text)

    for i in team:
        
        teams.append(i.text.replace("The ", ''))


    dictionary = dict(zip(numbers, teams))

    #{'1': 'Butterfingers', '6': 'DISCount Athletes', '2': 'Hammerrhoids', '7': 'Huck Dynasty', '3': '5 Alive', 
    # '8': 'Hammer Time', '4': 'Uppercuts', '9': 'Handle With Care', '5': 'Huck Tales', '10': 'Deborah'}


    #day = soup.find("table").find_all("th", id="week_header")
    day = soup.find("table", class_="schedWeek table table-condensed table-striped table-responsive f-small").find_all_next("th", id="week_header")
    days = []

    for i in day:
        days.append(i.text)
    
    
    playoff = ["Thursday, June 29"]

    if today_date in playoff:
        return(f"We have playoffs that day, and there is no schedule for that yet.")
    elif today_date in days:
        print("yes")
    else:
        return(f"There are no games on {today_date}. Check for a different date")
    

    #print(days)

    # nums =[]
    # field_num = soup.find("tbody").find_all(id="field_name")

    # for i in field_num:
    #     nums.append(i.text)


    # left_team = soup.find("tbody").find_all_next("a")
    opponent = soup.find("tbody").find_all_next("a")
    opponents = []
    count = 0
    for i in opponent:
        #opponents.append(days[len(opponents)])
        opponents.append(i.text) 
        count+= 1   


    count = 0
    # Field #, LEFT , RIGHT, LEFT, RIGHT 
    #      0 ,   1 ,    2,     3 ,   4

    split_arrays = []
    chunk_size = 5
    n = len(opponents)


    for i in range(0, n, chunk_size):
        sub_array = []

        for j in range(i, min(i + chunk_size, n)):
            
            sub_array.append(opponents[j])
        

        #sub_array.insert(0, days[count])
        split_arrays.append(sub_array)

    #date each game: 
    # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
    # 0  ,    1 ,     2,     3 ,    4 ,   5
    for i, group in enumerate(split_arrays):
        group.insert(0, days[i // 5])

    #print(split_arrays)


    #games we are playing
    flagged_arrays = []

    for sub_array in split_arrays:
        if '4' in sub_array:
            flagged_arrays.append(sub_array)

    #print(flagged_arrays)


    #today_date = "Thursday, May 18"

    current_games = []

    for array in flagged_arrays:
        if array[0] == today_date:
            current_games.append(array)

    #print("MEEP")

    #print(current_games)
    #
    # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
    # 0  ,    1 ,     2,     3 ,    4 ,   5

    first = []
    second = []

    for i in range (len(current_games)):
        for j in range (len(current_games[0])):

            if j < 4 and current_games[i][j] == '4':
                first.append(current_games[i])
            
            if j > 3 and current_games[i][j] == '4':
                second.append(current_games[i])

        
    # print(first)
    # print(second)


    colour = ''

    #first game colour 
    if '4' == first[0][2] or '4' == first[0][4]:
        colour = 'Dark'
        first.append(colour)

    if '4' == first[0][3] or '4' == first[0][5]:
        colour = 'White'
        first.append(colour)

    if '4' == second[0][2] or '4' == second[0][4]:
        colour = 'Dark'
        second.append(colour)

    if '4' == second[0][3] or '4' == second[0][5]:
        colour = 'White'
        second.append(colour)


    # print(first)
    # print(second)


    #two cases if games are on separate fields 
    # and if games are on the same field


    message = ""

    #first game 
    if first[1] == 'Dark':
        message = f"{today_date}: our first game we are playing against **{dictionary[first[0][3]]}** wearing **{first[1]}** on **{first[0][1]}**. "

    else:   
        message = f"{today_date}: our first game we are playing against **{dictionary[first[0][5]]}** wearing **{first[1]}** on **{first[0][1]}**. "

    #second game
    if second[1] == 'Dark':
        message += f"In our second game, we are playing against **{dictionary[second[0][5]]}** wearing **{second[1]}** on **{second[0][1]}**. "

    else:   
        message += f"In our second game, we are playing against **{dictionary[second[0][4]]}** wearing **{second[1]}** on **{second[0][1]}**. "

    return message  