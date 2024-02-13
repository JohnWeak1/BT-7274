import threading
import time
import data_manager
import nextcord
from nextcord import Color

def get_attr(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    else:
        return getattr(obj, key, default)

async def is_user_authed(interaction,silent=True):
    unauthed_admin_embed = nextcord.Embed(colour=Color.red(),
                                          title="this is a server admin only command :",
                                          description=f"you are not allowed to change this config")

    unauthed_role_embed = unauthed_admin_embed
    unauthed_role_embed.title = "this is a authorized only command :"
    embeds = [unauthed_admin_embed,unauthed_role_embed]

    is_authed = data_manager.are_roles_authed(interaction.guild.id,
                                              [role.id for role in interaction.user.roles])
    is_admin = interaction.user.guild_permissions.administrator
    if not silent and (not (is_authed or is_admin)):
        await interaction.send(embed=embeds[int(not is_admin)],ephemeral=True)

    return is_authed or is_admin