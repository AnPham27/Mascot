import requests
from bs4 import BeautifulSoup
from datetime import date
import calendar
  

def get_upcoming_schedule(upcoming_date):

    if "Thursday" in upcoming_date:
        TEAM_NUM = 4
    
        try:
            source = requests.get("https://data.perpetualmotion.org/allSports/schedule.php?leagueID=2011")
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
        #print(dictionary)

        #day = soup.find("table").find_all("th", id="week_header")
        day = soup.find("table", class_="schedWeek table table-condensed table-striped table-responsive f-small").find_all_next("th", id="week_header")
        days = []



        for i in day:
            days.append(i.text)
        
        
        playoff = ["Thursday, October 5"]

        if today_date in playoff:
            return(f"We have playoffs that day, and there is no schedule for that yet.")
        elif today_date in days:
            print("yes")
        else:
            return(f"There are no games on {today_date}. Check for a different date")
        

        #print(days)

        nums =[]
        field_num = soup.find("tbody").find_all(id="field_name")

        for i in field_num:
            nums.append(i.text)

        #print(nums)

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

            group.insert(0, days[i // 7])

        #print(split_arrays)


        #games we are playing
        flagged_arrays = []

        for sub_array in split_arrays:
            if f'{TEAM_NUM}' in sub_array:
                flagged_arrays.append(sub_array)

        #print(flagged_arrays)


        #today_date = "Thursday, May 18"

        current_games = []

        for array in flagged_arrays:
            if array[0] == today_date:
                current_games.append(array)

        #print("MEEP")

        #print(current_games)
        #[['Thursday, August 10', 'Margaret # 4', '1', '12', '12', '9'], 'Dark', 'White']
        # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
        # 0  ,    1 ,     2,     3 ,    4 ,   5

        first = []
        second = []

        #find the times of each game and append it. 
        game_header = soup.find_all(id='game_header')
        times = []
        for i in game_header:
            times.append(i.text)
        print(times)   


        for i in range (len(current_games)):
            for j in range (len(current_games[0])):

                if j < 4 and current_games[i][j] == f'{TEAM_NUM}':
                    first.append(current_games[i])
                
                if j > 3 and current_games[i][j] == f'{TEAM_NUM}':
                    second.append(current_games[i])

            
        # print(first)
        # print(second)


        colour = ''
        second_colour = ''

        #first game colour 
        if f'{TEAM_NUM}' == first[0][2]:
            colour = 'Dark'
            first.append(colour)

        if f'{TEAM_NUM}' == first[0][3]:
            colour = 'White'
            first.append(colour)
        
        #second game colour

        if f'{TEAM_NUM}' == second[0][4]:
            second_colour = 'Dark'
            second.append(second_colour)

        if f'{TEAM_NUM}' == second[0][5]:
            second_colour = 'White'
            second.append(second_colour)


        print(first)
        print(second)
        #[['Thursday, August 10', 'Margaret # 4', '1', '12', '12', '9'], 'Dark', 'White', time]
        # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
        # 0  ,    1 ,     2,     3 ,    4 ,   5

        #four cases:
        # if games are on separate fields 
        # if games are on the same field
        # if first game is practice
        # if second game is practice

        message = ""

        # First game
        if first[0][1] != "Practice Area":
            if first[1] == 'Dark':
                message = f"{today_date}: our first game we are playing against **{dictionary[first[0][3]].strip()}** wearing **{first[1]}** on **{first[0][1]}**. "
            elif first[1] == 'White':
                message = f"{today_date}: our first game we are playing against **{dictionary[first[0][2]].strip()}** wearing **{first[1]}** on **{first[0][1]}**. "
    
            if today_date == "Thursday, September 14":
                message += "Our first game starts at **6:15 PM**. "

            elif today_date == "Thursday, September 21":
                message += "Our first game starts at **8:30 PM**. "
            else:
                message += "Our first game starts at **6:30 PM**. "

        else:
            message = f"{today_date}: our first game we are practicing at **{first[0][1]}**."

        # Second game
        if second[0][1] != "Practice Area":

            if second[1] == 'Dark':
                message += f"In our second game, we are playing against **{dictionary[second[0][5]].strip()}** wearing **{second[1]}** on **{second[0][1]}**. "
            elif second[1] == 'White':
                message += f"In our second game, we are playing against **{dictionary[second[0][4]].strip()}** wearing **{second[1]}** on **{second[0][1]}**. "
        
            if today_date == "Thursday, September 14":
                message += "Our second game starts at **7:05 PM**."
            elif today_date == "Thursday, September 21":
                message += "Our second game starts at **9:20 PM**."
            else:
                message += "Our second game starts at **7:20 PM**."            
        
        else:
            message += f"In our second game, we are practicing at **{second[0][1]}**."

        return message




    else:
        #for Wednesdays
        try:
            source = requests.get("https://data.perpetualmotion.org/allSports/schedule.php?leagueID=1982")
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

        TEAM_NUM = 2

        number = soup.find("table", class_="teamlist f-small").find_all(id="team_num_cell")
        team = soup.find("table", class_="teamlist f-small").find_all("a")

        numbers = []
        teams = []


        for i in number:
            numbers.append(i.text)

        for i in team:
            
            teams.append(i.text.replace("The ", ''))


        dictionary = dict(zip(numbers, teams))
        print(dictionary)

        #day = soup.find("table").find_all("th", id="week_header")
        day = soup.find("table", class_="schedWeek table table-condensed table-striped table-responsive f-small").find_all_next("th", id="week_header")
        days = []

        for i in day:
            days.append(i.text)
        
        
        playoff = ["Wednesday, August 23"]

        if today_date in playoff:
            return(f"We have playoffs that day, and there is no schedule for that yet.")
        elif today_date in days:
            print("yes")
        else:
            return(f"There are no games on {today_date}. Check for a different date")
        

        print(days)

        nums =[]
        field_num = soup.find("tbody").find_all(id="field_name")

        for i in field_num:
            nums.append(i.text)

        print(nums)

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
            if f'{TEAM_NUM}' in sub_array:
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

                if j < 4 and current_games[i][j] == f'{TEAM_NUM}':
                    first.append(current_games[i])
                
                if j > 3 and current_games[i][j] == f'{TEAM_NUM}':
                    second.append(current_games[i])

            
        # print(first)
        # print(second)


        colour = ''
        second_colour = ''
        #first game colour 
        if f'{TEAM_NUM}' == first[0][2]:
            colour = 'Dark'
            first.append(colour)

        if f'{TEAM_NUM}' == first[0][3]:
            colour = 'White'
            first.append(colour)
        
        #second game colour

        if f'{TEAM_NUM}' == second[0][4]:
            second_colour = 'Dark'
            second.append(second_colour)

        if f'{TEAM_NUM}' == second[0][5]:
            second_colour = 'White'
            second.append(second_colour)


        #print(first)
        #print(second)


        #four cases:
        # if games are on separate fields 
        # if games are on the same field
        # if first game is practice
        # if second game is practice

        message = ""

        # First game
        if first[0][1] != "Practice Area":
            if first[1] == 'Dark':
                message = f"{today_date}: our first game we are playing against **{dictionary[first[0][3]].strip()}** wearing **{first[1]}** on **{first[0][1]}**. "
            elif first[1] == 'White':
                message = f"{today_date}: our first game we are playing against **{dictionary[first[0][2]].strip()}** wearing **{first[1]}** on **{first[0][1]}**. "
        else:
            message = f"{today_date}: our first game we are practicing at **{first[0][1]}**."

        # Second game
        if second[0][1] != "Practice Area":
            if second[1] == 'Dark':
                message += f"In our second game, we are playing against **{dictionary[second[0][5]].strip()}** wearing **{second[1]}** on **{second[0][1]}**. "
            elif second[1] == 'White':
                message += f"In our second game, we are playing against **{dictionary[second[0][4]].strip()}** wearing **{second[1]}** on **{second[0][1]}**. "
        else:
            message += f"In our second game, we are practicing at **{second[0][1]}**."

        return message