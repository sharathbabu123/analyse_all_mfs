from datetime import datetime, timedelta

import pandas as pd
import st_aggrid
import streamlit as st
from mftool import Mftool
from requests.exceptions import ChunkedEncodingError
from stqdm import stqdm
from tqdm import tqdm


# @st.cache_data(experimental_allow_widgets=True)
def compute():
    selected_scheme_category_path = os.path.join(scheme_path, selected_scheme_category)+'.csv'
    df = pd.DataFrame()
    if selected_scheme_category != 'All':
        df = pd.read_csv(selected_scheme_category_path)
    else:
        for file in files:
            file_path = os.path.join(scheme_path, file)
            temp_df = pd.read_csv(file_path)
            df = df.append(temp_df, ignore_index=True)
    
    if selected_scheme_category == 'All':
        filtered_df = df[
            # (direct_flag & df['scheme_name'].str.contains('Direct')) & 
            # (growth_flag & df['scheme_name'].str.contains('Growth')) &
            # (~df['scheme_name'].str.contains('Bonus Option')) &
            # (~df['scheme_name'].str.contains('IDCW'))& 
            (df['scheme_type']==selected_scheme_type)]
    else:
    # Filtered DataFrame
        filtered_df = df[
            (df['scheme_category']==(selected_scheme_category)) & 
            # (direct_flag & df['scheme_name'].str.contains('Direct')) & 
            # (growth_flag & df['scheme_name'].str.contains('Growth')) &
            # (~df['scheme_name'].str.contains('Bonus Option')) &
            # (~df['scheme_name'].str.contains('IDCW'))& 
            (df['scheme_type']==selected_scheme_type)]

    if direct_flag:
        filtered_df = filtered_df[filtered_df['scheme_name'].str.contains('Direct')]
    if growth_flag:
        filtered_df = filtered_df[filtered_df['scheme_name'].str.contains('Growth')]

    # print(len(scheme_codes))

    current_date = datetime.strptime(selected_date.strftime('%Y-%m-%d'), '%Y-%m-%d')
    filtered_df = filtered_df.sort_values('fund_house').groupby('fund_house').first()
    print(filtered_df.head())


    scheme_codes = list(filtered_df['scheme_code'].unique())
    for i in range(3):
        cagr__1_year_list=[]
        cagr__3_year_list=[]
        cagr__5_year_list=[]
        cagr__10_year_list=[]
        current_date_year = get_dates(current_date,i)
        for code in stqdm(scheme_codes):
            try:
                mf_nav = mf.get_scheme_historical_nav(code, as_json=True)
                mf_nav = json.loads(mf_nav)
                
                # Convert the 'data' part of the JSON to a DataFrame
                df_data = pd.DataFrame(mf_nav['data'])
                
                
                # print(float(df[df['date'] == current_date]['nav']))
                one_year_nav = get_latest_nav(df_data,get_dates(current_date_year,1))
                three_year_nav = get_latest_nav(df_data,get_dates(current_date_year,3))
                five_year_nav = get_latest_nav(df_data,get_dates(current_date_year,5))
                ten_year_nav = get_latest_nav(df_data,get_dates(current_date_year,10))
                current_nav = get_latest_nav(df_data,current_date_year)

                # print(current_nav,one_year_nav)
                
                if current_nav is None or one_year_nav is None or one_year_nav == 0:
                    cagr_1_year = None
                else:
                    cagr_1_year = round(((current_nav / one_year_nav) ** (1 / 1) - 1) * 100, 2)
                
                if current_nav is None or three_year_nav is None or three_year_nav == 0:
                    cagr_3_year = None
                else:
                    cagr_3_year = round((( current_nav / three_year_nav) ** (1 / 3) - 1) * 100,2)
                
                if current_nav is None or five_year_nav is None or five_year_nav == 0:
                    cagr_5_year = None
                else:
                    cagr_5_year = round((( current_nav / five_year_nav) ** (1 / 5) - 1) * 100,2)
                
                if current_nav is None or ten_year_nav is None or ten_year_nav == 0:
                    cagr_10_year = None
                else:
                    cagr_10_year = round((( current_nav / ten_year_nav) ** (1 / 10) - 1) * 100,2)


                cagr__1_year_list.append(cagr_1_year)
                cagr__3_year_list.append(cagr_3_year)
                cagr__5_year_list.append(cagr_5_year)
                cagr__10_year_list.append(cagr_10_year)

                # print(current_nav,one_year_nav,cagr_1_year)

                

                
                
            except ChunkedEncodingError:
                print(f"Error occurred for code: {code}")
        
        # filtered_df.sort_values(by='cagr', ascending=True, inplace=True)

        # ...
        # df.loc[df['scheme_code'] == code, 'cagr'] = cagr
        filtered_df['cagr_1_year'] = cagr__1_year_list
        filtered_df['cagr_3_year'] = cagr__3_year_list
        filtered_df['cagr_5_year'] = cagr__5_year_list
        filtered_df['cagr_10_year'] = cagr__10_year_list
        

        filtered_df.sort_values(by=sort_factor, ascending=False, inplace=True)
        top_10 = filtered_df.head(10)
        # go_builder = st_aggrid.GridOptionsBuilder.from_dataframe(top_10[['scheme_name', 'cagr_1_year', 'cagr_3_year', 'cagr_5_year', 'cagr_10_year']])
        # go_builder.configure_grid_options(alwaysShowHorizontalScroll = True)
        # go = go_builder.build()
        # st_aggrid.AgGrid(top_10[['scheme_name', 'cagr_1_year', 'cagr_3_year', 'cagr_5_year', 'cagr_10_year']],gridOptions=go, theme='streamlit', height=400)
        # st.cache(
        st.subheader(f'Top 10 Mutual Funds in Year {current_date_year.strftime('%Y')} :')
            # )
        # st.cache(
        st_aggrid.AgGrid(top_10[['scheme_name', 'cagr_1_year', 'cagr_3_year', 'cagr_5_year', 'cagr_10_year']]
                                ,columns_auto_size_mode=st_aggrid.ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,key=i,
                                update_mode = st_aggrid.GridUpdateMode.MODEL_CHANGED, 
                                 reload_data=True)
            # )
    return "None"

def get_latest_nav(df_data, date):
    date = date.strftime('%d-%m-%Y')
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

def get_dates(date,n_years):
    return (date - timedelta(days=n_years * 365))

# Initialize mftool
mf = Mftool()


# df = pd.read_csv('scheme_details_with_scheme_type.csv')



# Add a page icon
st.title('📄 Mutual Fund Returns')

import os

current_directory = os.getcwd()
folder_path = os.path.join(current_directory, 'mf_info')
folder_names = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
print(folder_names)

# Sidebar filters
selected_scheme_type = st.sidebar.selectbox('Select Scheme Type', folder_names)



# selected_scheme_type = st.sidebar.selectbox('Select Scheme Type', scheme_types)
# Filter options
# scheme_types = df['scheme_type'].unique()


scheme_path = os.path.join(folder_path, selected_scheme_type)
files = [name for name in os.listdir(scheme_path) if os.path.isfile(os.path.join(scheme_path, name))]

scheme_categories = ['All'] + [file.replace(".csv","") for file in files]
# selected_scheme_type = st.sidebar.selectbox('Select Scheme Type', scheme_types)
selected_scheme_category = st.sidebar.selectbox('Select Scheme Category', scheme_categories)

direct_flag = st.sidebar.checkbox('Direct Flag')
growth_flag = st.sidebar.checkbox('Growth Flag')


selected_date = st.sidebar.date_input('Select Date', datetime.now())

sort_factor = st.sidebar.selectbox('Sort Factor', ['cagr_1_year', 'cagr_3_year', 'cagr_5_year', 'cagr_10_year'])

import streamlit as st

# Add a submit button
submit_button = st.sidebar.button('Submit')




# current_date = '31-03-2021'
# print(type(current_date))

# one_year_end_date = (datetime.now() - timedelta(days=365)).strftime('%d-%m-%Y')
# three_year_end_date = (datetime.now() - timedelta(days=3 * 365)).strftime('%d-%m-%Y')
# five_year_end_date = (datetime.now() - timedelta(days=5 * 365)).strftime('%d-%m-%Y')
# ten_year_end_date = (datetime.now() - timedelta(days=10 * 365)).strftime('%d-%m-%Y')
# end_date = '31-03-2020'
# print(one_year_end_date)
# print(three_year_end_date)
# print(five_year_end_date)
# print(ten_year_end_date)
# (filtered_df).to_csv('filtered_df.csv',index=False)

# mf.get_scheme_historical_nav("119597",as_json=True)
import json

import pandas as pd
import streamlit as st

# if "load_state" not in st.session_state:
#     st.session_state.load_state = False

if submit_button :
# or st.session_state.load_state:
    # st.session_state.load_state = True
    # Filtered DataFrame
    # filtered_df = df[ (df['scheme_category'] == selected_scheme_category)]
    compute()
        # st.write(top_10)


    


