import time

import nextcord
from nextcord import Interaction, SlashOption, Color
from datetime import datetime
import data_manager as data_manager
from module_manager import is_module_enabled
from func import is_user_authed


def format_date(date):
    suffix = ["st", "nd", "rd", "th"][min(date.day % 10 - 1, 3)]
    return f"{date.day}{suffix} of {date.strftime('%B')}"


async def birthday_cmd(interaction, member):
    bd = data_manager.get_user_birthday(member.id, interaction.guild_id)

    if bd is not None:
        next_bd = data_manager.get_next_birthday(bd["day"], bd["month"])

        unix = int(time.mktime(next_bd.timetuple()))
        embed = nextcord.Embed(colour=Color.green(), timestamp=datetime.now(),
                               title=f"Birthday :",
                               description=f"<@{member.id}>'s birthday is the {format_date(next_bd)} \n(<t:{unix}:R>)")

    else:
        embed = nextcord.Embed(colour=Color.red(), timestamp=datetime.now(),
                               title=f"No birthdate set :",
                               description=f"{member.display_name} doesn't seem to have a birthday set")
    embed.set_thumbnail(member.avatar.url)

    await interaction.send(embed=embed, ephemeral=True)


@client.slash_command()
async def birthday(interaction: Interaction):
    pass


@birthday.subcommand(description="set your birthday", name="set")
async def bd_set(interaction: Interaction,
                 day: int = SlashOption(name="day", min_value=1, max_value=31),
                 month: int = SlashOption(name="month", min_value=1, max_value=12)):
    is_enabled = await is_module_enabled("birthday", interaction.guild_id, interaction)
    if not is_enabled: return

    response = data_manager.set_user_birthday(interaction.user.id, day, month, interaction.guild_id)

    if response is not None:
        embed = nextcord.Embed(colour=Color.green(),
                               title="Birthday set successfully",
                               description=f"your birthday has been set to the {format_date(response)}",
                               timestamp=datetime.now())
    else:
        embed = nextcord.Embed(colour=Color.red(),
                               title="Birthday set error",
                               description=f"the birthdate provided is invalid",
                               timestamp=datetime.now())

    await interaction.send(embed=embed, ephemeral=True)


@birthday.subcommand(description="get someone's birthday", name="get")
async def bd_get(interaction: Interaction,
                 member: nextcord.Member):
    is_enabled = await is_module_enabled("birthday", interaction.guild_id, interaction)
    if not is_enabled: return
    await birthday_cmd(interaction, member)


@birthday.subcommand(description="set someone else's birthday", name="force_set")
async def bd_force_set(interaction: Interaction,
                       member: nextcord.Member,
                       day: int = SlashOption(name="day", min_value=1, max_value=31),
                       month: int = SlashOption(name="month", min_value=1, max_value=12)):
    is_enabled = await is_module_enabled("birthday", interaction.guild_id, interaction)
    if not is_enabled: return
    if not await is_user_authed(interaction, False): return

    response = data_manager.set_user_birthday(member.id, day, month, interaction.guild_id)

    if response is not None:
        embed = nextcord.Embed(colour=Color.green(),
                               title="Birthday set successfully",
                               description=f"<@{member.id}> birthday has been set to the {format_date(response)}",
                               timestamp=datetime.now())
    else:
        embed = nextcord.Embed(colour=Color.red(),
                               title="Birthday set error",
                               description=f"the birthdate provided is invalid",
                               timestamp=datetime.now())

    await interaction.send(embed=embed, ephemeral=True)


@birthday.subcommand(description="get the next birthdays", name="next")
async def bd_get_next(interaction: Interaction):
    is_enabled = await is_module_enabled("birthday", interaction.guild_id, interaction)
    if not is_enabled: return

    data = data_manager.get_guild_birthdays(interaction.guild_id)

    if len(data) > 0:
        embed = nextcord.Embed(title="Next birthdays :", color=Color.green(), timestamp=datetime.now())
        next_bds = [{'user': d['user_id'], 'date': data_manager.get_next_birthday(d["day"], d["month"])} for d in data]
        next_bds = sorted(next_bds, key=lambda d: d['date'])
        for bd in next_bds:
            unix = int(time.mktime(bd['date'].timetuple()))
            embed.add_field(name=" ", value=f"<@{bd['user']}> : <t:{unix}:D>(<t:{unix}:R>)", inline=False)
    else:
        embed = nextcord.Embed(title="No next birthdays :", color=Color.red(), timestamp=datetime.now(),
                               description="nobody has set their birthdays on this server")

    await interaction.send(embed=embed, ephemeral=True)


@client.user_command(name="birthday")
async def bd_usr_get(interaction: Interaction, member: nextcord.Member):
    is_enabled = await is_module_enabled("birthday", interaction.guild_id, interaction)
    if not is_enabled: return
    await birthday_cmd(interaction, member)
