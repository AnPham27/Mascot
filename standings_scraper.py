import requests
from bs4 import BeautifulSoup


def standings():
    try:
        source = requests.get("https://data.perpetualmotion.org/web-app/standings/2011")
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')

    except Exception as e:
        print(e)

    # table = soup.find("table", class_="activeStandings table table-condensed table-striped f-small").find_all("th")


    teams = soup.find("tbody").find_all("a")

    waiting = False
    names = []

    for i in teams:
        names.append((i.text).replace("The ", '').replace("Birthday", "Bday").replace("With", "W/"))
        
        next_element = i.next_sibling.strip()
        #print(next_element)
        if "**" in next_element:
            waiting = True

    
    scores = soup.find("tbody").find_all("td", class_="text-center")

    point = []
    #wins, losses, ties, points, spirit points

    for i in scores:
        point.append(i.text)

  
        
    #no spirit score yet ~ less than 24 hours
    if len(point) == (len(names) * 4):
        count = 0
        total_num_scores = 4
        total_scores = len(names) * total_num_scores
        result = []

        #[team , W, L, T, P]
        row = []
        for i in range(len(names)):
            result.append(names[i])
            #[TEAM NAME, ]
            for j in range(total_num_scores):
                
                result.append(point[count])

                count += 1
            row.append(result)
            result=[]  


        headers = ['PL', 'TEAM', 'W', 'L', 'PTS']
        header_format = '{:<3} {:<17} {:<2} {:<2} {:<6}'

        chart = f"```\n{header_format.format(*headers)}\n"
        message = ""
        place = 1
            #[team , W, L, T, P]
        for r in row:
            chart += f"{place:<3} {r[0][:17].strip():<17} {r[1]:<2} {r[2]:<2} {r[4]:<6}\n"

            if r[0] == "Uppercuts":
                message += f"We are currently in {place}th place. Our spirit score is still being calculated. KEEP IT UP!!"

                if waiting == True:
                    message+= "Please note: Not all scores have been submitted at this moment. Check again later!"
            place += 1
        chart += "```"

    #spirit points are available
    else:
        count = 0
        total_num_scores = 5
        total_scores = len(names) * total_num_scores
        result = []

        #[team , W, L, T, P, SPIRIT]
        row = []
        for i in range(len(names)):
            result.append(names[i])
            #[TEAM NAME, ]
            for j in range(total_num_scores):
                
                result.append(point[count])

                count += 1
            row.append(result)
            result=[]  
            

        headers = ['PL', 'TEAM', 'W', 'L', 'SPRT']
        header_format = '{:<3} {:<17} {:<2} {:<2} {:<6}'

        chart = f"```\n{header_format.format(*headers)}\n"
        message = ""
        place = 1
            #[team , W, L, T, P]
        for r in row:
            chart += f"{place:<3} {r[0][:17].strip():<17} {r[1]:<2} {r[2]:<2} {r[5]:<6}\n"

            if r[0] == "Uppercuts":
                message += f"We are currently in {place}th place."
                if r[5] == "N/A":
                    message += f" Our spirit score is {r[5]} since it is our first game! Good luck!!"
                else: 
                    message += f" Our spirit score is {r[5]}! KEEP IT UP!!"
                
                if waiting == True:
                    message += "\nPlease note: Not all scores have been submitted at this moment. Please check again later!"
            place += 1
        chart += "```"
    
    return(chart, message)

def wednesday_standings():
    try:
        source = requests.get("https://data.perpetualmotion.org/web-app/standings/1982")
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')

    except Exception as e:
        print(e)

    # table = soup.find("table", class_="activeStandings table table-condensed table-striped f-small").find_all("th")


    teams = soup.find("tbody").find_all("a")
    names = []
    waiting = False

    for i in teams:
        names.append((i.text).replace("The ",'').replace("Birthday", "Bday").replace("With", "W/"))
        next_element = i.next_sibling.strip()
        #print(next_element)
        if "**" in next_element:
            waiting = True

    scores = soup.find("tbody").find_all("td", class_="text-center")

    point = []
    #wins, losses, ties, points, spirit points

    for i in scores:
        point.append(i.text)

  
        
    #no spirit score yet ~ less than 24 hours
    if len(point) == (len(names) * 4) and r[6]<1:
        count = 0
        total_num_scores = 6
        total_scores = len(names) * total_num_scores
        result = []

        #[team , W, L, T, P]
        row = []
        for i in range(len(names)):
            result.append(names[i])
            #[TEAM NAME, ]
            for j in range(total_num_scores):
                
                result.append(point[count])

                count += 1
            row.append(result)
            result=[]  


        headers = ['PL', 'TEAM', 'W', 'L', 'PTS']
        header_format = '{:<3} {:<17} {:<2} {:<2} {:<6}'

        chart = f"```\n{header_format.format(*headers)}\n"
        message = ""
        place = 1
            #[team , W, L, T, P]
        for r in row:
            chart += f"{place:<3} {r[0][:17].strip():<17} {r[1]:<2} {r[2]:<2} {r[3]:<6}\n"

            if r[0] == "Frisbeeana Jones":
                message += f"We are currently in {place}th place. Our spirit score is still being calculated. KEEP IT UP!!"
                
                if waiting == True:
                    message+= "Please note: Not all scores have been submitted at this moment. Check again later!"
            place += 1
        chart += "```"

    #spirit points are available
    else:
        
        count = 0
        total_num_scores = 6
        total_scores = len(names) * total_num_scores
        result = []

        #[team , W, L, T, P, SPIRIT]
        row = []
        for i in range(len(names)):
            result.append(names[i])
            #[TEAM NAME, ]
            for j in range(total_num_scores):
                
                result.append(point[count])

                count += 1
            row.append(result)
            result=[]  
            

        headers = ['PL', 'TEAM', 'W', 'L', 'SPRT']
        header_format = '{:<3} {:<17} {:<2} {:<2} {:<6}'

        chart = f"```\n{header_format.format(*headers)}\n"
        message = ""
        place = 1
            #[team , W, L, T, P]
        for r in row:
            chart += f"{place:<3} {r[0][:17].strip():<17} {r[1]:<2} {r[2]:<2} {r[6]:<6}\n"

            if r[0] == "Frisbeeana Jones":
                message += f"We are currently in {place}th place."
                if r[5] == "N/A":
                    message += f" Our spirit score is {r[6]} since it is our first game! Good luck!!"
                else: 
                    message += f" Our spirit score is {r[6]}! KEEP IT UP!!"

                if waiting == True:
                    message+= "Please note: Not all scores have been submitted at this moment. Check again later!"
            place += 1
        chart += "```"
    
    return(chart, message)


