from nextcord import Interaction

@client.slash_command(guild_ids=[521256432058761226, 717100212027392080])
async def ping(interaction: Interaction):
    await interaction.send("pong")
