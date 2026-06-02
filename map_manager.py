import json

def load_map_data(file_path):
    """
    Load map data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: Loaded data from the JSON file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not valid JSON!")
        return None


def display_objects(objects):
    """
    Display information about each object.
    
    Args:
    objects (list): List of objects to display
    """
    for obj in objects:
        print(f"ID: {obj['id']}")
        print(f"  Type: {obj['type']}")
        print(f"  Position: x={obj['position']['x']}, y={obj['position']['y']}")
        print(f"  Properties:", end=" ")
        for prop in obj['properties']:
            print(f"{prop['name']}={prop['value']}", end=" ")
        print("\n")
