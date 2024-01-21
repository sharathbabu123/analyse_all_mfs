import datetime
import os

import pandas as pd
import plotly.express as px
import streamlit as st

current_date = str(datetime.date.today())
print(current_date)

# Define the dropdown options for year, month, and date
years = range(2000, datetime.date.today().year + 1)
months = range(1, 13)
days = range(1, 32)

# Create the sidebar for date selection
st.sidebar.title('Date Selection')
selected_year = st.sidebar.selectbox('Select Year', years,index=len(years)-1)
selected_month = st.sidebar.selectbox('Select Month', months,index=0)
selected_day = st.sidebar.selectbox('Select Day', days,index=16)

# Create a submit button
# submit_button = st.sidebar.button('Submit')

# Combine the selected year, month, and date into a single string
selected_date = datetime.date(selected_year, selected_month, selected_day).strftime("%Y-%m-%d")

current_directory = os.getcwd()
print(current_directory)


# Read the data from the CSV file
data = pd.read_csv(os.path.join(current_directory, 'daily_mf_data', 'combined_' + selected_date + '.csv'))

# Define the dropdown options
fund_types = ['All'] + data['Fund Type'].unique().tolist()

if "selected_fund_type" not in st.session_state:
    st.session_state["selected_fund_type"] = "All"

if st.session_state["selected_fund_type"] not in fund_types:
    st.session_state["selected_fund_type"] = "All"

st.session_state.selected_fund_type = st.selectbox('Select Fund Type',  fund_types, index=fund_types.index(st.session_state.selected_fund_type))

# Filter the data based on the selected fund type
if st.session_state.selected_fund_type == "All":
    filtered_data = data
else:
    filtered_data = data[data['Fund Type'] == st.session_state.selected_fund_type]

# Remove '%' and '-' signs from the Percentage Allocation column and convert it to float type
filtered_data['Percentage Allocation'] = filtered_data['Percentage Allocation'].str.replace('%', '').str.replace('-', '0').astype(float)

# Calculate the sum of the Percentage Allocation column
sum_percentage_allocation = filtered_data.groupby('Company Name')['Percentage Allocation'].sum()

# Get the top 10 company names based on sum of Percentage Allocation
top_10_company_names = sum_percentage_allocation.nlargest(10)
st.write("Top 10 Company Names by Sum of Percentage Allocation:")
st.write(top_10_company_names)

# Get the top 10 stocks based on frequency of Company Name
top_10_frequency = filtered_data['Company Name'].value_counts().nlargest(10)
st.write(top_10_frequency)

# Create a bar chart to illustrate the top 10 stocks by frequency
fig_frequency = px.bar(x=top_10_frequency.index, y=top_10_frequency.values, title='Top 10 Stocks by Frequency')
st.plotly_chart(fig_frequency)
