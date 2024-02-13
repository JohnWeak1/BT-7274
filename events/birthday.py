from datetime import datetime
import nextcord
from aiocron import crontab
import data_manager


@crontab('0 0 * * *')
async def check_birthday():
    now = datetime.now()


    birthdays = data_manager.get_current_birthday(now.day, now.month)

    for bd in birthdays:

        channel_id = data_manager.get_default_channel(bd["guild_id"], "birthday")
        if channel_id is not None:
            def_channel = client.get_guild(bd["guild_id"]).get_channel(channel_id)
        else:
            def_channel = client.get_guild(bd["guild_id"]).system_channel

        await def_channel.send("@everyone", embed=nextcord.Embed(title="Happy birthday !",
                                                                 description=f"today is <@{bd['user_id']}>'s birthday !",
                                                                     timestamp=now))