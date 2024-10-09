import ast
import numpy as np
from selenium import webdriver # Version 3.3.0


# Timeline
link = "https://gol.gg/game/stats/44421/page-timeline/"
# link = "https://gol.gg/game/stats/44418/page-timeline/"

def process_gold_data(gold_data):
        """
        Helper function, Assumes blue top -> red supp

        gold_data: list(list())

        Returns: All gold variables needed for RNN
        """
        match_length = range(len(gold_data[0]))

        # Find gold diff
        blue_gold = np.sum(np.array(gold_data[:5]), axis=0)
        red_gold = np.sum(np.array(gold_data[5:]), axis=0)

        golddiff = np.sum(np.array([blue_gold, -1*red_gold]), axis=0)
        
        # Individual gold diff
        goldblueTop = gold_data[0]
        goldblueJungle = gold_data[1]
        goldblueMiddle = gold_data[2]
        goldblueADC = gold_data[3]
        goldblueSupport = gold_data[4]

        goldredTop = gold_data[5]
        goldredJungle = gold_data[6]
        goldredMiddle = gold_data[7]
        goldredADC = gold_data[8]
        goldredSupport = gold_data[9]

        return [golddiff,
            goldblueTop, goldblueJungle, goldblueMiddle, goldblueADC, goldblueSupport,
            goldredTop, goldredJungle, goldredMiddle, goldredADC, goldredSupport]


def process_link(link=link):
    driver = webdriver.PhantomJS(r"C:\Users\Jae\Documents\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver.get(link)
    html_page_source = driver.page_source

    # Important variable names
    golddatas = "golddatas"
    Events = "Events"
    csdatas  = "csdatas"

    blue_side = "../_img/blueside-icon.png"
    red_side = "../_img/redside-icon.png"

    kill = "../_img/kill-icon.png"
    tower = "../_img/tower-icon.png"
    plate = "PLATE" # Ignore such instances
    inhibs = "../_img/inhib-icon.png"
    dragons = "dragon.png"
    barons = "../_img/nashor-icon.png"
    hearlds = "../_img/herald-icon.png"

    # Variables
    count = 0
    role = None
    data = []
    gold_lists = []
    unprocessed_events = []

    # Data needed
    golddiff = [0 for i in range(95)]

    bKills = [0 for i in range(95)]
    bTowers = [0 for i in range(95)]
    bInhibs = [0 for i in range(95)]
    bDragons = [0 for i in range(95)]
    bBarons = [0 for i in range(95)]
    bHeralds = [0 for i in range(95)]

    rKills = [0 for i in range(95)]
    rTowers = [0 for i in range(95)]
    rInhibs = [0 for i in range(95)]
    rDragons = [0 for i in range(95)]
    rBarons = [0 for i in range(95)]
    rHeralds = [0 for i in range(95)]

    goldblueTop = [0 for i in range(95)]
    goldblueJungle = [0 for i in range(95)]
    goldblueMiddle = [0 for i in range(95)]
    goldblueADC = [0 for i in range(95)]
    goldblueSupport = [0 for i in range(95)]

    goldredTop = [0 for i in range(95)]
    goldredJungle = [0 for i in range(95)]
    goldredMiddle = [0 for i in range(95)]
    goldredADC = [0 for i in range(95)]
    goldredSupport = [0 for i in range(95)]

    # Process source
    # if count < 5 -> blue, count >=5 -> red
    html_page_source_list = html_page_source.split("\n")
    inside_golddatas = False
    inside_events = False

    def process_gold_data(gold_data):
        """
        Assumes blue top -> red supp

        gold_data: list(list())

        Returns: All gold variables needed for RNN
        """
        match_length = range(len(gold_data[0]))

        # Find gold diff
        blue_gold = np.sum(np.array(gold_data[:5]), axis=0)
        red_gold = np.sum(np.array(gold_data[5:]), axis=0)

        golddiff = np.sum(np.array([blue_gold, -1*red_gold]), axis=0)
        
        # Individual gold diff
        goldblueTop = gold_data[0]
        goldblueJungle = gold_data[1]
        goldblueMiddle = gold_data[2]
        goldblueADC = gold_data[3]
        goldblueSupport = gold_data[4]

        goldredTop = gold_data[5]
        goldredJungle = gold_data[6]
        goldredMiddle = gold_data[7]
        goldredADC = gold_data[8]
        goldredSupport = gold_data[9]

        return [golddiff,
            goldblueTop, goldblueJungle, goldblueMiddle, goldblueADC, goldblueSupport,
            goldredTop, goldredJungle, goldredMiddle, goldredADC, goldredSupport]

    def process_events_data(unprocessed_events, team):
        for event_num, unprocessed_event in enumerate(unprocessed_events[1:-1]):
            event_time = unprocessed_event.split("<td>")[1][:-5]
            team = unprocessed_event.split('img src="../_img/')[1].split("side-icon.png")[0]

            if kill in unprocessed_event:
                # If blue team gets kill
                if team == "blue":
                    bKills[int(event_time.split(":")[0])] += 1
                
                # If red team gets kill
                if team == "red":
                    print(event_time, team)
                    rKills[int(event_time.split(":")[0])] += 1

            elif tower in unprocessed_event:
                # If blue team gets tower
                if team == "blue":
                    bTowers[int(event_time.split(":")[0])] += 1
                
                # If red team gets tower
                if team == "red":
                    rTowers[int(event_time.split(":")[0])] += 1

            elif inhibs in unprocessed_event:
                # If blue team gets inhib
                if team == "blue":
                    bInhibs[int(event_time.split(":")[0])] += 1
                
                # If red team gets inhib
                if team == "red":
                    rInhibs[int(event_time.split(":")[0])] += 1

            elif dragons in unprocessed_event:
                # If blue team gets dragon
                if team == "blue":
                    bDragons[int(event_time.split(":")[0])] += 1
                
                # If red team gets dragon
                if team == "red":
                    rDragons[int(event_time.split(":")[0])] += 1

            elif barons in unprocessed_event:
                # If blue team gets barons
                if team == "blue":
                    bBarons[int(event_time.split(":")[0])] += 1
                
                # If red team gets barons
                if team == "red":
                    rBarons[int(event_time.split(":")[0])] += 1

            elif hearlds in unprocessed_event:
                # If blue team gets hearlds
                if team == "blue":
                    bHeralds[int(event_time.split(":")[0])] += 1
                
                # If red team gets hearlds
                if team == "red":
                    rHeralds[int(event_time.split(":")[0])] += 1

        stats = [('Blue Kills', bKills),
                ('Blue Towers', bTowers),
                ('Blue Inhibs', bInhibs),
                ('Blue Dragons', bDragons),
                ('Blue Barons', bBarons),
                ('Blue Heralds', bHeralds),
                ('Red Kills', rKills),
                ('Red Towers', rTowers),
                ('Red Inhibs', rInhibs),
                ('Red Dragons', rDragons),
                ('Red Barons', rBarons),
                ('Red Heralds', rHeralds)]

        for label, values in stats:
            print(f"{label}: {sum(values)}")

        return [bKills, bTowers, bInhibs, bDragons, bBarons, bHeralds,
            rKills, rTowers, rInhibs, rDragons, rBarons, rHeralds]

    for html_source_string in html_page_source_list:
        # Process gold data
        # If string is gold information
        if golddatas in html_source_string:
            inside_golddatas = True
        
        if inside_golddatas:
            if "label:" in html_source_string:
                role =  html_source_string.split(" ")[3][1:-2]
                # print("role:", role)
                count += 1
            
            if "data:" in html_source_string:
                data = html_source_string.split(" ")[3][:-2] + "]"
                team = "blue" if count < 6 else "red"
                data = ast.literal_eval(data)
                gold_lists.append(data)

        # If all of gold information extracted
        if csdatas in html_source_string:
            inside_golddatas = False
            process_gold_data(gold_lists)
        
        # Process events data
        # If string is events information
        if "Events" in html_source_string:
            inside_events = True
        
        # Save events to a list
        if inside_events:
            if blue_side in html_source_string or red_side in html_source_string:
                # Find first team that causes an event
                first_event_team_index = html_source_string.find("side-icon.png")
                first_event_team = html_source_string[first_event_team_index-7:first_event_team_index+20]
                first_event_team = first_event_team.split("/")[-1].split("side-icon.png")[0]

                # Save event to list
                # unprocessed_events += html_source_string.split("side-icon.png")
                unprocessed_events += html_source_string.split("resetPoint")

        # If end of events
        if "function ShowPoint" in html_source_string:
            inside_events = False
            process_events_data(unprocessed_events, first_event_team)
    
    return 