import os

import mafic
import nextcord
from nextcord import Interaction, Color
from nextcord.ext import commands
from datetime import datetime
from mafic import EndReason

Queue = {}


async def get_player(interaction):
    if not interaction.guild.voice_client:
        return await interaction.user.voice.channel.connect(cls=mafic.Player)
    else:
        return interaction.guild.voice_client


def add_queue(guild, track):
    if track is not None:
        list = Queue.get(guild, [])
        list.append(track)
        Queue[guild] = list


async def play_next(guild):
    player = getattr(guild, "voice_client", None)
    tracks = Queue.get(guild.id, [])
    if player is not None and len(tracks) != 0:
        await player.play(tracks[0])
        Queue[guild.id].pop(0)
        return player.current
    elif player is not None:
        await player.stop()
        await player.disconnect()
        return None


async def check_vc(interaction):
    client_vc = getattr(interaction.guild.voice_client,"channel",None)
    user_vc = getattr(interaction.user.voice, "channel", None)

    if user_vc is None:
        embed = nextcord.Embed(title="You are not in a voice channel :", color=Color.red(), timestamp=datetime.now(),
                           description="please join a voice channel to use this command")
        await interaction.send(embed=embed, ephemeral=True)
        return True
    elif client_vc != user_vc and client_vc is not None:
        embed = nextcord.Embed(title="The bot is already in use :", color=Color.red(), timestamp=datetime.now(),
                           description=f"please join <#{client_vc.id}> to use this command")
        await interaction.send(embed=embed, ephemeral=True)
        return True

    return False


@client.slash_command()
async def music(interaction: Interaction):
    pass


@music.subcommand()
async def play(interaction: nextcord.Interaction, query: str):
    if await check_vc(interaction): return

    if not interaction.guild.voice_client:
        player = await interaction.user.voice.channel.connect(cls=mafic.Player)
        await player.add_filter(mafic.Filter(volume=0.4), label='init')
    else:
        player = interaction.guild.voice_client

    tracks = await player.fetch_tracks(query)
    add_queue(interaction.guild_id, tracks[0])
    length = int(tracks[0].length / 1000)
    track_name = f"**{tracks[0].author}**\n[{tracks[0].title}]({tracks[0].uri}) ({length // 60}:{length % 60:0>2})"

    if player.current is None:
        await play_next(interaction.guild)
        embed = nextcord.Embed(title="Playing :", timestamp=datetime.now(), color=Color.green(),
                               description=f"{track_name} is now playing")
        embed.set_thumbnail(tracks[0].artwork_url)
    else:
        embed = nextcord.Embed(title="Added to queue :", timestamp=datetime.now(), color=Color.green(),
                               description=f"{track_name} has been added to queue")
        embed.set_thumbnail(tracks[0].artwork_url)

    await interaction.send(embed=embed, ephemeral=True)


@music.subcommand()
async def skip(interaction: nextcord.Interaction):
    if await check_vc(interaction): return
    track = await play_next(interaction.guild)
    length = int(track.length / 1000)
    track_name = f"**{track.author}**\n[{track.title}]({track.uri}) ({length // 60}:{length % 60:0>2})"

    embed = nextcord.Embed(title="Playing :", timestamp=datetime.now(), color=Color.green(),
                           description=f"{track_name} is now playing")
    embed.set_thumbnail(track.artwork_url)

    await interaction.send(embed=embed,ephemeral=True)

@music.subcommand()
async def stop(interaction: nextcord.Interaction):
    if await check_vc(interaction): return
    Queue[interaction.guild_id] = []
    await play_next(interaction.guild)

@music.subcommand()
async def current(interaction: nextcord.Interaction):
    player = getattr(interaction.guild, "voice_client", None)
    track = getattr(player, "current", None)

    length = int(track.length / 1000)

    embed = nextcord.Embed(title="Bot is playing :", timestamp=datetime.now(), color=Color.green(),
                           description=f"**{track.author}**\n[{track.title}]({track.uri}) ({length // 60}:{length % 60:0>2}) "
                                       f"is currently playing\n")
    embed.set_thumbnail(track.artwork_url)

    for i, q in enumerate(Queue.get(interaction.guild_id, [])):
        embed.add_field(name=f"Up next #{i + 1} :", value=f"[{q.title}]({track.uri})", inline=False)

    await interaction.send(embed=embed, ephemeral=True)


@client.listen()
async def on_track_end(event: mafic.TrackEndEvent):
    print(EndReason.REPLACED)
    if event.reason != EndReason.REPLACED:

        await play_next(event.player.guild)

@client.event
async def on_voice_state_update(member, before, after):
    guild = getattr(getattr(before,"channel",None),"guild",None)
    player = getattr(guild,"voice_client",None)

    if guild is not None and player is not None and after.channel is None and member == client.user:
        Queue[guild.id] = []