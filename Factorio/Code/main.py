import EditDatabase
import GetDatabases

if __name__ == "__main__":
    test = EditDatabase
    database = GetDatabases.connect_to_database()["Vanilla"]
    
    # test.create_machine_table(database)
    # test.add_machine(database, machine_name="Assembling Machine 3", craft_speed=1.25, module_slots=4, max_energy_consumption=375, idle_energy_consumption=12.5, energy_consumption_type="Electric", pollution=2)
    
    # for item in (test.get_machine(database, machine_name="Assembling Machine")):
    #     print(item)
    test.update_machine(database, id=1, Machine_Name="Assembling Machine 1", Pollution=4)
