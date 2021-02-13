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
            PRIMARY KEY
            AUTOINCREMENT,
        Machine_Name
            TEXT
            NOT NULL,
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
            CHECK (Machine_Energy_Type LIKE ("Electric" OR "Item" OR "Liquid")) 
            NOT NULL
            DEFAULT Electric,
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
                max_energy_consumption: float, idle_energy_consumption: float, energy_consumption_type: str, pollution: float):
    """
    Adds a machine to the database.
    :param database: Connection object; the database to add the machine to.
    :param machine_name: str; The name of the machine.
    :param craft_speed: float; The crafting speed of the machine.
    :param module_slots: int; The number of modules which can be in the machine.
    :param max_energy_consumption: float; The power consumption of the machine in KW while active.
    :param idle_energy_consumption: float; The power consumption of the machine in KW while idle.
    :param energy_consumption_type: str; The type of energy consumed (Electric, Fuel).
    :param pollution: The pollution the machine outputs per minute while active.
    :return:
    """
    sql = """
    INSERT INTO Machines(
        Machine_Name,
        Craft_Speed,
        Module_Slots,
        Max_Energy_Consumption_KW,
        Idle_Energy_Consumption_KW,
        Energy_Consumption_Type,
        Pollution_Per_Minute
        )
    Values(?,?,?,?,?,?,?);
    """
    try:
        database.cursor().execute(sql, (machine_name, craft_speed, module_slots, max_energy_consumption, idle_energy_consumption, energy_consumption_type.capitalize(), pollution))
        database.commit()
    except Error as e:
        print(e)
    except IntegrityError as e:
        print(e)

def get_machine(database: sqlite3.Connection, id: int = None, machine_name: str = None) -> List[Dict[str, str or float]]:
    """
    Gets a machine.
    
    :param database: Connection object; The database to search in.
    :param id: int; The ID of the machine if known. Defaults to None.
    :param machine_name: str; The name of the machine if known. Defaults to None.
    
    :return: Dict[str, str or float]
    """
    if id is not None:
        try:
            sql = f"""
            SELECT * 
            FROM Machines 
            WHERE Machine_ID={id}
            """
            cur = database.cursor()
            cur.execute(sql)
            
            row =  cur.fetchall()
            machine_id, machine_name, crafting_speed, module_slots, max_energy, idle_energy, energy_consumption_type, pollution = row[0]
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
            print(row)
    
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
            machine_id, machine_name, crafting_speed, module_slots, max_energy, idle_energy, energy_consumption_type, pollution = row
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
    cur = database.cursor()
    cur.execute("SELECT * FROM Machines")
    return cur.fetchall()
    

def update_machine(database: sqlite3.Connection, id: int = None, machine_name: str = None, prompt_user_on_multiple_match: bool = True, **new_values: Dict[str, str or int or float]):
    """
    Updates a machines information.
    
    :param database: Connection object; The database the machine is in.
    :param id: int; The id of the machine if known. Defaults to None.
    :param machine_name: str; The machine name if known. If multiple machines with the name given arises, will prompt
    user to input the one they want. Defaults to None.
    :param prompt_user_on_multiple_match: bool; Whether or not to prompt users to input the machine they want if
    multiple machines with the same name given exists. Defaults to True.
    :param new_values: Dict[str, str or int or float]; The new values for the machine)
    
    
    :return:
    """
    # First, assign machine the output of get_machine, then check it's length
    if len(machine := get_machine(database, id=id, machine_name=machine_name)) > 1:
        if prompt_user_on_multiple_match:
            for item in machine:
                print(item)
            
            while ((machine_wanted := input("Please put the name of the machine you want to edit: ")) in ((item["Machine_Name"] for item in machine) or ["Exit", "Stop", "Quit"])):
                for item in machine:
                    if item["Machine_Name"] == machine_wanted:
                        machine_wanted = item
                break
        
        else:
            machine_wanted = machine[0]
        
    elif len(machine) == 1:  # This works due to the fact that the := operator assigns the machine variable to the output of get_machine.
        machine_wanted = machine[0]
    
    if machine_wanted is not None and new_values != {}:
        for key in new_values.keys():
            if key in machine_wanted.keys():
                machine_wanted[key] = new_values[key]

        sql = """
        UPDATE Machines
        SET Machine_Name = ?,
            Craft_Speed = ?,
            Module_Slots = ?,
            Max_Energy_Consumption_KW = ?,
            Idle_Energy_Consumption_KW = ?,
            Energy_Consumption_Type = ?,
            Pollution_Per_Minute = ?
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
def get_all_recipes(database: sqlite3.Connection) -> Dict[str, str]:
    """
    Gets all the recipes from a database.
    :param database: Connection object; The database.
    :return: Dict[str, ]
    """

def create_recipe_table(database: sqlite3.Connection, override_existing: bool = False):
    """
    Creates a new table inside a database for recipes
    :param database: Connection object; The database to add the table to.
    :param override_existing: bool; Whether or not to override an existing table.
    :return:
    """
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
            PRIMARY KEY
            AUTOINCREMENT,
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

def add_recipe(database: sqlite3.Connection, product: List[Dict[str, str or float]], reqirements: List):...

    # Check type of the following:
    #   product (should be list)
# endregion

def _create_connection(file: str) -> sqlite3.Connection or None:
    """
    Creates a connection to a database.
    :param file: str; The file to attempt to create a connection to.
    :return: Connection object or None.
    """

    try:
        return sqlite3.connect(file)

    except Error as e:
        return None
