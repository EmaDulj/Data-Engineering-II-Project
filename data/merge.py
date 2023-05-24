import json

# List of input JSON file paths
file_paths = ['sorted_page1.json', 'sorted_page2.json', 'sorted_page3.json', 'sorted_page4.json','sorted_page5.json', 'sorted_page6.json', 'sorted_page7.json', 'sorted_page8.json', 'sorted_page9.json','sorted_page10.json']

# Dictionary to store merged data
merged_data = {}

# Merge JSON files
for file_path in file_paths:
    with open(file_path, 'r') as file:
        data = json.load(file)
        merged_data.update(data)

# Save merged data to a new JSON file
output_file = '1000sorted.json'
with open(output_file, 'w') as file:
    json.dump(merged_data, file)

# Check length of merged data
merged_data_length = len(merged_data)
print("Length of merged data:", merged_data_length)
