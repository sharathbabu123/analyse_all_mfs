import pandas as pd
import glob

# Get a list of all CSV files in the "Mid Cap Fund" folder
folder_path = 'Multi Cap Fund'
csv_files = glob.glob(folder_path + '/*.csv')

# Create an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Iterate over each CSV file and read its contents into the combined DataFrame
for file in csv_files:
    df = pd.read_csv(file)
    combined_data = combined_data._append(df)

# Count the frequency of each company name
company_counts = combined_data['Company Name'].value_counts()

# Create a DataFrame to store the company names and their counts
company_counts_df = pd.DataFrame({'Company Name': company_counts.index, 'Count': company_counts.values})

combined_data['Percentage Allocation'] = combined_data['Percentage Allocation'].apply(lambda x: '0.00' if '%' not in str(x) else x)
# print(combined_data['Percentage Allocation'].to_string(index=False))

try:
    combined_data['Percentage Allocation'] = combined_data['Percentage Allocation'].str.rstrip('%').astype(float)
except ValueError as e:
    print(f"Error converting 'Percentage Allocation' column to float: {e}")
sum_allocation = combined_data.groupby('Company Name')['Percentage Allocation'].sum().reset_index()

# Merge the average allocation with the company counts DataFrame
company_counts_df = pd.merge(company_counts_df, sum_allocation, on='Company Name')

# Add "Asset Type" to the DataFrame
asset_type = combined_data.groupby('Company Name')['Asset Type'].first().reset_index()
company_counts_df = pd.merge(company_counts_df, asset_type, on='Company Name')

# Sort the DataFrame by the average allocation column
company_counts_df = company_counts_df.sort_values('Percentage Allocation', ascending=False)

# Save the DataFrame to a CSV file
company_counts_df.to_csv(folder_path+"_"+'company_counts.csv', index=False)
