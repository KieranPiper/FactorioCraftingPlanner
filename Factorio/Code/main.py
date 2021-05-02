import EditDatabase
import GetDatabases

if __name__ == "__main__":
    test = EditDatabase
    database = GetDatabases.connect_to_database()["Vanilla"]
    
    # test.update_machine(database, machine_name="e", Machine_Name="Assembling Machine 1")
    
    # test.create_machine_table(database, True)
    # test.add_machine(database, "Assembling Machine 2", 0.75, 2, 150.0, 5.0, "Electric", 3.0)
    # print(test.get_all_machines(database))
    
    # test.add_machine(database, "Electric Furnace", 2.0, 2, 180.0, 6.0, "Electric", 1.0)

    # test.add_item(database, "Iron Ore")
    # test.add_item(database, "Iron Plate")
    
    # test.add_recipe(database, 
    #     [{
    #         "Item_Name": "Iron Ore",
    #         "Item_Amount": 1
    #     }],
    #     [{
    #         "Item_Name": "Iron Plate",
    #         "Item_Amount": 1
    #     }],
    #     3.2,
    #     ["Stone Furnace"],
    #     []
    #                 )
    # test.get_recipe(database, recipe_id=1)
    # print(test.get_recipe(database, recipe_id=1))

    # print(test.get_item(database, item_id=1))
    # print(test.update_item(database, item_id=1, Item_Name="Iron Ore"))
    # print(test.get_item(database, item_id=1))
    #
    
    # test.get_all_recipes(database)
    
    test.add_item(database, item_name="Radar", item_energy_value_kw=000.0)
    # test.update_item(database, item_name="Powerr Armor", Item_Name="Power Armor")
    print(test.get_all_items(database))
 