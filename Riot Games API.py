import requests

API_KEY = open(r"C:\Users\Jae\Desktop\api_key.txt")
puuid = "jbsmMdaWH94ZhqeO2A6U_i7cS0JYtDjHSZJ_bNluxYZfgg3_E0GaSNWU4r_GYELvIlAULOZmo6u_eA"
match_history_url = "https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/MlPhG7YdJyzwZ6hLGDBFgGshR6TjJaiPX_kOehD8kfh7178PXJ14ZTjISLZFbwLOB5iEJ39g9JutZw/ids?start=0&count=20&api_key=RGAPI-623ee5ec-5af3-4642-8dcc-cf616b888a8e"
match_timeline_url = "https://sea.api.riotgames.com/lol/match/v5/matches/OC1_639113578/timeline?api_key=RGAPI-623ee5ec-5af3-4642-8dcc-cf616b888a8e"

response = requests.get(match_history_url).json()
match_id = response[0]
print(match_id)

match_timeline_info = requests.get(match_timeline_url).json()
match_timeline_info = match_timeline_info["info"]
print(match_timeline_info.keys())