import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import IntegrityError

from typing import Dict, List, Tuple


# region Machine Table
def create_machine_table(database: sqlite3.Connection, override_existing: bool = False):
    """
    Creates a new table inside a database for machines.
    :param database: Connection object; The database to add the table to.
    :param override_existing: bool; whether or not to override an existing table.
    :return:
    """
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        }
    ])
    if override_existing:
        drop_table = """
        DROP TABLE Machines;
        """
        try:
            database.cursor().execute(drop_table)
            database.commit()
        except Error as e:
            print(e)

    sql = """
    CREATE TABLE IF NOT EXISTS Machines (
        Machine_ID
            INTEGER
            PRIMARY KEY,
        Machine_Name
            TEXT
            NOT NULL
            UNIQUE,
        Machine_Crafting_Speed
            REAL
            NOT NULL
            CHECK (Machine_Crafting_Speed >= 0),
        Machine_Module_Slots 
            INTEGER
            NOT NULL
            CHECK (Machine_Module_Slots >= 0) 
            DEFAULT (0),
        Machine_Max_Energy_Consumption_KW
            REAL
            NOT NULL
            CHECK (Machine_Max_Energy_Consumption_KW >= 0) 
            DEFAULT (0.0),
        Machine_Idle_Energy_Consumption_KW
            REAL
            NOT NULL
            CHECK (Machine_Idle_Energy_Consumption_KW >= 0) 
            DEFAULT (0.0),
        Machine_Energy_Type
            TEXT
            NOT NULL
            DEFAULT Electric
            CHECK (Machine_Energy_Type IN ("Electric", "Item", "Liquid")),
        Machine_Pollution_Per_Minute
            REAL
            NOT NULL
            CHECK (Machine_Pollution_Per_Minute >= 0)
        );
    """
    try:
        database.cursor().execute(sql)
    except Error as e:
        print(e)


def add_machine(database: sqlite3.Connection, machine_name: str, craft_speed: float, module_slots: int,
                max_energy_consumption: float, idle_energy_consumption: float, energy_consumption_type: str,
                pollution: float):
    """
    Adds a machine to the database.
    :param database: Connection object; the database to add the machine to.
    :param machine_name: str; The name of the machine.
    :param craft_speed: float; The crafting speed of the machine.
    :param module_slots: int; The number of modules which can be in the machine.
    :param max_energy_consumption: float; The power consumption of the machine in KW while active.
    :param idle_energy_consumption: float; The power consumption of the machine in KW while idle.
    :param energy_consumption_type: str; The type of energy consumed (Electric, Item, Liquid).
    :param pollution: float; The pollution the machine outputs per minute while active.
    :return:
    """
    _check_types([
        {
            "Argument Name": "machine_name",
            "Value Supplied": machine_name,
            "Type": str
        },
        {
            "Argument Name": "craft_speed",
            "Value Supplied": craft_speed,
            "Type": float
        },
        {
            "Argument Name": "module_slots",
            "Value Supplied": module_slots,
            "Type": int
        },
        {
            "Argument Name": "max_energy_consumption",
            "Value Supplied": max_energy_consumption,
            "Type": float
        },
        {
            "Argument Name": "idle_energy_consumption",
            "Value Supplied": idle_energy_consumption,
            "Type": float
        },
        {
            "Argument Name": "energy_consumption_type",
            "Value Supplied": energy_consumption_type,
            "Type": str
        },
        {
            "Argument Name": "pollution",
            "Value Supplied": pollution,
            "Type": float
        }
    ])

    sql = """
    INSERT INTO Machines(
        Machine_Name,
        Machine_Crafting_Speed,
        Machine_Module_Slots,
        Machine_Max_Energy_Consumption_KW,
        Machine_Idle_Energy_Consumption_KW,
        Machine_Energy_Type,
        Machine_Pollution_per_Minute
        )
    Values(?,?,?,?,?,?,?);
    """
    try:
        database.cursor().execute(sql, (machine_name, craft_speed, module_slots, max_energy_consumption,
                                        idle_energy_consumption, energy_consumption_type.capitalize(), pollution))
        database.commit()
    except Error as e:
        print(e)
    except IntegrityError as e:
        print(e)


def get_machine(database: sqlite3.Connection, machine_id: int = None, machine_name: str = None) -> \
        List[Dict[str, str or float]]:
    """
    Gets a machine.
    
    :param database: Connection object; The database to search in.
    :param machine_id: int; The ID of the machine if known. Defaults to None.
    :param machine_name: str; The name of the machine if known. Defaults to None.
    
    :return: Dict[str, str or float]
    """
    # region Check Types
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        }
    ])
    if machine_id is not None:
        _check_types([
            {
                "Argument Name": "machine_id",
                "Value Supplied": machine_id,
                "Type": int
            }
        ])

    if machine_name is not None:
        _check_types([
            {
                "Argument Name": "machine_name",
                "Value Supplied": machine_name,
                "Type": str
            }
        ])
    # endregion

    if machine_id is not None:
        try:
            sql = f"""
            SELECT * 
            FROM Machines 
            WHERE Machine_ID={machine_id}
            """
            cur = database.cursor()
            cur.execute(sql)

            row = cur.fetchall()
            machine_id, machine_name, crafting_speed, module_slots, max_energy, idle_energy, energy_consumption_type, \
                pollution = row[0]

            return [{
                "Machine_id": machine_id,
                "Machine_Name": machine_name,
                "Crafting_Speed": crafting_speed,
                "Module_Slots": module_slots,
                "Max_Energy_Consumption": max_energy,
                "Idle_Energy_Consumption": idle_energy,
                "Energy_Consumption_Type": energy_consumption_type,
                "Pollution": pollution
            }]

        except Error as e:
            print(e)
        except ValueError as e:
            print(e)

    if machine_name is not None:
        sql = f"""
        SELECT *
        FROM Machines
        WHERE Machine_Name LIKE "%{machine_name}%"
        """

        cur = database.cursor()
        cur.execute(sql)

        rows = cur.fetchall()
        machines = []

        for row in rows:
            machine_id, machine_name, crafting_speed, module_slots, max_energy, idle_energy, energy_consumption_type, \
                pollution = row

            machines.append({
                "Machine_id": machine_id,
                "Machine_Name": machine_name,
                "Crafting_Speed": crafting_speed,
                "Module_Slots": module_slots,
                "Max_Energy_Consumption": max_energy,
                "Idle_Energy_Consumption": idle_energy,
                "Energy_Consumption_Type": energy_consumption_type,
                "Pollution": pollution
            })

        return machines


def get_all_machines(database: sqlite3.Connection) -> List[Tuple[str, str or int or float]]:
    """
    Gets all the machines from the database.
    
    :param database: Connection object; The database to get all the machines from.
    
    
    :return: List[Dict[str, str or int or float]]
    """
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        }
    ])

    cur = database.cursor()
    cur.execute("SELECT * FROM Machines")
    return cur.fetchall()


def update_machine(database: sqlite3.Connection, machine_id: int = None, machine_name: str = None,
                   prompt_user_on_multiple_match: bool = True, **new_values: Dict[str, str or int or float]):
    """
    Updates a machines information.
    
    :param database: Connection object; The database the machine is in.
    :param machine_id: int; The id of the machine if known. Defaults to None.
    :param machine_name: str; The machine name if known. If multiple machines with the name given arises, will prompt
    user to input the one they want. Defaults to None.
    :param prompt_user_on_multiple_match: bool; Whether or not to prompt users to input the machine they want if
    multiple machines with the same name given exists. Defaults to True.
    :param new_values: Dict[str, str or int or float]; The new values for the machine)

    :return:
    """
    # region Type Checks
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        },
        {
            "Argument Name": "prompt_user_on_multiple_match",
            "Value Supplied": prompt_user_on_multiple_match,
            "Type": bool
        },
        {
            "Argument Name": "new_values",
            "Value Supplied": new_values,
            "Type": dict
        }
    ])

    if machine_id is not None:
        _check_types([
            {
                "Argument Name": "machine_id",
                "Value Supplied": machine_id,
                "Type": int
            }
        ])
    if machine_name is not None:
        _check_types([
            {
                "Argument Name": "machine_name",
                "Value Supplied": machine_name,
                "Type": str
            },
        ])
    # endregion

    # First, assign machine the output of get_machine, then check it's length
    if len(machine := get_machine(database, machine_id=machine_id, machine_name=machine_name)) > 1:
        if prompt_user_on_multiple_match:
            for item in machine:
                print(item)

            while ((machine_wanted := input("Please put the name of the machine you want to edit: ")) not in (
                    ([item["Machine_Name"] for item in machine]) or ["Exit", "Stop", "Quit"])):
                for item in machine:
                    print(item)

            for item in machine:
                if item["Machine_Name"] == machine_wanted:
                    machine_wanted = item

        else:
            machine_wanted = machine[0]

    elif len(machine) == 1:  # This works due to the fact that the := operator assigns the machine variable to the
        # output of get_machine.
        machine_wanted = machine[0]

    else:
        machine_wanted = None

    if machine_wanted is not None and new_values != {}:
        for key in new_values.keys():
            if key in machine_wanted.keys():
                machine_wanted[key] = new_values[key]

        sql = """
        UPDATE Machines
        SET Machine_Name = ?,
            Machine_Crafting_Speed = ?,
            Machine_Module_Slots = ?,
            Machine_Max_Energy_Consumption_KW = ?,
            Machine_Idle_Energy_Consumption_KW = ?,
            Machine_Energy_Type = ?,
            Machine_Pollution_Per_Minute = ?
        Where Machine_ID = ?
        """
        database.cursor().execute(sql, (machine_wanted["Machine_Name"],
                                        machine_wanted["Crafting_Speed"],
                                        machine_wanted["Module_Slots"],
                                        machine_wanted["Max_Energy_Consumption"],
                                        machine_wanted["Idle_Energy_Consumption"],
                                        machine_wanted["Energy_Consumption_Type"],
                                        machine_wanted["Pollution"],
                                        machine_wanted["Machine_id"]
                                        ))
        database.commit()


# endregion

# region Recipes
def create_recipe_table(database: sqlite3.Connection, override_existing: bool = False):
    """
    Creates a new table inside a database for recipes
    :param database: Connection object; The database to add the table to.
    :param override_existing: bool; Whether or not to override an existing table.
    :return:

    """
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        },
        {
            "Argument Name": "override_existing",
            "Value Supplied": override_existing,
            "Type": bool
        }
    ])

    if override_existing:
        drop_table = """
        DROP TABLE Recipes
        """
        database.cursor().execute(drop_table)
        database.commit()

    sql = """
    CREATE TABLE IF NOT EXISTS Recipes (
        Recipe_ID 
            INTEGER
            PRIMARY KEY,
        Recipe_Items_Used
            TEXT
            NOT NULL,
        Recipe_Products
            TEXT
            NOT NULL,
        Recipe_Craft_Time_Seconds
            REAL
            NOT NULL
            CHECK (Recipe_Craft_Time_Seconds >= 0),
        Recipe_Machine_Used
            TEXT
            NOT NULL,
        Recipe_Modules_Allowed
            TEXT
            NOT NULL
    );
    """
    database.cursor().execute(sql)
    database.commit()


def add_recipe(database: sqlite3.Connection, recipe_requirements: List[Dict[str, str]],
               recipe_products: List[Dict[str, str]], craft_time: float, machines: List[str], modules: List[str]):
    """
    Adds a recipe to the database.
    
    :param database: Connection object; The database.
    :param recipe_requirements: List[Dict[str, str or float]]; The requirements for the recipe. Dict: {"Name": Amount} 
    :param recipe_products: List[Dict[str, str or float]]; The products made by the recipe. Dict: {"Name": Amount}
    :param craft_time: float; The amount of time in seconds the recipe takes to craft.
    :param machines: List[Dict[str, str]]; The machines which the recipe can be crafted in.
    :param modules: List[str]; The modules which can be used in the recipe (Speed, Productivity, Efficiency).
    
    :returns:
    """

    # region Type Check
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        },
        {
            "Argument Name": "recipe_requirements",
            "Value Supplied": recipe_requirements,
            "Type": list
        },
        {
            "Argument Name": "recipe_products",
            "Value Supplied": recipe_products,
            "Type": list
        },
        {
            "Argument Name": "craft_time",
            "Value Supplied": craft_time,
            "Type": float
        },
        {
            "Argument Name": "machines",
            "Value Supplied": machines,
            "Type": list
        },
        {
            "Argument Name": "modules",
            "Value Supplied": modules,
            "Type": list
        }])
    _check_type_of_children([
        {
            "Argument Name": "recipe_requirements",
            "Value Supplied": recipe_requirements,
            "Type": dict
        },
        {
            "Argument Name": "recipe_products",
            "Value Supplied": recipe_products,
            "Type": dict
        },
        # {
        #     "Argument Name": "machines",
        #     "Value Supplied": machines,
        #     "Type": str
        # },
        # {
        #     "Argument Name": "modules",
        #     "Value Supplied": modules,
        #     "Type": str
        # }
    ])
    # endregion

    sql = """
    INSERT INTO Recipes (
        Recipe_Items_Used,
        Recipe_Products,
        Recipe_Craft_Time_Seconds,
        Recipe_Machine_Used,
        Recipe_Modules_Allowed
        )
    Values(?,?,?,?,?);
    """

    try:
        database.cursor().execute(sql, (str(recipe_requirements), str(recipe_products), float(craft_time),
                                        str(machines), str(modules)))
        database.commit()
    except Error as e:
        print(e)
    except IntegrityError as e:
        print(e)


def get_recipe(database: sqlite3.Connection, recipe_id: int = None, recipe_product: str = None) -> List[Dict[str, str or
                                                                                                             float]]:
    """
    Gets a recipe.

    :param database: Connection object; The database.
    :param recipe_id: int; The id of the recipe, if known. Defaults to None.
    :param recipe_product: str; The product which you are making. Defaults to None.

    :return: List[Dict[str, str or float]].
    """
    # region Type Checks
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        }
    ])

    if recipe_id is not None:
        _check_types([
            {
                "Argument Name": "recipe_id",
                "Value Supplied": recipe_id,
                "Type": int
            }
        ])

    if recipe_product is not None:
        _check_types([
            {
                "Argument Name": "recipe_product",
                "Value Supplied": recipe_product,
                "Type": str
            }
        ])
    # endregion

    if recipe_id is not None:
        try:
            sql = f"""
            SELECT *
            FROM Recipes
            WHERE Recipe_ID={recipe_id}
            """
            cur = database.cursor()
            cur.execute(sql)

            recipe = cur.fetchall()[0]

            recipe_id, recipe_items, recipe_products, recipe_craft_time, recipe_machines, recipe_modules = recipe

            # TODO convert recipe_items, Recipe_products, Recipe_Machines into lists.

            recipe_items = _convert_str_to_dict_list(recipe_items)
            recipe_products = _convert_str_to_dict_list(recipe_products)
            recipe_machines = _convert_str_to_list(recipe_machines)
            recipe_modules = _convert_str_to_list(recipe_modules)

            return [{
                "Recipe_id": recipe_id,
                "Recipe_Items": recipe_items,
                "Recipe_Products": recipe_products,
                "Recipe_Craft_Time": recipe_craft_time,
                "Recipe_Machines": recipe_machines,
                "Recipe_Modules_Allowed": recipe_modules
            }]

        except Error as e:
            print(e)

    if recipe_product is not None:
        try:
            cur = database.cursor()
            product_sql = f"""
            SELECT *
            FROM Items
            WHERE Item_Name={recipe_product}
            """
            cur.execute(product_sql)

            product = cur.fetchall()
            item_id, item_name, item_energy_value = product[0]

            # As we are saving a list to the Recipe_Products column as TEXT, we cannot make a SQL statement which is
            # 100% accurate.
            recipe_sql = f"""
            SELECT *
            FROM Recipes
            WHERE {item_name} in Recipe_Products;
            """
            cur.execute(recipe_sql)

            recipes = cur.fetchall()

            recipes_with_product = []
            for recipe in recipes:
                recipe_id, recipe_items, recipe_products, recipe_craft_time, recipe_machines, recipe_modules = recipe

                # TODO rewrite this to convert everything needed into the dict form of lists
                # Convert the string form of the list to an actual list
                recipe_product = _convert_str_to_list(recipe_product)

                if item_name in recipe_product:
                    # Convert the items, machines and modules to lists.
                    recipe_items = _convert_str_to_list(recipe_items)
                    recipe_machines = _convert_str_to_list(recipe_machines)
                    recipe_modules = _convert_str_to_list(recipe_modules)

                    recipes_with_product += {
                        "Recipe_id": recipe_id,
                        "Recipe_Items": recipe_items,
                        "Recipe_Products": recipe_products,
                        "Recipe_Craft_Time": recipe_craft_time,
                        "Recipe_Machines": recipe_machines,
                        "Recipe_Modules_Allowed": recipe_modules
                    }
            return recipes_with_product

        except Error as e:
            print(e)


def get_all_recipes(database: sqlite3.Connection) -> Dict[str, str]:
    """
    Gets all the recipes from a database.
    :param database: Connection object; The database.
    :return: Dict[str, ]
    """


# endregion

# region Items
def create_item_table(database: sqlite3.Connection, override_existing: bool = False):
    """
    Creates a new table inside a database for items.
    
    :param database: Connection Object; The database to add the table to.
    :param override_existing: bool; Whether or not to override an existing table. Defaults to False.
    
    :returns:
    """
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        },
        {
            "Argument Name": "override_existing",
            "Value Supplied": override_existing,
            "Type": bool
        }
    ])

    if override_existing:
        database.cursor().execute("DROP TABLE Items")
        database.commit()

    sql = """
    CREATE TABLE Items (
        Item_ID
            INTEGER
            PRIMARY KEY,
        Item_Name
            TEXT
            NOT NULL
            UNIQUE,
        Item_Energy_Value_KW
            REAL
            CHECK (Item_Energy_Value_KW >= 0) 
            NOT NULL
            DEFAULT (0.0) 
    );
    """
    database.cursor().execute(sql)
    database.commit()


def add_item(database: sqlite3.Connection, item_name: str, item_energy_value_kw: float = 0.0):
    """
    Adds an item to the database.
    
    :param database: Connection object; The database to add the item to.
    :param item_name: str; The name of the item.
    :param item_energy_value_kw: float; The amount of energy the item provides when burnt. Defaults to 0.0.
    
    :return:
    """
    _check_types([
        {
            "Argument Name": "item_name",
            "Value Supplied": item_name,
            "Type": str
        },
        {
            "Argument Name": "item_energy_value_KW",
            "Value Supplied": item_energy_value_kw,
            "Type": float
        }
    ])

    sql = """
    INSERT INTO Items(
        Item_Name,
        Item_Energy_Value_KW
        )
    Values(?,?)
    """
    try:
        database.cursor().execute(sql, (item_name, item_energy_value_kw))
        database.commit()
    except Error as e:
        print(e)
    except IntegrityError as e:
        print(e)


def get_item(database: sqlite3.Connection, item_id: int = None, item_name: str = None) -> List[Dict[str, str or float]]:
    """
    Gets an item.
    
    :param database: Connection Object; The database to search in.
    :param item_id: int; The ID of the item if known. Defaults to None.
    :param item_name: str; The name of the item if known. Defaults to None.
    
    :return: Dict[str, str or float]
    """
    # region Check Types
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        }
    ])

    if item_id is not None:
        _check_types([
            {
                "Argument Name": "item_id",
                "Value Supplied": item_id,
                "Type": int
            }
        ])

    if item_name is not None:
        _check_types([
            {
                "Argument Name": "item_name",
                "Value Supplied": item_name,
                "Type": str
            }
        ])
    # endregion

    if item_id is not None:
        try:
            sql = f"""
            SELECT *
            FROM Items
            WHERE Item_ID={item_id}
            """
            cur = database.cursor()
            cur.execute(sql)

            row = cur.fetchall()
            item_id, item_name, item_energy_value = row[0]
            return [{
                "Item_id": item_id,
                "Item_Name": item_name,
                "Item_Energy_Value": item_energy_value
            }]
        except Error as e:
            print(e)
        except ValueError as e:
            print(e)

    if item_name is not None:
        sql = f"""
        SELECT *
        FROM Items
        WHERE Item_Name LIKE "%{item_name}%"
        """

        cur = database.cursor()
        cur.execute(sql)

        rows = cur.fetchall()
        items = []

        for row in rows:
            item_id, item_name, item_energy_value = row
            items.append({
                "Item_id": item_id,
                "Item_Name": item_name,
                "Item_Energy_Value": item_energy_value
            })
        return items


def get_all_items(database: sqlite3.Connection) -> List[Tuple[str or int or float]]:
    """
    Gets all items from a database.
    
    :param database: Connection Object; The database to get all the items from.
    
    :return: List[Tuple[str or int or float]]
    """
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        }
    ])

    cur = database.cursor()
    cur.execute("SELECT * FROM Items")
    return cur.fetchall()


def update_item(database: sqlite3.Connection, item_id: int = None, item_name: str = None,
                prompt_user_on_multiple_match: bool = True, **new_values: Dict[str, str or int or float]):
    """
    Updates an items information.
    
    :param database: Connection object; The database the item is in.
    :param item_id: int; The id of the item if known. Defaults to None.
    :param item_name: str; The name of the item if known. Defaults to None.
    :param prompt_user_on_multiple_match: bool; Whether or not to prompt the users to input the item they want if
    multiple items with the same name exists. Defaults to True.
    
    :return: 
    """
    # region Type Checks
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        },
        {
            "Argument name": "prompt_user_on_multiple_match",
            "Value Supplied": prompt_user_on_multiple_match,
            "Type": bool
        },
        {
            "Argument Name": "new_values",
            "Value Supplied": new_values,
            "Type": dict
        }
    ])

    if item_id is not None:
        _check_types([
            {
                "Argument Name": "item_id",
                "Value Supplied": item_id,
                "Type": int
            }
        ])
    if item_name is not None:
        _check_types([
            {
                "Argument Name": "item_name",
                "Value Supplied": item_name,
                "Type": str
            }
        ])
    # endregion

    # First, assign item as the output of get_item, then check its length.
    if len(item := get_item(database, item_id=item_id, item_name=item_name)) > 1:
        if prompt_user_on_multiple_match:
            for items in item:
                print(items)

            # First, assign item_wanted to the input of the user, then check if it is in any of the items or stopping
            # the loop.
            while ((item_wanted := input("Please put the name of the item you want to edit: ")) not in (
                    ([items["Item_Name"] for items in item]) or ["Exit", "Stop", "Quit"])):
                for items in item:
                    print(items)

            for items in item:
                if items["Item_Name"] == item_wanted:
                    item_wanted = items

        else:
            item_wanted = item[0]

    elif len(item) == 1:
        item_wanted = item[0]

    else:
        item_wanted = None

    if item_wanted is not None and new_values != {}:
        for key in new_values.keys():
            if key in item_wanted.keys():
                item_wanted[key] = new_values[key]

        sql = """
        UPDATE Items
        SET Item_Name = ?,
            Item_Energy_Value_KW = ?
        Where Item_ID = ?
        """
        database.cursor().execute(sql, (item_wanted["Item_Name"],
                                        item_wanted["Item_Energy_Value"],
                                        item_wanted["Item_id"]))
        database.commit()
# endregion

# region Liquids
def create_liquid_table(database: sqlite3.Connection, override_existing: bool = False):
    """
    Creates a new table inside a database for liquids.
    
    :param database: Connection Object; The database to add the table to.
    :param override_existing: bool; Whether or not to override an existing table. Defaults to False.
    
    :returns:
    """
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        },
        {
            "Argument Name": "override_existing",
            "Value Supplied": override_existing,
            "Type": bool
        }
    ])

    if override_existing:
        database.cursor().execute("DROP TABLE Liquids")
        database.commit()

    sql = """
    CREATE TABLE IF NOT EXISTS Liquids (
        Liquid_ID
            INTEGER
            PRIMARY KEY,
        Liquid_Name            
            TEXT
            NOT NULL,
        Liquid_Temperature
            REAL    
            NOT NULL
            DEFAULT (15.0) 
    );
    """
    database.cursor().execute(sql)
    database.commit()


def add_liquid(database: sqlite3.Connection, liquid_name: str, liquid_temperature: float = 15.0):
    """
    Adds an liquid to the database.
    
    :param database: Connection object; The database to add the item to.
    :param item_name: str; The name of the liquid.
    :param liquid_temperature: float; The temperature of the liquid. Defaults to 15.0.
    
    :return:
    """
    _check_types([
        {
            "Argument Name": "liquid_name",
            "Value Supplied": liquid_name,
            "Type": str
        },
        {
            "Argument Name": "liquid_temperature",
            "Value Supplied": liquid_temperature,
            "Type": float
        }
    ])

    sql = """
    INSERT INTO Liquids(
        Liquid_Name,
        Liquid_Temperature
        )
    Values(?,?)
    """
    try:
        database.cursor().execute(sql, (liquid_name, liquid_temperature))
        database.commit()
    except Error as e:
        print(e)
    except IntegrityError as e:
        print(e)


def get_liquid(database: sqlite3.Connection, liquid_id: int = None, liquid_name: str = None) -> List[Dict[str, str or float]]:
    """
    Gets an liquid.
    
    :param database: Connection Object; The database to search in.
    :param liquid_id: int; The ID of the liquid if known. Defaults to None.
    :param liquid_name: str; The name of the liquid if known. Defaults to None.
    
    :return: Dict[str, str or float]
    """
    # region Check Types
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        }
    ])

    if liquid_id is not None:
        _check_types([
            {
                "Argument Name": "liquid_id",
                "Value Supplied": liquid_id,
                "Type": int
            }
        ])

    if liquid_name is not None:
        _check_types([
            {
                "Argument Name": "liquid_name",
                "Value Supplied": liquid_name,
                "Type": str
            }
        ])
    # endregion

    if liquid_id is not None:
        try:
            sql = f"""
            SELECT *
            FROM Liquids
            WHERE Liquid_ID={liquid_id}
            """
            cur = database.cursor()
            cur.execute(sql)

            row = cur.fetchall()
            liquid_id, liquid_name, liquid_temperature = row[0]
            return [{
                "Liquid_id": liquid_id,
                "Liquid_Name": liquid_name,
                "Liquid_Temperature": liquid_temperature
            }]
        except Error as e:
            print(e)
        except ValueError as e:
            print(e)

    if liquid_name is not None:
        sql = f"""
        SELECT *
        FROM Liquids
        WHERE Liquid_Name LIKE "%{liquid_name}%"
        """

        cur = database.cursor()
        cur.execute(sql)

        rows = cur.fetchall()
        liquids = []

        for row in rows:
            liquid_id, liquid_name, liquid_temperature = row
            liquids.append({
                "Liquid_id": liquid_id,
                "Liquid_Name": liquid_name,
                "Liquid_Temperature": liquid_temperature
            })
        return liquids


def get_all_liquids(database: sqlite3.Connection) -> List[Tuple[str or int or float]]:
    """
    Gets all liquids from a database.
    
    :param database: Connection Object; The database to get all the liquids from.
    
    :return: List[Tuple[str or int or float]]
    """
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        }
    ])

    cur = database.cursor()
    cur.execute("SELECT * FROM Liquids")
    return cur.fetchall()


def update_liquid(database: sqlite3.Connection, liquid_id: int = None, liquid_name: str = None,
                prompt_user_on_multiple_match: bool = True, **new_values: Dict[str, str or int or float]):
    """
    Updates an liquids information.
    
    :param database: Connection object; The database the liquid is in.
    :param liquid_id: int; The id of the liquid if known. Defaults to None.
    :param liquid_name: str; The name of the liquid if known. Defaults to None.
    :param prompt_user_on_multiple_match: bool; Whether or not to prompt the users to input the liquid they want if
    multiple liquid with the same name exists. Defaults to True.
    
    :return: 
    """
    # region Type Checks
    _check_types([
        {
            "Argument Name": "database",
            "Value Supplied": database,
            "Type": sqlite3.Connection
        },
        {
            "Argument name": "prompt_user_on_multiple_match",
            "Value Supplied": prompt_user_on_multiple_match,
            "Type": bool
        },
        {
            "Argument Name": "new_values",
            "Value Supplied": new_values,
            "Type": dict
        }
    ])

    if liquid_id is not None:
        _check_types([
            {
                "Argument Name": "liquid_id",
                "Value Supplied": liquid_id,
                "Type": int
            }
        ])
    if liquid_name is not None:
        _check_types([
            {
                "Argument Name": "liquid_name",
                "Value Supplied": liquid_name,
                "Type": str
            }
        ])
    # endregion

    # First, assign liquid as the output of get_liquid, then check its length.
    if len(liquid := get_liquid(database, liquid_id=liquid_id, liquid_name=liquid_name)) > 1:
        if prompt_user_on_multiple_match:
            for liquids in liquid:
                print(liquid)

            # First, assign liquid_wanted to the input of the user, then check if it is in any of the liquids or stopping
            # the loop.
            while ((liquid_wanted := input("Please put the name of the liquid you want to edit: ")) not in (
                    ([liquids["Liquid_Name"] for liquids in liquid]) or ["Exit", "Stop", "Quit"])):
                for liquids in liquid:
                    print(liquid)

            for liquids in liquid:
                if liquids["Liquid_Name"] == liquid_wanted:
                    liquid_wanted = liquid

        else:
            liquid_wanted = liquid[0]

    elif len(liquid) == 1:
        liquid_wanted = liquid[0]

    else:
        liquid_wanted = None

    if liquid_wanted is not None and new_values != {}:
        for key in new_values.keys():
            if key in liquid_wanted.keys():
                liquid_wanted[key] = new_values[key]

        sql = """
        UPDATE Liquids
        SET Liquid_Name = ?,
            Liquid_Temperature = ?
        Where Liquid_ID = ?
        """
        database.cursor().execute(sql, (liquid_wanted["Liquid_Name"],
                                        liquid_wanted["Liquid_Temperature"],
                                        liquid_wanted["Liquid_id"]))
        database.commit()
# endregion

def _create_connection(file: str) -> sqlite3.Connection or None:
    """
    Creates a connection to a database.
    :param file: str; The file to attempt to create a connection to.
    :return: Connection object or None.
    """

    try:
        return sqlite3.connect(file)

    except Error:
        return None


def _check_types(arguments):
    for arg in arguments:
        if not isinstance(arg["Value Supplied"], arg["Type"]):
            raise ValueError(
                f"Argument {arg['Argument Name']} was expecting {arg['Type']}, got {type(arg['Value Supplied'])}.")


def _check_type_of_children(arguments):
    for arg in arguments:
        for each in arg["Value Supplied"]:
            if not isinstance(each, arg["Type"]):
                raise ValueError(
                    f"Value {each} given to {arg['Argument Name']} should be {arg['Type']}, not {type(each)}")


def _convert_str_to_list(string: str) -> List[str]:
    """
    Converts a str to a list.

    :param string: str; The string to be converted.

    :return: List[str]
    """
    string = string[1: len(string) - 1].split(",")
    for x in range(len(string)):
        string[x] = string[x].strip().strip("'")
    return string


def _convert_str_to_dict_list(string: str) -> List[Dict]:
    """
    Converts a str to a list of dicts.
    
    :param string: str; The string to be converted.
    
    :return: List[Dict]
    """
    converted = []

    string = string[1: len(string) - 1].split("}")
    string.pop()

    for x in range(len(string)):
        converted.append({})

        string[x] = string[x].strip()
        components = string[x].split(",")

        for y in range(len(components)):
            key, value = components[y].strip().split(":")

            key = key.strip().strip("{").strip("'")
            value = value.strip().strip("'")

            converted[x][key] = value

    return converted
