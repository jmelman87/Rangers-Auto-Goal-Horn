import requests
import json
import asyncio
from kasa import SmartPlug
import time
import magichue
import pygame

async def siren():
    user = "ENTER USER / EMAIL HERE"
    pwd = 'ENTER PASSWORD HERE'
    file = 'PATH TO GOAL HORN MP3 FILE.mp3' 

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)

    api = magichue.RemoteAPI.login_with_user_password(user=user, password=pwd)

    p = SmartPlug("IP ADDRESS OF YOUR SMART PLUG")

    light = api.get_online_bulbs()[0]
    light.mode = magichue.RED_BLUE_CROSSFADE # creates red and blue effect on led lights
    await p.update()
    await p.turn_on()
    time.sleep(1)
    pygame.mixer.music.play()
    light.turn_on()
    time.sleep(60) # plays goal horn for 60 seconds
    await p.turn_off()
    light.turn_off()
    pygame.mixer.music.stop()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

team_id = 3 #CHANGE THIS TO YOUR TEAM ID
url = f'https://statsapi.web.nhl.com/api/v1/teams/{team_id}?expand=team.schedule.next'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)

    if 'nextGameSchedule' in data['teams'][0]:
        next_game = data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]
        game_pk = next_game['gamePk']
        game_date = next_game['gameDate']

        live_url = f"https://statsapi.web.nhl.com/api/v1/game/{game_pk}/feed/live"

        live_response = requests.get(live_url, headers=headers)

        if live_response.status_code == 200:
            live_data = json.loads(live_response.text)
            gameStatus = live_data['gameData']['status']['detailedState']

        else:
            print(f"Error: {live_response.status_code}")
        

        boxscore_url = f"https://statsapi.web.nhl.com/api/v1/game/{game_pk}/boxscore"
        
        boxscore_response = requests.get(boxscore_url, headers=headers)

        if boxscore_response.status_code == 200:
            boxscore_data = json.loads(boxscore_response.text)
            away_team = boxscore_data['teams']['away']['team']['name']
            home_team = boxscore_data['teams']['home']['team']['name']

            away_score = boxscore_data['teams']['away']['teamStats']['teamSkaterStats']['goals']
            home_score = boxscore_data['teams']['home']['teamStats']['teamSkaterStats']['goals']

            print(f"Game Date: {game_date}")
            print(f"Game Score: {away_team} {away_score} - {home_team} {home_score}")

            i = 0

            if(home_team == 'New York Rangers'):
                currentScore = home_score
                print("Rangers are the HOME team")
                
                while(gameStatus != 'Final'):
                    live_response = requests.get(live_url, headers=headers)

                    if live_response.status_code == 200:
                        live_data = json.loads(live_response.text)
                        gameStatus = live_data['gameData']['status']['detailedState']
                    
                    else:
                        print(f"Error: {live_response.status_code}")
                    
                    if gameStatus == 'Final': break
                    i = 0

                    while(i<15):
                        boxscore_response = requests.get(boxscore_url, headers=headers)
                        if boxscore_response.status_code == 200: 
                            boxscore_data = json.loads(boxscore_response.text)
                            home_score = boxscore_data['teams']['home']['teamStats']['teamSkaterStats']['goals']

                            if (home_score > currentScore):
                                currentScore = home_score
                                print("HOME GOAL!")
                                asyncio.run(siren())
                            
                            elif (home_score < currentScore):
                                currentScore = home_score
                                print("score error... now fixed.")
                            
                            else:
                                print("No change in score...")

                            time.sleep(4)
                            i = i+1

            else:
                currentScore = away_score
                print("Rangers are the AWAY team")

                while(gameStatus != 'Final'):
                    live_response = requests.get(live_url, headers=headers)

                    if live_response.status_code == 200:
                        live_data= json.loads(live_response.text)
                        gameStatus = live_data['gameData']['status']['detailedState']

                    else:
                        print(f"Error: {live_response.status_code}")
                    
                    if gameStatus == 'Final': break
                   
                    i = 0

                    while(i<15):
                        boxscore_response = requests.get(boxscore_url, headers=headers)

                        if boxscore_response.status_code == 200:
                            boxscore_data = json.loads(boxscore_response.text)
                            away_score = boxscore_data['teams']['away']['teamStats']['teamSkaterStats']['goals']

                            if (away_score > currentScore):
                                currentScore = away_score
                                print("AWAY GOAL!")
                                asyncio.run(siren())

                            elif (away_score < currentScore):
                                currentScore = away_score
                                print("score error... now fixed.")

                            else:
                                print("No change in score...")

                            time.sleep(4)
                            i = i+1
                            
            print("Game Over.")

        else:
            print(f"Error fetching boxscore data: {boxscore_response.status_code}")
else:
    print(f"Error: {response.status_code}")
