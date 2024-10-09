import ast
import re
from selenium import webdriver # Version 3.3.0


driver = webdriver.PhantomJS(r"C:\Users\Jae\Documents\phantomjs-2.1.1-windows\bin\phantomjs.exe")

# Timeline
driver.get("https://gol.gg/game/stats/44421/page-timeline/")
html_page_source = driver.page_source

# Important variable names
golddatas = "golddatas"
Events = "Events"
csdatas  = "csdatas"

blue_side = "../_img/blueside-icon.png"
red_side = "../_img/redside-icon.png"

# Variables
count = 0
role = None
data = []
gold_lists = []
unprocessed_events = []

# Data needed
golddiff = []

bKills = []
bTowers = []
bInhibs = []
bDragons = []
bBarons = []
bHeralds = []

rKills = []
rTowers = []
rInhibs = []
rDragons = []
rBarons = []
rHeralds = []

goldblueTop = []
goldblueJungle = []
goldblueMiddle = []
goldblueADC = []
goldblueSupport = []

goldredTop = []
goldredJungle = []
goldredMiddle = []
goldredADC = []
goldredSupport = []

# Process source
# if count <= 4 -> blue, count >=5 -> red
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
    print(sum(gold_data[:5][t] for t in match_length))
    # golddiff.append(sum(event[:5][t] for t in match_length))

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
            unprocessed_events += html_source_string.split("side-icon.png")

    # If end of events
    if "function ShowPoint" in html_source_string:
        inside_events = False

        # If list has been populated
        # print(unprocessed_events[0])
        # print("==========================")
        # print(unprocessed_events[1])
        
        # for event in unprocessed_events:
        #     print(event)
        #     print("==========================")

print('Done')