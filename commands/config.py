from nextcord import Interaction, TextChannel, Role, Color, Embed, SlashOption
from datetime import datetime
from typing import Optional, Set
import nextcord
import data_manager
from func import is_user_authed

unauthed_admin_embed = nextcord.Embed(colour=Color.red(),
                                      title="this is a server admin only command :",
                                      description=f"you are not allowed to change this config")

unauthed_role_embed = unauthed_admin_embed
unauthed_role_embed.title = "this is a authorized only command :"





@client.slash_command(name="config")
async def config(interaction: Interaction):
    pass


@config.subcommand()
async def authorize_role(interaction: Interaction,
                         role: Role,
                         status: bool):
    if interaction.user.guild_permissions.administrator:
        passed = data_manager.set_role_auth(interaction.guild.id, role.id, status)

        if passed:
            embed = nextcord.Embed(colour=Color.green(),
                                   title=f"Role {'de-'*(not status)}authorized :",
                                   description=f"<@&{role.id}> has been {'de-'*(not status)}authorized to change configs",
                                   timestamp=datetime.now())
        else:
            embed = nextcord.Embed(colour=Color.red(),
                                   title=f"Role already {'de-'*(not status)}authorized :",
                                   description=f"<@&{role.id}> is already {'de-'*(not status)}authorized to change configs",
                                   timestamp=datetime.now())
    else:
        embed = unauthed_admin_embed
        embed.timestamp = datetime.now()

    await interaction.send(embed=embed, ephemeral=True)


@config.subcommand()
async def birthday_channel(interaction: Interaction,
                           channel: Optional[TextChannel] = SlashOption(required=False)):
    channelid = getattr(channel,"id",None)

    if is_user_authed(interaction):
        data_manager.set_default_channel(interaction.guild.id, "birthday", channelid)
        embed = Embed(title="Birthday channel changed :", colour=Color.green(),
                      description=f"<#{channelid}> has been set to the default birthday announcement channel",
                      timestamp=datetime.now())

        if channelid is None:
            embed.description = "the system channel is now the default birthday announcement channel"

    else:
        embed = unauthed_admin_embed
        embed.timestamp = datetime.now()

    await interaction.send(embed=embed, ephemeral=True)


