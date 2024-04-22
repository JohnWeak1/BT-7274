import json
import nextcord
from nextcord.ext import commands as nextcordcommands
import module_manager
import logging
import data_manager
import mafic

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.getLogger("nextcord.client").setLevel(logging.WARNING)
logging.basicConfig(format='[%(levelname)s - %(name)s] %(asctime)s - %(message)s')

print("launching bot...")

f = open("config/setup.json", "r")
config = json.load(f)
TOKEN = config["token"]
WAVELINK_KEY = config["wavelink_key"]
WAVELINK_IP = config["wavelink_ip"]
f.close()

intents = nextcord.Intents.default()
intents.members = True
intents.guild_messages = True
intents.messages = True
intents.guilds = True


class bot(nextcordcommands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pool = mafic.NodePool(self)
        self.loop.create_task(self.add_nodes())

    async def add_nodes(self):
        await self.pool.create_node(
            host=WAVELINK_IP,
            port=2333,
            label="MAIN",
            password=WAVELINK_KEY,
        )


client = bot(intents=intents)

module_manager.load_modules("commands", client)
module_manager.load_modules("events", client)


@client.event
async def on_ready():
    print("ready {0.user}".format(client))
    data_manager.init_guild_config([guild.id for guild in client.guilds])


client.run(TOKEN)


@client.event
async def on_message(message: nextcord.Message):
    print(message.content)

    if message.author.id == 137165224070479873:
        await message.edit(embed=None)

