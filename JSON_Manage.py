import json
import os


databases_file_path = "databases.json"

def check_in_database(chromadatabase):
    """
    Check if the databases.json file already exists and add initialize it if not with the chroma database name.
    Args:
    - chromadatabase (str): Name of the chroma database to store data information for in the JSON file.
    Returns:
        None
    """

    database_starter_info = {
        "Num_Chunks": None,
        "Data_Path": 0,
        "Embedding_Function_Used": None
    }

    # Check if the master JSON database file exists
    if os.path.exists(databases_file_path):
        print("Adding new database info to JSON file")
        # Read the JSON file
        with open(databases_file_path, "r") as file:
            databases = json.load(file)

        # If JSON file exists already, add the new database_id if it does not exist already
        if chromadatabase not in databases:
            databases[chromadatabase] = database_starter_info
            # Write the updated dictionary back to the JSON file
            with open(databases_file_path, "w") as file:
                json.dump(databases, file, indent=4)
    else:
        print("The master JSON file does not exist already")
        # Create empty databases dictionary
        databases = {}
        # Add a new dictionary to store info for the new database
        databases[chromadatabase] = database_starter_info
        # Write the updated dictionary back to the JSON file
        with open(databases_file_path, "w") as file:
            json.dump(databases, file, indent=4)

def add_data_info_to_database(chromadatabase, data_path, num_chunks, embedding_function):
    """
    Add chroma database data and information to dabases.json file.
    Args:
    - chromadatabase (str): Name of the chroma database to store data information for in the JSON file.
    Returns:
        None
    """

    check_in_database(chromadatabase)
    with open(databases_file_path, "r") as file:
        databases = json.load(file)

    current_database = databases[chromadatabase]
    current_database["Num_Chunks"] = num_chunks
    current_database["Data_Path"] = data_path
    current_database["Embedding_Function_Used"] = embedding_function

    with open(databases_file_path, "w") as file:
        json.dump(databases, file, indent=4)

def remove_database(chromadatabase):
    """
    Remove chroma database name and information from JSON file when it is removed.
    Args:
    - chromadatabase (str): Name of the chroma database to remove the correct one in the JSON file.
    Returns:
        None
    """

    if os.path.exists(databases_file_path):
        with open(databases_file_path, "r") as file:
            databases = json.load(file)

        if chromadatabase in databases:
            del databases[chromadatabase]
            with open(databases_file_path, "w") as file:
                json.dump(databases, file, indent=4)
        else:
            print("Database ID not in Database")
    else:
        print("No Databases Made Yet")




    

