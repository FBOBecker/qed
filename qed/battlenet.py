from requests import get

try:
    with open("../.api_key") as fin:
        KEY = fin.read().strip()
except FileNotFoundError:
    try:
        with open(".api_key") as fin:
            KEY = fin.read().strip()
    except FileNotFoundError:
        with open(".api_key", "w") as fout:
            KEY = input("NO API KEY WAS FOUND. ENTER IT HERE: ")
            fout.write(KEY)


URL = "https://eu.api.battle.net/wow/{{}}?apikey={}".format(KEY)


def character(name, realm):
    url = URL.format("character/{}/{}".format(realm, name))
    return get(url)
