import EditDatabase
import GetDatabases

if __name__ == "__main__":
    test = EditDatabase
    database = GetDatabases.connect_to_database()["Vanilla"]
    
    # test.update_machine(database, machine_name="e", Machine_Name="Assembling Machine 1")
    
    # test.create_machine_table(database, True)
    # test.add_machine(database, "Assembling Machine 2", 0.75, 2, 150.0, 5.0, "Electric", 3.0)
    # print(test.get_all_machines(database))
    
    # test.add_machine(database, "Stone Furnace", 1.0, 0, 90.0, 0.0, "Item", 2.0)
    
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
    test.get_recipe(database, recipe_id=1)
    print(test.get_recipe(database, recipe_id=1))
    # list_test = test._convert_str_to_dict_list(test.get_recipe(database, recipe_id=1)[0]["Recipe_Items"])
    # print(list_test)
    # print(list_test[0].keys())
    
    
    
    # test.get_all_recipes(database)
 