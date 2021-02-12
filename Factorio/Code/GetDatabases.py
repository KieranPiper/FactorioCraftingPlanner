import sqlite3
from sqlite3 import Error

from typing import Dict, List


def connect_to_database(vanilla: bool = True, mods: List[str] = None, modpacks: List[str] = None) -> \
        Dict[str, sqlite3.Connection] or None:
    """
    Connects to databases based on what type of game is being played.
    :param vanilla: True, False; Whether or not the game is vanilla.
    :param mods: [str]; What mods are being used.
    :param modpacks: [str]; What modpacks are being used.
    :return: Dict[Database Name: Connection object] or None
    """

    # If there are any mods or modpacks selected, automatically turn vanilla to False.
    if mods is not None or modpacks is not None:
        vanilla = False

    # If the game is vanilla, just get the vanilla database and send it back to
    if vanilla:
        try:
            conn = sqlite3.connect("..\\Vanilla\\Vanilla.db")
            return {"Vanilla": conn}
        except Error as e:
            print(e)
            return None

    else:
        # First get any mods from the modpacks (if there are any) so that we can discount the mod if it is added
        # into the mods list. This prevents bringing up recipes which may have been changed in a modpack due to
        # the mod database also being loaded.
        mods_to_remove = []
        databases = {}

        if modpacks is not None:
            mods_to_remove += _get_mods(modpacks)
            databases.update(_get_modpack_database(modpacks))

        if mods is not None:
            for mod in mods:
                if mod in mods_to_remove:
                    mods.remove(mod)

            databases.update(_get_mod_database(mods))

        return databases


def _get_mods(*modpacks: List[str]) -> List[str] or List[None]:
    """
    Gets all the mods from multiple modpacks.
    :param modpacks: List[str]; The modpacks to get.
    :return: List[str] or List[None]
    """

    mods = []
    for modpack in modpacks:
        try:
            with open(f"..\\Modpacks\\{modpack}\\mods.txt") as f:
                for row in f:
                    if row not in ["\n", " ", ""]:
                        mods.append(row.strip())

        except FileNotFoundError:
            continue

    return mods


def _get_mod_database(mods: List[str]) -> Dict[str, sqlite3.Connection] or Dict[None]:
    """
    Gets the databases for multiple mods.
    :param mods: List[str]; The mods to get
    :return: Dict[str, Connection object] or Dict[None]
    """
    mod_databases = {}
    for mod in mods:
        try:
            mod_databases[mod.capitalize()] = sqlite3.connect(f"..\\Mods\\{mod.capitalize()}.db")
        except Error:
            continue

    return mod_databases


def _get_modpack_database(modpacks: List[str]) -> Dict[str, sqlite3.Connection] or Dict[None]:
    """
    Gets the databases for multiple modpacks.
    :param modpacks: List[str]; The modpacks to get.
    :return: Dict[str, Connection object]
    """
    modpack_databases = {}
    for modpack in modpacks:
        print(modpack)
        try:
            modpack_databases[modpack.capitalize()] = sqlite3.connect(f"..\\Modpacks\\{modpack.capitalize()}\\"
                                                                      f"{modpack.capitalize()}.db")
        except Error:
            continue
    return modpack_databases
