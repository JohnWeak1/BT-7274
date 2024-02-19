import nextcord
from datetime import datetime
import data_manager

@client.event
async def on_member_remove(member):
    channel = member.guild.system_channel

    data_manager.remove_user_birthday(member.id,member.guild.id)

    embed = nextcord.Embed(title=f"Goodbye {member.name}",
                           description="We hope you enjoyed your stay",
                           color=0xff0000,
                           timestamp=datetime.now())

    await channel.send(embed=embed)


@client.event
async def on_member_join(member):
    channel = member.guild.system_channel

    embed = nextcord.Embed(title=f"Welcome, {member.name}",
                           description=f"Welcome to : {member.guild.name}",
                           color=0x00ff26,
                           timestamp=datetime.now())

    await channel.send(embed=embed)