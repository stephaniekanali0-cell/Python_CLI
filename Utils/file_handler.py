import json
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data(file_path, data):
    try:
      os.makedirs(os.path.dirname(file_path), exist_ok=True)
      with open(file_path,'w') as file:
        json.dump(data, file, indent=4)
    except IOError as e:
     print (f"Error saving data to {file_path}: {e}")
