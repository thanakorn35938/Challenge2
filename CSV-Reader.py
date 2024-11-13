import json

def read_json_to_array(file_path, fields):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load JSON file into a Python data structure
            
            # Ensure data is in list format (wrap in list if it's a single object)
            if isinstance(data, dict):
                data = [data]
            
            # Extract only the specified fields
            filtered_data = [
                {field: item.get(field) for field in fields} for item in data
            ]
            
            return filtered_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

file_path = 'Challenge2_data.json'
fields = ['Apparent Magitude (m)']  # Specify the fields you want to extract
data_array = read_json_to_array(file_path, fields)

# Print or manage the array
print(data_array)
