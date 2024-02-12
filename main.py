import json
from datetime import datetime
import nextcord
from nextcord.ext import commands as nextcordcommands
import module_manager
import logging
import data_manager
import schedule

logging.getLogger("httpx").setLevel(logging.WARNING)

print("launching bot...")

f = open("config/setup.json", "r")
TOKEN = json.load(f)["token"]
f.close()

intents = nextcord.Intents.default()
intents.members = True
intents.guild_messages = True
intents.messages = True
intents.guilds = True

client = nextcordcommands.Bot(intents=intents)

module_manager.load_modules("commands", client)
module_manager.load_modules("events", client)

@client.event
async def on_ready():
    print("ready {0.user}".format(client))
    data_manager.init_guild_config([guild.id for guild in client.guilds])




client.run(TOKEN)
