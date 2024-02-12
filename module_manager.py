import os
import importlib
import nextcord
import data_manager
from datetime import datetime
from nextcord import Color

def load_modules(dir, client):
    print(f"loading : {dir} modules")
    cmd_mods = os.listdir(dir)
    cmd_mods = [f for f in cmd_mods if f.endswith('.py')]
    modules_data = {}
    for cmd_mod in cmd_mods:
        script_path = os.path.join(dir, cmd_mod)

        module_name = f"{script_path[:-3]}"

        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        module.client = client
        spec.loader.exec_module(module)

        modules_data[module_name] = getattr(module, "module_data", None)
        print(f"    [OK] {module_name}")

    return modules_data


async def is_module_enabled(module_name,guild,interaction=None):
    is_enabled = data_manager.get_module_setting(guild).get(module_name, False)
    if interaction is not None and not is_enabled:
        embed = nextcord.Embed(colour=Color.red(),
                               title="Module is disabled",
                               description=f"the module has been disabled by a moderator",
                               timestamp=datetime.now())

        await interaction.send(embed=embed, ephemeral=True)
    return is_enabled


