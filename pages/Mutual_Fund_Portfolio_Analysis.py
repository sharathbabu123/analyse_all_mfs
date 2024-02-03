import datetime
import os

import pandas as pd
import plotly.express as px
import streamlit as st

# Set the title of the Streamlit dashboard
# Set the page icon


st.title('📊 Mutual Fund Portfolio Analysis')

current_directory = os.getcwd()

# Find the files in the folder "TOP_HOLDING" and sort them
files = sorted(os.listdir(os.path.join(current_directory, 'daily_mf_data', 'TOP_HOLDING')))

# Select the last file
last_file = files[-1]

# Save it as a variable as a string
selected_file = last_file.split('_')[-1].split('.')[0]


# current_directory = os.getcwd()
# current_directory = os.path.dirname(os.path.dirname(os.getcwd()))

# print(current_directory)

# print("Date: "+selected_date)
# Read the data from the CSV file
data = pd.read_csv(os.path.join(current_directory, 'daily_mf_data','TOP_HOLDING', 'combined_portfolio_' + selected_file+'.csv'),on_bad_lines='skip')
data_sector = pd.read_csv(os.path.join(current_directory, 'daily_mf_data','TOP_SECTOR_HOLDING', 'combined_sector_' + selected_file+'.csv'),on_bad_lines='skip')

# Define the dropdown options for fund type and asset type
fund_types = ['All'] + data['Fund Type'].unique().tolist()
asset_types = ['All'] + data['Asset Type'].unique().tolist()
scheme_names = ['All'] + data['Scheme Name'].unique().tolist()

# Check if "selected_fund_type" and "selected_asset_type" are in session state, otherwise set them to "All"
if "selected_fund_type" not in st.session_state:
    st.session_state["selected_fund_type"] = "All"
if "selected_asset_type" not in st.session_state:
    st.session_state["selected_asset_type"] = "All"
if "selected_scheme_name" not in st.session_state:
    st.session_state["selected_scheme_name"] = "All"

# Check if the selected fund type and asset type are valid, otherwise set them to "All"
if st.session_state["selected_fund_type"] not in fund_types:
    st.session_state["selected_fund_type"] = "All"
if st.session_state["selected_asset_type"] not in asset_types:
    st.session_state["selected_asset_type"] = "All"
if st.session_state["selected_scheme_name"] not in scheme_names:
    st.session_state["selected_scheme_name"] = "All"

# Create dropdowns for fund type and asset type selection
st.session_state["selected_fund_type"] = st.sidebar.selectbox('Select Fund Type', fund_types, index=fund_types.index(st.session_state["selected_fund_type"]))
st.session_state["selected_asset_type"] = st.sidebar.selectbox('Select Asset Type', asset_types, index=asset_types.index(st.session_state["selected_asset_type"]))
st.session_state["selected_scheme_name"] = st.sidebar.selectbox('Select Scheme Name', scheme_names, index=scheme_names.index(st.session_state["selected_scheme_name"]))

# # Rerun the page whenever a selectbox is chosen
# st.rerun()

# Filter the data based on the selected fund type and asset type
if st.session_state.selected_fund_type == "All" and st.session_state.selected_asset_type == "All":
    filtered_data = data.copy()
    filtered_data_sector = data_sector.copy()
elif st.session_state.selected_fund_type == "All":
    filtered_data = data[data['Asset Type'] == st.session_state.selected_asset_type].copy()
    filtered_data_sector = data_sector.copy()
elif st.session_state.selected_asset_type == "All":
    filtered_data = data[data['Fund Type'] == st.session_state.selected_fund_type].copy()
    filtered_data_sector = data_sector[data_sector['Fund Type'] == st.session_state.selected_fund_type].copy()
else:
    filtered_data = data[(data['Fund Type'] == st.session_state.selected_fund_type) & (data['Asset Type'] == st.session_state.selected_asset_type)].copy()
    filtered_data_sector = data_sector[(data_sector['Fund Type'] == st.session_state.selected_fund_type)].copy()

if st.session_state.selected_scheme_name != "All":
    filtered_data = filtered_data[filtered_data['Scheme Name'] == st.session_state.selected_scheme_name]
    filtered_data_sector = filtered_data_sector[filtered_data_sector['Scheme Name'] == st.session_state.selected_scheme_name]

# Remove '%' and '-' signs from the Percentage Allocation column and convert it to float type
filtered_data['Percentage Allocation'] = filtered_data['Percentage Allocation'].str.replace('%', '').str.replace('-', '0').astype(float)
filtered_data_sector['Percentage Allocation'] = filtered_data_sector['Percentage Allocation'].str.replace('%', '').str.replace('-', '0').astype(float)

# Calculate the sum of the Percentage Allocation column
sum_percentage_allocation = filtered_data.groupby('Company Name')['Percentage Allocation'].sum()
sum_percentage_allocation_sector = filtered_data_sector.groupby('Sector Name')['Percentage Allocation'].sum()

n = st.sidebar.slider('Select the value of n', 5, 30, 10, step=5)
# Get the top 10 company names based on sum of Percentage Allocation
top_10_company_names = sum_percentage_allocation.nlargest(n)
top_10_sector_names = sum_percentage_allocation_sector.nlargest(10)

# Get the top 10 stocks based on frequency of Company Name
top_10_frequency = filtered_data['Company Name'].value_counts().nlargest(n)


# Create a bar chart to illustrate the top 10 stocks by sum of percentage allocation
fig_sum = px.bar(x=top_10_sector_names.index, y=top_10_sector_names.values, title='Top 10 Sector by Sum of Percentage Allocation')


st.plotly_chart(fig_sum)

# Create a bar chart to illustrate the top 10 stocks by sum of percentage allocation
fig_sum = px.bar(x=top_10_company_names.index, y=top_10_company_names.values, title='Top 10 Stocks by Sum of Percentage Allocation')
st.plotly_chart(fig_sum)

# Create a bar chart to illustrate the top 10 stocks by frequency
fig_frequency = px.bar(x=top_10_frequency.index, y=top_10_frequency.values, title='Top 10 Stocks by Frequency')
st.plotly_chart(fig_frequency)
