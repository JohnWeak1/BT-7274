import datetime
from datetime import datetime as dt
import json
import supabase
from func import get_attr

f = open("./config/setup.json", "r")
conf = json.load(f)
f.close()

database = supabase.create_client(conf["db_url"], conf["db_key"])

def init_guild_config(guild_ids):

    for guild_id in guild_ids:
        database.table("enabled_modules").upsert({'guild_id':guild_id}).execute()


def cell_array(table, column, col_eq, equal, value, add=True):
    values = database.table(table).select(column).eq(col_eq, equal).maybe_single().execute()

    values = set(get_attr(get_attr(values,"data",None),column,[]))
    passed = (value in values) != add
    values.add(value) if add else values.discard(value)

    if passed: database.table(table).upsert({f"{col_eq}": equal, f"{column}": list(values)}).execute()

    return passed


def set_user_birthday(user_id, day, month, guild):
    try:
        Date = datetime.datetime(2004, day=day, month=month)
    except ValueError:
        return None

    cell_array("user_birthdates", "guild_ids", "user_id", user_id, guild)

    database.table('user_birthdates').upsert(
        {'user_id': user_id, 'day': day, 'month': month}).execute()
    return Date

def get_current_birthday(day,month):
    data = database.table('user_birthdates').select('*').eq('month', month).eq('day',day).execute()

    return get_attr(data,"data",[])

def get_user_birthday(user_id, guild_id):
    data = database.table('user_birthdates').select('*').eq('user_id', user_id).maybe_single().execute()

    print(get_attr(get_attr(data, "data", None), "guild_ids", []))

    if guild_id in get_attr(get_attr(data, "data", None), "guild_ids", []):
        return get_attr(data, "data", None)
    return None


def get_user_next_birthday(user_id,guild_id):
    bd = get_user_birthday(user_id,guild_id)

    if bd is None: return None

    bd_datetime = dt(2004, month=bd["month"], day=bd["day"])
    cur_datetime = dt.now().replace(year=2004)

    return bd_datetime.replace(year=dt.now().year + (cur_datetime > bd_datetime))


def set_default_channel(server_id, column, channel_id):
    database.table("default_channels").upsert({"guild_id": server_id, column: channel_id}).execute()


def get_default_channel(server_id, column):
    data = database.table("default_channels").select(column).eq("guild_id", server_id).maybe_single().execute()

    return get_attr(get_attr(data, "data", None), "birthday", None)


def set_role_auth(guild_id, role_id, status):
    return cell_array("authed_roles", "role_ids", "guild_id", guild_id, role_id, status)


def get_role_auth(guild_id):
    data = database.table("authed_roles").select("role_ids").eq("guild_id", guild_id).maybe_single().execute()

    return get_attr(get_attr(data, "data", None), "role_ids", None)


def are_roles_authed(server_id, role_ids):
    data = get_role_auth(server_id)

    if data is None: return False

    authed_roles = set(data)
    return len(authed_roles.intersection(set(role_ids))) != 0


def get_module_setting(server_id):
    data = database.table("enabled_modules").select("*").eq("guild_id",server_id).maybe_single().execute()

    return get_attr(data,"data",{})

def get_modules():
    data = database.table("enabled_modules").select("*").eq("guild_id",1).single().execute().data

    return list(data.keys())

print(get_current_birthday(12,2))