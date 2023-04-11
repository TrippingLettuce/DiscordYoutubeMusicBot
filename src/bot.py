import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands 
import json
import datetime
import livesong
import asyncio
from collections import defaultdict

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

ADMIN_ID =  #Your Discord ID
current_channel =  # Channel ID where currently listing too music is displayed
liked_channel =  # Channel ID where liked songs with its features go
emoji_like = "👍" 
bot_key = ""

music_loop_flags = defaultdict(lambda: True)
liked_music_loop_flags = defaultdict(lambda: True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}') #Bot Name
    print(bot.user.id) #Bot ID

#Fun
@bot.tree.command()
async def lyric_search(interaction: discord.Interaction, lyrics:str):
    """Look Songs Up From Lyrics"""

    results = livesong.words_to_song(lyrics)
    song_list = "\n".join(results)
    data = {
        "type": "rich",
        "title": f'Songs With the Lyrics - "{lyrics}"',
        "description": f"{song_list}",
        "color": 0x00ff00,
        "fields": [
        ],
        "footer": {
            "text": 'Search From Genius'
        }
    }
    embed = discord.Embed.from_dict(data)
    await interaction.response.send_message(embed = embed)



@bot.tree.command()
async def start_music_updates(interaction: discord.Interaction):
    """Start displaying current music"""

    if ADMIN_ID != interaction.user.id:
        content =  "You can not use this command :P"
        await interaction.response.send_message(content=content, ephemeral=True)
        return

    if not music_loop_flags[interaction.channel.id]:
        content = "Music updates are already running."
        await interaction.response.send_message(content=content, ephemeral=True)
        return

    music_loop_flags[interaction.channel.id] = True
    await update_music_status(interaction.channel.id)

@bot.tree.command()
async def stop_music_updates(interaction: discord.Interaction):
    """Stop displaying current music"""

    if ADMIN_ID != interaction.user.id:
        content =  "You can not use this command :P"
        await interaction.response.send_message(content=content, ephemeral=True)
        return

    if not music_loop_flags[interaction.channel.id]:
        content = "Music updates are not running."
        await interaction.response.send_message(content=content, ephemeral=True)
        return

    music_loop_flags[interaction.channel.id] = False
    content = "Music updates stopped."
    await interaction.response.send_message(content=content)


@bot.tree.command()
async def start_liked_music_updates(interaction: discord.Interaction):
    """Start displaying liked music"""

    if ADMIN_ID != interaction.user.id:
        content =  "You can not use this command :P"
        await interaction.response.send_message(content=content, ephemeral=True)
        return

    if not liked_music_loop_flags[interaction.channel.id]:
        content = "Liked music updates are already running."
        await interaction.response.send_message(content=content, ephemeral=True)
        return

    liked_music_loop_flags[interaction.channel.id] = True
    await update_liked_music(interaction.channel.id)


@bot.tree.command()
async def stop_liked_music_updates(interaction: discord.Interaction):
    """Stop displaying liked music"""

    if ADMIN_ID != interaction.user.id:
        content =  "You can not use this command :P"
        await interaction.response.send_message(content=content, ephemeral=True)
        return

    if not liked_music_loop_flags[interaction.channel.id]:
        content = "Liked music updates are not running."
        await interaction.response.send_message(content=content, ephemeral=True)
        return

    liked_music_loop_flags[interaction.channel.id] = False
    content = "Liked music updates stopped."
    await interaction.response.send_message(content=content)


class SimilarMusicButton(discord.ui.Button):
    def __init__(self, song_name, artist_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.song_name = song_name
        self.artist_name = artist_name

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Finding similar music...", ephemeral=True)
        await similar_music(self.song_name, self.artist_name)
        await interaction.message.edit(view=self.view)

class MusicLyricsButton(discord.ui.Button):
    def __init__(self, song_name, artist_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.song_name = song_name
        self.artist_name = artist_name

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Finding lyrics...", ephemeral=True)
        await lyrics_button(self.song_name, self.artist_name)
        await interaction.message.edit(view=self.view)

async def lyrics_button(song_name,artist):
    lyrics = livesong.get_lyrics(song_name, artist)
    data = {
    "type": "rich",
        "title": f'Lyrics - {song_name}',
        "description": f"\n{lyrics}\n",
        "color": 0xFFD700,
        "fields": [
        ],
    "footer": {
        "text": 'Lyrics From Genius'
    }
    }
    embed = discord.Embed.from_dict(data)
    await bot.get_channel(liked_channel).send(embed=embed)


async def similar_music(song_name, artist):
    song_list = livesong.similar_songs(song_name, artist)

    data = {
    "type": "rich",
        "title": f'Similar Songs - {song_name}',
        "description": f"\n{song_list}\n",
        "color": 0xFFD700,
        "fields": [
        ],
    "footer": {
        "text": 'The majority of this document is generated by an AI'
    }
    }
    
    embed = discord.Embed.from_dict(data)
    await bot.get_channel(liked_channel).send(embed=embed)


#LIKE
async def update_liked_music(channel):
    while liked_music_loop_flags[channel]:
        # Send an update to the channel
        song_name = livesong.get_song_name()
        with open('universalV.txt', 'r') as f:
            name_hold = f.readlines()

        if name_hold[0] != song_name:
            #Get description and rest of UI shiz
            artist_name, song_name, album, thumbnail_url, duration, url,genre,desc,date,song_list = livesong.get_liked_song()

            typeAS = 'Album'
            if album == 'None':
                typeAS = 'Single'
            elif album == 'N/A':
                typeAS = 'Single'


            data = {
            "type": "rich",
                "title": f'{song_name}',
                "description": f"Description-\n{desc}\n",
                "color": 0x27c3b4,
                "fields": [
                {
                    "name": 'Artist',
                    "value": f'{artist_name}',
                    "inline": True
                },
                {
                    "name": f'{typeAS}',
                    "value": f'{album}',
                    "inline": True
                },
                {
                    "name": 'Duration',
                    "value": f'{duration}',
                    "inline": True
                },
                {
                "name": 'Genre',
                "value": f"{genre}",
                "inline": True
                },
                {
                "name": 'Release Date',
                "value": f'{date}',
                "inline": True
                },
                {
                "name": 'Similar Music',
                "value": f'Coming Soon',
                "inline": True
                }
                ],
            "thumbnail": {
            "url": f'{thumbnail_url}',
            "height": 0,
            "width": 0
            },
            "footer": {
                "text": 'The majority of this document is generated by an AI'
            },
            "url": f'{url}'
            }

            view = discord.ui.View()
            similar_music_button = SimilarMusicButton(song_name=song_name, artist_name=artist_name, style=discord.ButtonStyle.primary, label="Similar Music", custom_id="similar_music")
            show_lyrics_buttons = MusicLyricsButton(song_name=song_name, artist_name=artist_name, style=discord.ButtonStyle.primary, label="Lyrics")
            view.add_item(similar_music_button)
            view.add_item(show_lyrics_buttons)


            embed = discord.Embed.from_dict(data)
            await bot.get_channel(liked_channel).send(embed=embed,view=view)

        with open('universalV.txt', 'w') as f:
            f.write(song_name)

        await asyncio.sleep(45)
        liked_music_loop_flags[channel] = True


class LikeButton(discord.ui.Button):
    def __init__(self, video_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video_id = video_id

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Liking the song...", ephemeral=True)
        await like_song(self.video_id)  # Add 'await' here
        self.disabled = True
        await interaction.message.edit(view=self.view)

async def like_song(video_id):
    livesong.like_song_in(video_id)
    # Send an update to the channel

    song_name = livesong.get_song_name()

    with open('universalV.txt', 'r') as f:
        name_hold = f.readlines()


    if name_hold != song_name:
        artist_name, song_name, album, thumbnail_url, duration, url,genre,desc,date,song_list = livesong.get_liked_song()

        typeAS = 'Album'
        if album == 'None':
            typeAS = 'Single'
        elif album == 'N/A':
            typeAS = 'Single'


        data = {
        "type": "rich",
            "title": f'{song_name}',
            "description": f"Description-\n{desc}\n",
            "color": 0x27c3b4,
            "fields": [
            {
                "name": 'Artist',
                "value": f'{artist_name}',
                "inline": True
            },
            {
                "name": f'{typeAS}',
                "value": f'{album}',
                "inline": True
            },
            {
                "name": 'Duration',
                "value": f'{duration}',
                "inline": True
            },
            {
            "name": 'Genre',
            "value": f"{genre}",
            "inline": True
            },
            {
            "name": 'Release Date',
            "value": f'{date}',
            "inline": True
            },
            {
            "name": 'Similar Music',
            "value": f'Coming Soon',
            "inline": True
            }
            ],
        "thumbnail": {
        "url": f'{thumbnail_url}',
        "height": 0,
        "width": 0
        },
        "footer": {
            "text": 'The majority of this document is generated by an AI'
        },
        "url": f'{url}'
        }

        view = discord.ui.View()
        similar_music_button = SimilarMusicButton(song_name=song_name, artist_name=artist_name, style=discord.ButtonStyle.primary, label="Similar Music", custom_id="similar_music")
        show_lyrics_buttons = MusicLyricsButton(song_name=song_name, artist_name=artist_name, style=discord.ButtonStyle.primary, label="Lyrics")
        view.add_item(similar_music_button)
        view.add_item(show_lyrics_buttons)

        embed = discord.Embed.from_dict(data)
        await bot.get_channel(liked_channel).send(embed=embed,view=view)

        with open('universalV.txt', 'w') as f:
            f.write(song_name)


async def update_music_status(channel):
    name_hold = ""
    while music_loop_flags[channel]:
        artist_name, song_name, album, thumbnail_url, duration, url,video_id = livesong.get_current_song()
        # Send an update to the channel
        
        if name_hold != song_name:
            typeAS = 'Album'
            if album == 'None':
                typeAS = 'Single'
            elif album == 'N/A':
                typeAS = 'Single'

            data = {
            "type": "rich",
                "title": f'{song_name}',
                "description": "",
                "color": 0x27c3b4,
                "fields": [
                {
                    "name": 'Artist',
                    "value": f'{artist_name}',
                    "inline": True
                },
                {
                    "name": f'{typeAS}',
                    "value": f'{album}',
                    "inline": True
                },
                {
                    "name": 'Duration',
                    "value": f'{duration}',
                    "inline": True
                }
                ],
            "thumbnail": {
            "url": f'{thumbnail_url}',
            "height": 0,
            "width": 0
            },
            "footer": {
            "text": 'Most Recently Listened To'
            },
            "url": f'{url}'
            }

            view = discord.ui.View()
            like_button = LikeButton(video_id, label="", style=discord.ButtonStyle.green,emoji=emoji_like)
            view.add_item(like_button)

            embed = discord.Embed.from_dict(data)
            await bot.get_channel(current_channel).send(embed=embed,view=view)
        name_hold = song_name
        await asyncio.sleep(30)
        music_loop_flags[channel] = True 






#------ Sync Command ------
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context):
	synced = await ctx.bot.tree.sync()
	await ctx.send(f"Synced {len(synced)} commands {'globally'}")


bot.run(bot_key) 
