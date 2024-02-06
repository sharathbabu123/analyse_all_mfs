import csv
import datetime
import os

curent_directory = os.getcwd()

# Get the current directory
current_directory_portfolio = r"C:\Users\shara\Desktop\gpt-bot\mutual_funds\HOLDING"
print(current_directory_portfolio)

current_directory_sector_holding = r"C:\Users\shara\Desktop\gpt-bot\mutual_funds\SECTOR_HOLDING"
print(current_directory_sector_holding)

current_datetime = str(datetime.date.today())
print(current_datetime)


combined_file_path_portfolio = curent_directory+'\\daily_mf_data'+'\\TOP_HOLDING'+'\\combined_portfolio_'+current_datetime+'.csv'
combined_file_path_sector_holding = curent_directory+'\\daily_mf_data'+'\\TOP_SECTOR_HOLDING'+'\\combined_sector_'+current_datetime+'.csv'

if os.path.exists(combined_file_path_portfolio):
    # Empty the file
    open(combined_file_path_portfolio, 'w').close()
else:
    # Create the file
    open(combined_file_path_portfolio, 'x').close()

if os.path.exists(combined_file_path_sector_holding):
    # Empty the file
    open(combined_file_path_sector_holding, 'w').close()
else:
    # Create the file
    open(combined_file_path_sector_holding, 'x').close()


for file in os.listdir(current_directory_portfolio):
    file_path = os.path.join(current_directory_portfolio, file)
    
    # Check if the item is a CSV file
    if file.endswith('.csv'):
        # Read the CSV file
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)
        
        # Skip the first row
        rows = rows[1:]
        
        
            
        

        # Append the rows to the combined file
        with open(combined_file_path_portfolio, 'a') as combined_file:
            writer = csv.writer(combined_file)
            writer.writerows(rows)
                    
# Remove empty rows from the combined file
with open(combined_file_path_portfolio, 'r') as combined_file:
    lines = combined_file.readlines()



# Remove empty rows
lines = [line for line in lines if line.strip()]

# Write the non-empty lines back to the combined file
with open(combined_file_path_portfolio, 'w') as combined_file:
    combined_file.writelines(lines)

# Read the existing content of the combined file
with open(combined_file_path_portfolio, 'r') as combined_file:
    existing_content = combined_file.read()

# # Remove rows with 5 entries rather than 6
# rows = [row for row in rows if len(row) == 6]

# # Append the rows to the combined file
# with open(combined_file_path_portfolio, 'a') as combined_file:
#     writer = csv.writer(combined_file)
#     writer.writerows(rows)



# Append the header row to the existing content
header_row =["Company Name", "Asset Type", "Percentage Allocation","Portfolio Date","Scheme Name","Fund House","Type","Sub-Category","Category"]
header_row_str = ','.join(header_row) + '\n'
new_content = header_row_str + existing_content


# Write the new content back to the combined file
with open(combined_file_path_portfolio, 'w') as combined_file:
    combined_file.write(new_content)
    


for file in os.listdir(current_directory_sector_holding):
    file_path = os.path.join(current_directory_sector_holding, file)
    
    # Check if the item is a CSV file
    if file.endswith('.csv'):
        # Read the CSV file
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)
        
        # Skip the first row
        rows = rows[1:]
        
        
            
        

        # Append the rows to the combined file
        with open(combined_file_path_sector_holding, 'a') as combined_file:
            writer = csv.writer(combined_file)
            writer.writerows(rows)
                    
# Remove empty rows from the combined file
with open(combined_file_path_sector_holding, 'r') as combined_file:
    lines = combined_file.readlines()

# Remove empty rows
lines = [line for line in lines if line.strip()]

# Write the non-empty lines back to the combined file
with open(combined_file_path_sector_holding, 'w') as combined_file:
    combined_file.writelines(lines)

# Read the existing content of the combined file
with open(combined_file_path_sector_holding, 'r') as combined_file:
    existing_content = combined_file.read()

# Append the header row to the existing content
header_row =["Sector Name", "Dummy", "Percentage Allocation","Scheme Name","Fund House","Type","Sub-Category","Category"]
header_row_str = ','.join(header_row) + '\n'
new_content = header_row_str + existing_content
# print(new_content)
# Write the new content back to the combined file
with open(combined_file_path_sector_holding, 'w') as combined_file:
    combined_file.write(new_content)