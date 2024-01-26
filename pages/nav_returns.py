from datetime import datetime, timedelta

import pandas as pd
from mftool import Mftool
from requests.exceptions import ChunkedEncodingError
from tqdm import tqdm


def get_latest_nav(df_data, date):
    for i in range(3):
        if not (df_data[df_data['date'] == date].empty):
            nav = float(df_data[df_data['date'] == date]['nav'])
        else:
            nav = None
        # print(nav)
        if not pd.isnull(nav):
            # print(date, nav)
            return nav
        date = (datetime.strptime(date, '%d-%m-%Y') - timedelta(days=1)).strftime('%d-%m-%Y')
    return None


# Initialize mftool
mf = Mftool()


df = pd.read_csv('scheme_details_with_scheme_type.csv')

import streamlit as st

scheme_types = df['scheme_type'].unique()

selected_scheme_type = st.sidebar.selectbox('Select Scheme Type', scheme_types)
# Filter options
# scheme_types = df['scheme_type'].unique()
scheme_categories = df[df['scheme_type']==selected_scheme_type]['scheme_category'].unique()
# # Sidebar filters
# selected_scheme_type = st.sidebar.selectbox('Select Scheme Type', scheme_types)
selected_scheme_category = st.sidebar.selectbox('Select Scheme Category', scheme_categories)

selected_date = st.sidebar.date_input('Select Date', datetime.now())

sort_factor = st.sidebar.selectbox('Sort Factor', ['cagr_1_year', 'cagr_3_year', 'cagr_5_year', 'cagr_10_year'])

import streamlit as st

# Add a submit button
submit_button = st.sidebar.button('Submit')



# Filtered DataFrame
# filtered_df = df[ (df['scheme_category'] == selected_scheme_category)]


# Filtered DataFrame
filtered_df = df[(df['scheme_category'] == selected_scheme_category) & 
                 (df['scheme_name'].str.contains('Direct')) & 
                 (df['scheme_name'].str.contains('Growth')) & (df['scheme_type']==selected_scheme_type)]



scheme_codes = list(filtered_df['scheme_code'].unique())
print(len(scheme_codes))

current_date = selected_date.strftime('%d-%m-%Y')
# current_date = '31-03-2021'
print(current_date)

one_year_end_date = (datetime.now() - timedelta(days=365)).strftime('%d-%m-%Y')
three_year_end_date = (datetime.now() - timedelta(days=3 * 365)).strftime('%d-%m-%Y')
five_year_end_date = (datetime.now() - timedelta(days=5 * 365)).strftime('%d-%m-%Y')
ten_year_end_date = (datetime.now() - timedelta(days=10 * 365)).strftime('%d-%m-%Y')
# end_date = '31-03-2020'
print(one_year_end_date)
print(three_year_end_date)
print(five_year_end_date)
print(ten_year_end_date)

# mf.get_scheme_historical_nav("119597",as_json=True)
import json

import pandas as pd
import streamlit as st

cagr__1_year_list=[]
cagr__3_year_list=[]
cagr__5_year_list=[]
cagr__10_year_list=[]

if submit_button:
    for code in tqdm(scheme_codes):
        try:
            mf_nav = mf.get_scheme_historical_nav(code, as_json=True)
            mf_nav = json.loads(mf_nav)
            
            # Convert the 'data' part of the JSON to a DataFrame
            df_data = pd.DataFrame(mf_nav['data'])
            
            # print(float(df[df['date'] == current_date]['nav']))
            one_year_nav = get_latest_nav(df_data,one_year_end_date)
            three_year_nav = get_latest_nav(df_data,three_year_end_date)
            five_year_nav = get_latest_nav(df_data,five_year_end_date)
            ten_year_nav = get_latest_nav(df_data,ten_year_end_date)
            current_nav = get_latest_nav(df_data,current_date)

            # print(current_nav,one_year_nav)
            
            if current_nav is None or one_year_nav is None or one_year_nav == 0:
                cagr_1_year = None
            else:
                cagr_1_year = (( current_nav / one_year_nav) ** (1 / 1) - 1) * 100
            
            if current_nav is None or three_year_nav is None or three_year_nav == 0:
                cagr_3_year = None
            else:
                cagr_3_year = (( current_nav / three_year_nav) ** (1 / 3) - 1) * 100
            
            if current_nav is None or five_year_nav is None or five_year_nav == 0:
                cagr_5_year = None
            else:
                cagr_5_year = (( current_nav / five_year_nav) ** (1 / 5) - 1) * 100
            
            if current_nav is None or ten_year_nav is None or ten_year_nav == 0:
                cagr_10_year = None
            else:
                cagr_10_year = (( current_nav / ten_year_nav) ** (1 / 10) - 1) * 100


            cagr__1_year_list.append(cagr_1_year)
            cagr__3_year_list.append(cagr_3_year)
            cagr__5_year_list.append(cagr_5_year)
            cagr__10_year_list.append(cagr_10_year)

            # print(current_nav,one_year_nav,cagr_1_year)

            # df.loc[df['scheme_code'] == code, 'cagr'] = cagr
            
            
        except ChunkedEncodingError:
            print(f"Error occurred for code: {code}")


    filtered_df['cagr_1_year'] = cagr__1_year_list
    filtered_df['cagr_3_year'] = cagr__3_year_list
    filtered_df['cagr_5_year'] = cagr__5_year_list
    filtered_df['cagr_10_year'] = cagr__10_year_list

    # filtered_df.sort_values(by='cagr', ascending=True, inplace=True)

    # ...

    filtered_df.sort_values(by='cagr_3_year', ascending=False, inplace=True)
    top_10 = filtered_df.head(10)
    st.write(top_10[['scheme_name', 'cagr_1_year', 'cagr_3_year', 'cagr_5_year', 'cagr_10_year']])
    # st.write(top_10)


