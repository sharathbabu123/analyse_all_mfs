import csv
import datetime
import os

# Get the current directory
current_directory = r"C:\Users\shara\Desktop\gpt-bot\mutual_funds"
print(current_directory)

current_datetime = str(datetime.date.today())
print(current_datetime)


combined_file_path = current_directory+'\\'+'daily_mf_data\\'+'combined_'+current_datetime+'.csv'

# Check if the combined file already exists
if os.path.exists(combined_file_path):
    # Empty the file
    open(combined_file_path, 'w').close()

# Iterate over the folders in the current directory
for folder in os.listdir(current_directory):
    folder_path = os.path.join(current_directory, folder)
    
    # Check if the item is a folder
    if os.path.isdir(folder_path):
        # Iterate over the CSV files in the folder
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            
            # Check if the item is a CSV file
            if file.endswith('.csv'):
                # Read the CSV file
                with open(file_path, 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    rows = list(reader)
                
                # Skip the first row
                rows = rows[1:]
                
                # Add a column with the folder name
                for row in rows:
                    row.append(folder)
                    
                

                # Append the rows to the combined file
                with open(combined_file_path, 'a') as combined_file:
                    writer = csv.writer(combined_file)
                    writer.writerows(rows)
                    
# Remove empty rows from the combined file
with open(combined_file_path, 'r') as combined_file:
    lines = combined_file.readlines()

# Remove empty rows
lines = [line for line in lines if line.strip()]

# Write the non-empty lines back to the combined file
with open(combined_file_path, 'w') as combined_file:
    combined_file.writelines(lines)

# Read the existing content of the combined file
with open(combined_file_path, 'r') as combined_file:
    existing_content = combined_file.read()

# Append the header row to the existing content
header_row = ['Company Name', 'Asset Type', 'Percentage Allocation', 'Fund Type']
header_row_str = ','.join(header_row) + '\n'
new_content = header_row_str + existing_content

# Write the new content back to the combined file
with open(combined_file_path, 'w') as combined_file:
    combined_file.write(new_content)
    
