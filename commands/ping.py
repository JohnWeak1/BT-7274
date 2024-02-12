from nextcord import Interaction

@client.slash_command()
async def ping(interaction: Interaction):
    await interaction.send("pong")
