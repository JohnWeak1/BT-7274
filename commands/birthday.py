import time

import nextcord
from nextcord import Interaction, SlashOption, Color
from datetime import datetime
import data_manager as data_manager
from module_manager import is_module_enabled

print("test")

def format_date(date):
    suffix = ["st", "nd", "rd", "th"][min(date.day % 10 - 1, 3)]
    return f"{date.day}{suffix} of {date.strftime('%B')}"


async def birthday_cmd(interaction, member):
    next_bd = data_manager.get_user_next_birthday(member.id, interaction.guild_id)
    print(next_bd)
    if next_bd is not None:
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


@client.slash_command(guild_ids=[521256432058761226, 717100212027392080])
async def birthday(interaction: Interaction):
    pass


@birthday.subcommand(description="set your birthdate", name="set")
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


@birthday.subcommand(description="get someone's birth day", name="get")
async def bd_get(interaction: Interaction,
                 member: nextcord.Member):
    is_enabled = await is_module_enabled("birthday", interaction.guild_id, interaction)
    if not is_enabled: return
    await birthday_cmd(interaction, member)


@client.user_command(name="birthday")
async def bd_usr_get(interaction: Interaction, member: nextcord.Member):
    is_enabled = await is_module_enabled("birthday", interaction.guild_id, interaction)
    if not is_enabled: return
    await birthday_cmd(interaction, member)
