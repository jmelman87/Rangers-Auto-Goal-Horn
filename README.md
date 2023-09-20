# Rangers-Auto-Goal-Horn

I've always wanted to have my own goal horn with the Rangers goal song in my house whenever the Rangers score in a game. With this project, I'm proud to say that I have been able to accomplish just that! 


For this project, I used:

1. NHL API (https://statsapi.web.nhl.com/api)
2. Python with various modules
3. AC powered red siren light
4. KASA Smart Plug (used to control siren light)
5. LED strip lights (MagicHome LED controller)
6. A speaker (bluetooth or wired, doesn't matter)
7. (Raspberry Pi Pico W integration in progress...)


Here is a link to the detailed NHL API documentation to learn how to use the API --> https://github.com/dword4/nhlapi#teams

Even if you're a fan of a different team, you could slightly modify this program to make it work for you! All you'll really need to get is your team's ID, which 
can be found here: https://statsapi.web.nhl.com/api/v1/teams - just search for your team name, and the ID listed above your team name is your team's ID.

It is also important to take note of the way the full name is spelled under "name", as you will need to replace 'New York Rangers' on line 81 in goal.py with your team's 
EXACT name, including capital letters. 

Make sure to also get an MP3 file of your team's goal song, and get the filepath. I did this simply by searching for the goal song on YouTube and then using a third party website to download the video as an MP3. 

Also, if you don't want to use the same equipment I used to run the goal effect, you can of course modify the entire siren() function to do something else when your team scores. 

My python script for this project utilizies the following modules:
1. time
2. requests
3. json
4. asyncio
5. kasa 
6. magichue
7. pygame

The program uses Requests and JSON to make requests to the NHL's API and read back the information that is being provided by the API. It first checks to see what the next game scheduled is
for your team, and when it finds the information, it makes a new request to the game-specific boxscore and live feed URLs in order to retrieve information about the game, such as 
the game's date and time, the opponent, and the score. The program then runs a double nested while loop - the inner loop scans for a change in your team's score, and when a change is detected, the siren function is called, and the outer loop is scanning for a change in the game's status specifically to the value 'Final' so that the program understands the game is over
and will therefore end the program. 

To use your Kasa Smart Plug with Python, you will need to first install the python-kasa library: simply type "pip install python-kasa" in your terminal. Once that installs, you can use the command "kasa" to get information about devices that are online on your network, and this is how you can get the 
device's IP address. Please refer to this guide for more detailed information on python-kasa: https://python-kasa.readthedocs.io/en/latest/

** I am currently working on integrating a Raspberry Pi Pico W microchip into this project. I want the program to run off a microchip, instead of off my computer. The Pico W has Wi-Fi capability and will be able to connect to the NHL API directly. 



