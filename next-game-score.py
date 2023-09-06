import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Replace '3' with the ID of the team you are interested in (3 is the ID for the New York Rangers...)
team_id = 3
url = f"https://statsapi.web.nhl.com/api/v1/teams/{team_id}?expand=team.schedule.next"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    
    # Check if there is a next game scheduled
    if 'nextGameSchedule' in data['teams'][0]:
        next_game = data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]
        game_pk = next_game['gamePk']
        
        # Construct the URL for the boxscore
        boxscore_url = f"https://statsapi.web.nhl.com/api/v1/game/{game_pk}/boxscore"
        
        # Make a request to the boxscore URL
        boxscore_response = requests.get(boxscore_url, headers=headers)
        
        if boxscore_response.status_code == 200:
            boxscore_data = json.loads(boxscore_response.text)
            away_team = boxscore_data['teams']['away']['team']['name']
            home_team = boxscore_data['teams']['home']['team']['name']
            
            # Extract the scores
            away_score = boxscore_data['teams']['away']['teamStats']['teamSkaterStats']['goals']
            home_score = boxscore_data['teams']['home']['teamStats']['teamSkaterStats']['goals']
            
            # Print the game score
            print(f"Game Score: {away_team} {away_score} - {home_score} {home_team}")
        else:
            print(f"Error fetching boxscore data: {boxscore_response.status_code}")
    else:
        print("No upcoming games scheduled.")
else:
    print(f"Error: {response.status_code}")
