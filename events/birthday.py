import schedule
import data_manager
import nextcord
from datetime import datetime
from func import run_continuously
import asyncio
from aiocron import crontab
import time

@crontab('0 0 * * *')
async def check_birthday():
    now = datetime.now()


    birthdays = data_manager.get_current_birthday(now.day, now.month)

    for birthday in birthdays:
        for guild_id in birthday["guild_ids"]:

            channel_id = data_manager.get_default_channel(guild_id, "birthday")
            if channel_id is not None:
                def_channel = client.get_guild(guild_id).get_channel(channel_id)
            else:
                def_channel = client.get_guild(guild_id).system_channel

            await def_channel.send("@everyone", embed=nextcord.Embed(title="Happy birthday !",
                                                                     description=f"today is <@{birthday['user_id']}>'s birthday !",
                                                                     timestamp=now))