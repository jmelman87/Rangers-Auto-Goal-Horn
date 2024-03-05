# Rangers-Auto-Goal-Horn


** UPDATE MARCH 2024



I've always wanted to have my own goal horn with the Rangers goal song in my house whenever the Rangers score in a game. With this project, I'm proud to say that I have been able to accomplish just that! 



For this project, I used:

1. NHL API (https://statsapi.web.nhl.com/api) (UPDATE DECEMBER 2023: The NHL API has changed and is now available at https://api-web.nhle.com/v1/ )
2. Python with various modules
3. AC powered red siren light
4. KASA Smart Plug (used to control siren light)
5. LED strip lights (MagicHome LED controller)
6. A speaker (bluetooth or wired, doesn't matter)
7. (Raspberry Pi Pico W integration in progress...)


Here is a link to the detailed NHL API documentation to learn how to use the *NEW* API --> [https://github.com/dword4/nhlapi#teams](https://gitlab.com/dword4/nhlapi/-/blob/master/new-api.md)

Even if you're a fan of a different team, you could slightly modify this program to make it work for you! All you need is your team's abbreviation (ex: NYR) and team name (ex: Rangers). 

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
8. datetime
9. socket

The program uses Requests and JSON to make requests to the NHL's API and read back the information that is being provided by the API. It first checks to see what the next game scheduled is
for your team, and when it finds the information, it makes a new request to the game-specific boxscore and live feed URLs in order to retrieve information about the game, such as 
the game's date and time, the opponent, and the score. The program then runs a double nested while loop - the inner loop scans for a change in your team's score, and when a change is detected, the siren function is called, and the outer loop is scanning for a change in the game's status specifically to the value 'Final' so that the program understands the game is over
and will therefore end the program. 

To use your Kasa Smart Plug with Python, you will need to first install the python-kasa library: simply type "pip install python-kasa" in your terminal. Once that installs, you can use the command "kasa" to get information about devices that are online on your network, and this is how you can get the 
device's IP address. Please refer to this guide for more detailed information on python-kasa: https://python-kasa.readthedocs.io/en/latest/

In this program, I am also using Python to control my MagicHome Smart LED lights and make them flash blue and red when the Rangers score. If you have LED lights, you can buy a MagicHome LED controller on Amazon for $10-15 and use this function in your program too! And if you're using the program for a different team, you can have it flash a different set of colors. You'll need to run "pip install python-magichue" to install the necessary library. The documentation for the library can be found here: https://pypi.org/project/python-magichue/

I also have a 32x8 LED matrix screen connected to a Raspberry Pi Pico-W microchip, which waits to receive a signal from the main program (goal.py). When a goal is detected, a signal is sent by socket connection from the computer that's running the main program to the Pico microchip, and when the signal is received, the screen will display "NYR GOAL! RANGERS GOAL!". And after the goal siren and goal song complete, the main program will locate the name of the goal scorer within the API and then it will send another signal to the Pico, and then it will display the goal scorer's name. 

** I am currently working on integrating a Raspberry Pi Pico W microchip into the project. I have a 32x8 LED matrix screen that I am using to display a "NYR GOAL!!" sign when the Rangers score. The main program (goal.py) will send a signal to the Pico W over the Wi-Fi to trigger the LED matrix to turn on when they score. I am working on implementing a feature where the main program extracts the name of the player who scored the goal, and then sending the name via a string through a Wi-Fi signal to have the name displayed on the LED sign as well. **



