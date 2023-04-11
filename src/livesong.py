from ytmusicapi import YTMusic
import json
import openai
import lyricsgenius


ytmusic = YTMusic('headers_auth.json')
openai.api_key = "sk-"
genius_token = ''
genius = lyricsgenius.Genius(genius_token)
genius.verbose = False
genius.remove_section_headers = True


def like_song_in(video_id):
    ytmusic.rate_song(videoId=video_id,rating='LIKE')

def words_to_song(lyrics):
    request = genius.search_lyrics(lyrics)
    results = []
    for hit in request['sections'][0]['hits']:
        results.append(hit['result']['title'])
    return results

def get_current_song():
    data = ytmusic.get_history()

    top_history = data[:1]

    for item in top_history:
        video_id = item['videoId']
        artist_name = item['artists'][0]['name']
        song_name = item['title']
        album = item['album']['name'] if item['album'] else 'N/A'
        thumbnail_url = item['thumbnails'][1]['url'] if len(item['thumbnails']) > 1 else item['thumbnails'][0]['url']
        duration = item['duration']
        url = f"https://www.youtube.com/watch?v={item['videoId']}"
        if song_name == album:
            album = "None"

    return artist_name,song_name,album,thumbnail_url,duration,url,video_id

def get_song_name():
    liked_songs_raw = ytmusic.get_liked_songs()

    liked_songs = liked_songs_raw['tracks'][:1]
    for item in liked_songs:
        song_name = item['title']
    return song_name


def get_liked_song():
    liked_songs_raw = ytmusic.get_liked_songs()

    liked_songs = liked_songs_raw['tracks'][:1]

    for item in liked_songs:
        artist_name = item['artists'][0]['name']
        song_name = item['title']
        album = item['album']['name'] if item['album'] else 'N/A'
        thumbnail_url = item['thumbnails'][1]['url'] if len(item['thumbnails']) > 1 else item['thumbnails'][0]['url']
        duration = item['duration']
        url = f"https://www.youtube.com/watch?v={item['videoId']}"
        if song_name == album:
            album = "None"
    
    genre = classify_song_genre(song_name, artist_name)
    desc = description(song_name, artist_name)
    rdate = release_date(song_name,artist_name)
    #song_list = similar_songs(song_name, artist_name)
    song_list = ""

    return artist_name,song_name,album,thumbnail_url,duration,url,genre,desc,rdate,song_list

def get_lyrics(song_name,artist):
    song = genius.search_song(song_name, artist)

    if song is not None:
        lyrics = song.lyrics
        return lyrics
    else:
        lyrics = "Lyrics not found."
        return lyrics

def classify_song_genre(song_name, artist):
    prompt = f"Classify the song '{song_name}' by '{artist}' into a music genre with out a description"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    genre = response.choices[0].text.strip()
    return genre


def description(song_name, artist):
    prompt = f"Write me a short review in third person on the song {song_name} by {artist}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=250,
        n=1,
        stop=None,
        temperature=1,
    )

    desc = response.choices[0].text.strip()
    return desc

def release_date(song_name, artist):
    prompt = f"When did {song_name} by {artist} release display it as Release:mm/dd/yy only"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.5,
    )

    ogtext = response.choices[0].text.strip()

    if "Release:" in ogtext:
        rdate = ogtext[ogtext.index("Release:")+len("Release:"):][:10]
    else:
        rdate = "N/A"

    return rdate


def similar_songs(song_name, artist):
    prompt = f"What are 5 similar yet unique songs like {song_name} by {artist}, display as 1.x 2.x 3.x 4.x 5.x"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=550,
        n=1,
        stop=None,
        temperature=0.4,
    )

    song_list = response.choices[0].text.strip()

    return song_list
