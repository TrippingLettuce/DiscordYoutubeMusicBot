# DiscordYoutubeMusicBot
Discord Bot that displays currently listening too, liked music, writes descriptions for songs, recommends similar music, shows lyrics, search music by lyrics, like songs within discord.

## Example ScreenShots of Bot running 
![GitHub2P](https://user-images.githubusercontent.com/82426784/236603446-8c6e7a25-460f-4a4c-abfb-77d4d5b6a844.png)
![GitP1](https://user-images.githubusercontent.com/82426784/236603448-2486b47b-4b3f-4ec6-a4f5-8f99766949c8.png)
![rifhwjrn](https://user-images.githubusercontent.com/82426784/236603463-5eb10b38-616c-4be7-99fd-122445ac81d2.png)


Setting up everything for this bot is a lot so make sure to review the steps below

#### Installs
```
pip install discord.py
pip install ytmusicapi
pip install openai
pip install lyricsgenius
```

#### Documents
Discord.py 2.0 - https://discordpy.readthedocs.io/en/stable/index.html
YTMusicAPI - https://ytmusicapi.readthedocs.io/en/stable/index.html
OpenAI API - https://platform.openai.com/docs/introduction
Genius API - https://lyricsgenius.readthedocs.io/en/master/

#### Verification

Setting Up the header_auth for YTMusic can be done in chrome or firefox
Documentation (SetUp) - https://ytmusicapi.readthedocs.io/en/stable/setup.html

To run authenticated requests, set it up by first copying your request headers from an authenticated POST request in your browser. To do so, follow these steps:

Open a new tab
Open the developer tools (Ctrl-Shift-I) and select the “Network” tab
Go to https://music.youtube.com and ensure you are logged in
Find an authenticated POST request. The simplest way is to filter by /browse using the search bar of the developer tools. If you don’t see the request, try scrolling down a bit or clicking on the library button in the top bar.

**FireFox** 
Verify that the request looks like this: Status 200, Method POST, Domain music.youtube.com, File browse?...
Copy the request headers (right click > copy > copy request headers)

**Chrome** 
Verify that the request looks like this: Status 200, Name browse?...
Click on the Name of any matching request. In the “Headers” tab, scroll to the section “Request headers” and copy everything starting from “accept: */*” to the end of the section

**In your code**
To set up your project, open a Python console and call YTMusic.setup() with the parameter filepath=headers_auth.json and follow the instructions and paste the request headers to the terminal input: *This is going in your headers_auth file*
```Python
from ytmusicapi import YTMusic
YTMusic.setup(filepath="headers_auth.json")
```
The verifcation should have a very long span so dont worry about reverifying

#### Other API Tokens
OpenAI/Geunis are easy to get just make an account and get the token id
Input the token in live_song.py

*Lyrics Button* just broke out of no where if someone wants to fix that slash command still works thou

### Addtional Lyric Search Command
![Lryics](https://user-images.githubusercontent.com/82426784/236603483-2cc7cc20-2a8d-4b21-9057-c06ede213198.png)

