import os

import mafic
import nextcord
from nextcord import Interaction, Color
from nextcord.ext import commands
from datetime import datetime

Queue = {}
Players = {}


async def get_player(interaction):
    if not interaction.guild.voice_client:
        return await interaction.user.voice.channel.connect(cls=mafic.Player)
    else:
        return interaction.guild.voice_client

def add_queue(guild,track):
    if track is not None:
        list = Queue.get(guild,[])
        list.append(track)
        Queue[guild] = list

async def play_next(guild):
    player = getattr(guild,"voice_client",None)
    tracks = Queue.get(guild.id,[])
    if player is not None and len(tracks) != 0:
        await player.play(tracks[0])
        Queue[guild.id].pop(0)
    elif player is not None:
        await player.stop()

@client.slash_command()
async def music(interaction: Interaction):
    pass


@music.subcommand()
async def play(interaction: nextcord.Interaction, query: str):
    if not interaction.guild.voice_client:
        player = await interaction.user.voice.channel.connect(cls=mafic.Player)
        await player.add_filter(mafic.Filter(volume=0.4), label='init')
    else:
        player = interaction.guild.voice_client



    tracks = await player.fetch_tracks(query)
    add_queue(interaction.guild_id,tracks[0])
    len = int(tracks[0].length / 1000)
    embed = nextcord.Embed(title="Playing :",timestamp=datetime.now(),color=Color.green(),
                           description=f"**{tracks[0].author}**\n[{tracks[0].title}]({tracks[0].uri}) ({len // 60}:{len % 60}) is now playing")
    embed.set_thumbnail(tracks[0].artwork_url)

    if player.current is None: await play_next(interaction.guild)
    await interaction.send(embed=embed,ephemeral=True)

@music.subcommand()
async def next(interaction: nextcord.Interaction):
    await play_next(interaction.guild)

@client.listen()
async def on_track_end(event: mafic.TrackEndEvent):
    await play_next(event.player.guild)

