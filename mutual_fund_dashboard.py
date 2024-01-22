import datetime
import os

import pandas as pd
import plotly.express as px
import streamlit as st

# Set the title of the Streamlit dashboard
st.title('Mutual Fund Dashboard')



current_date = str(datetime.date.today())
# print(current_date)

# Define the dropdown options for year, month, and date
years = range(2000, datetime.date.today().year + 1)
months = range(1, 13)
days = range(1, 32)

# Create the sidebar for date selection
st.sidebar.title('Date Selection')

# Check if "selected_year", "selected_month", and "selected_day" are in session state, otherwise set them to default values
if "selected_year" not in st.session_state:
    st.session_state["selected_year"] = years[-1]
if "selected_month" not in st.session_state:
    st.session_state["selected_month"] = 1
if "selected_day" not in st.session_state:
    st.session_state["selected_day"] = 22

selected_year = st.sidebar.selectbox('Select Year', years, index=years.index(st.session_state["selected_year"]))
selected_month = st.sidebar.selectbox('Select Month', months, index=months.index(st.session_state["selected_month"]))
selected_day = st.sidebar.selectbox('Select Day', days, index=days.index(st.session_state["selected_day"]))

# # Rerun the page whenever a selectbox is chosen
# st.rerun()

# Update the session state with the selected year, month, and day
st.session_state["selected_year"] = selected_year
st.session_state["selected_month"] = selected_month
st.session_state["selected_day"] = selected_day

# Combine the selected year, month, and date into a single string
selected_date = str(selected_year) + '-' + str(selected_month).zfill(2) + '-' + str(selected_day).zfill(2)

current_directory = os.getcwd()
# print(current_directory)

print("Date: "+selected_date)
# Read the data from the CSV file
data = pd.read_csv(os.path.join(current_directory, 'daily_mf_data','TOP_HOLDING', 'combined_portfolio_' + selected_date + '.csv'),on_bad_lines='skip')
data_sector = pd.read_csv(os.path.join(current_directory, 'daily_mf_data','TOP_SECTOR_HOLDING', 'combined_sector_' + selected_date + '.csv'),on_bad_lines='skip')

# Define the dropdown options for fund type and asset type
fund_types = ['All'] + data['Fund Type'].unique().tolist()
asset_types = ['All'] + data['Asset Type'].unique().tolist()

# Check if "selected_fund_type" and "selected_asset_type" are in session state, otherwise set them to "All"
if "selected_fund_type" not in st.session_state:
    st.session_state["selected_fund_type"] = "All"
if "selected_asset_type" not in st.session_state:
    st.session_state["selected_asset_type"] = "All"

# Check if the selected fund type and asset type are valid, otherwise set them to "All"
if st.session_state["selected_fund_type"] not in fund_types:
    st.session_state["selected_fund_type"] = "All"
if st.session_state["selected_asset_type"] not in asset_types:
    st.session_state["selected_asset_type"] = "All"

# Create dropdowns for fund type and asset type selection
st.session_state["selected_fund_type"] = st.sidebar.selectbox('Select Fund Type', fund_types, index=fund_types.index(st.session_state["selected_fund_type"]))
st.session_state["selected_asset_type"] = st.sidebar.selectbox('Select Asset Type', asset_types, index=asset_types.index(st.session_state["selected_asset_type"]))

# # Rerun the page whenever a selectbox is chosen
# st.rerun()

# Filter the data based on the selected fund type and asset type
if st.session_state.selected_fund_type == "All" and st.session_state.selected_asset_type == "All":
    filtered_data = data.copy()
    filtered_data_sector = data_sector.copy()
elif st.session_state.selected_fund_type == "All":
    filtered_data = data[data['Asset Type'] == st.session_state.selected_asset_type].copy()
    filtered_data_sector = data_sector[data_sector['Asset Type'] == st.session_state.selected_asset_type].copy()
elif st.session_state.selected_asset_type == "All":
    filtered_data = data[data['Fund Type'] == st.session_state.selected_fund_type].copy()
    filtered_data_sector = data_sector[data_sector['Fund Type'] == st.session_state.selected_fund_type].copy()
else:
    filtered_data = data[(data['Fund Type'] == st.session_state.selected_fund_type) & (data['Asset Type'] == st.session_state.selected_asset_type)].copy()
    filtered_data_sector = data_sector[(data_sector['Fund Type'] == st.session_state.selected_fund_type) & (data_sector['Asset Type'] == st.session_state.selected_asset_type)].copy()

# Remove '%' and '-' signs from the Percentage Allocation column and convert it to float type
filtered_data['Percentage Allocation'] = filtered_data['Percentage Allocation'].str.replace('%', '').str.replace('-', '0').astype(float)
filtered_data_sector['Percentage Allocation'] = filtered_data_sector['Percentage Allocation'].str.replace('%', '').str.replace('-', '0').astype(float)

# Calculate the sum of the Percentage Allocation column
sum_percentage_allocation = filtered_data.groupby('Company Name')['Percentage Allocation'].sum()
sum_percentage_allocation_sector = filtered_data_sector.groupby('Sector Name')['Percentage Allocation'].sum()

# Get the top 10 company names based on sum of Percentage Allocation
top_10_company_names = sum_percentage_allocation.nlargest(10)
top_10_sector_names = sum_percentage_allocation_sector.nlargest(10)

# Get the top 10 stocks based on frequency of Company Name
top_10_frequency = filtered_data['Company Name'].value_counts().nlargest(10)


# Create a bar chart to illustrate the top 10 stocks by sum of percentage allocation
fig_sum = px.bar(x=top_10_sector_names.index, y=top_10_sector_names.values, title='Top 10 Sector by Sum of Percentage Allocation')
st.plotly_chart(fig_sum)

# Create a bar chart to illustrate the top 10 stocks by sum of percentage allocation
fig_sum = px.bar(x=top_10_company_names.index, y=top_10_company_names.values, title='Top 10 Stocks by Sum of Percentage Allocation')
st.plotly_chart(fig_sum)

# Create a bar chart to illustrate the top 10 stocks by frequency
fig_frequency = px.bar(x=top_10_frequency.index, y=top_10_frequency.values, title='Top 10 Stocks by Frequency')
st.plotly_chart(fig_frequency)
