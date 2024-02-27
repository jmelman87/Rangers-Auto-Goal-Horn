import requests
import json
import datetime
import asyncio
from kasa import SmartPlug
import time
import magichue
import pygame
import socket

async def siren(x):
    user = "YOUR MAGICHUE USERNAME HERE"
    pwd = 'MAGICHUE PASSWORD HERE'
    file = 'PATH TO GOAL HORN MP3 FILE HERE'

    time_of_goal = datetime.datetime.now()
    print(time_of_goal)
    
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)

    api = magichue.RemoteAPI.login_with_user_password(user=user, password=pwd)


    
    try:
        p = SmartPlug("KASA SMARTPLUG IP HERE")
        await p.update()
        await p.turn_on()
        time.sleep(1)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Exception occurred while working with SmartPlug: {str(e)}")

    try:
        light = api.get_online_bulbs()[0]
        light.mode = magichue.RED_BLUE_CROSSFADE
        light.turn_on()
        time.sleep(60)
    except Exception as e:
        print(f"Exception occurred while working with MagicHue light: {str(e)}")

    try:
        await p.turn_off()
       # light.turn_off()
        light.rgb = (255, 137, 18)
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Exception occurred while turning off SmartPlug and MagicHue light: {str(e)}")


# Get today's date and save it as a string.
current_datetime = datetime.datetime.now()
date = current_datetime.date()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

team_abbr = 'TEAM ABBREVIATION HERE' # Ex: NYR, WSH, LAK...
url = f'https://api-web.nhle.com/v1/club-schedule/{team_abbr}/week/now'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)

    # Iterate over the games and find the game with today's date
    for game in data.get('games', []):
        game_date = game.get('gameDate')
        if game_date == str(date):
            game_id = game.get('id')
            print("the game id is: ", game_id)
            

            box_url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
            box_response = requests.get(box_url, headers=headers)

            if box_response.status_code == 200:
                box_data = json.loads(box_response.text)

                gameStatus = box_data.get('gameState')
                print(gameStatus)

                while(gameStatus != 'LIVE'):
                    if 'score' in box_data['awayTeam'] and 'score' in box_data['homeTeam']:
                        break
                    else:
                        print("Game not started yet.")
                        time.sleep(60)
                        box_response = requests.get(box_url, headers=headers)
                        
                        if box_response.status_code == 200:
                            box_data = json.loads(box_response.text)

                            gameStatus = box_data.get('gameState')

                

                away_team_name = box_data['awayTeam']['name']['default']
                away_score = box_data['awayTeam']['score']
                home_team_name = box_data['homeTeam']['name']['default']
                home_score = box_data['homeTeam']['score']
                print(f"{away_team_name} {away_score} - {home_score} {home_team_name}")

                currentScore = 0
                i = 0 

                if(home_team_name == 'YOUR TEAM NAME HERE'): # Ex: Rangers, Capitals, Kings...
                    currentScore = home_score
                    print("Rangers are the home team")
                    while(gameStatus != 'OFF' and gameStatus != 'FUT'):
                            
                        box_response = requests.get(box_url, headers=headers)

                        if box_response.status_code == 200:
                            box_data = json.loads(box_response.text)
                            gameStatus = box_data.get('gameState')

                        else:
                            print(f"Error: {box_response.status_code}")

                        if gameStatus == 'OFF' or gameStatus == 'FUT': break
                        i = 0

                        while(i < 15):
                            box_response = requests.get(box_url, headers=headers)
                            if box_response.status_code == 200:
                                box_data = json.loads(box_data.text)
                                home_score = box_data['homeTeam']['score']

                                if (home_score > currentScore):
                                    # GOAL SCORED !
                                    currentScore = home_score
                                    print("HOME GOAL")
                                    asyncio.run(siren(game_id))

                                elif (home_score < currentScore):
                                    print("score error. fixing now...")
                                    currentScore = home_score
                                    
                                else:
                                    print("no change in score")
                                    
                                time.sleep(4)
                                i = i+1


                else:
                    currentScore = away_score
                    print("Rangers are the away team")
                    while(gameStatus != 'OFF' and gameStatus != 'FUT'):

                        box_response = requests.get(box_url, headers=headers)

                        if box_response.status_code == 200:
                            box_data = json.loads(box_response.text)
                            gameStatus = box_data.get('gameState')

                        else:
                            print(f"Error: {box_response.status_code}")

                        if gameStatus == 'OFF' or gameStatus == 'FUT': break
                        i = 0

                        while(i < 15):
                            box_response = requests.get(box_url, headers=headers)
                            if box_response.status_code == 200:
                                box_data = json.loads(box_response.text)
                                away_score = box_data['awayTeam']['score']

                                if (away_score > currentScore):
                                    # GOAL SCORED ! 
                                    currentScore = away_score
                                    print("AWAY GOAL")
                                    asyncio.run(siren(game_id))

                                elif (away_score < currentScore):
                                    print("score error. fixing now...")
                                    currentScore = away_score
                                    
                                else:
                                    print("no change in score")
                                    
                                time.sleep(4)
                                i = i+1
                    
                print("Game over")

                
            else:
                print(f"Error: {box_response.status_code}")

            
else:
    print(f"Error: {response.status_code}")


