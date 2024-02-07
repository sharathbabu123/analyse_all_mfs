import json
from datetime import datetime, timedelta

import pandas as pd
import st_aggrid
import streamlit as st
from mftool import Mftool
from requests.exceptions import ChunkedEncodingError
from stqdm import stqdm
from tqdm import tqdm


def get_dates(date,n_years):
    return (date - timedelta(days=n_years * 365))

# @st.cache_data(experimental_allow_widgets=True)
def compute():
    df = pd.DataFrame()
    current_directory = os.getcwd()
    selected_scheme_category_path = os.path.join(current_directory,"mf_info",selected_scheme_type, selected_scheme_category)+'.csv'
    df = pd.DataFrame()
    if selected_scheme_category != 'All':
        # print(selected_scheme_category_path)
        df = pd.read_csv(selected_scheme_category_path)
    else:
        for folder in scheme_types:
            for file in scheme_dict[folder]:
                file_path = os.path.join(current_directory,"mf_info",folder, file)+'.csv'
                temp_df = pd.read_csv(file_path)
                df = pd.concat([df, temp_df], ignore_index=True)
    
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
    # print(filtered_df.head())


    scheme_codes = list(filtered_df['scheme_code'].unique())
    for i in range(3):
        # print("hi")
        cagr__1_year_list=[]
        cagr__3_year_list=[]
        cagr__5_year_list=[]
        cagr__10_year_list=[]
        current_date_year = get_dates(current_date,i)
        for code in stqdm(scheme_codes):
            try:
                # print("in for loop")
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
        st.subheader(f"Top 10 Mutual Funds in Year {current_date_year.strftime('%Y')} :")
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


# Initialize mftool
mf = Mftool()


# df = pd.read_csv('scheme_details_with_scheme_type.csv')



# Add a page icon
st.title('📄 Mutual Fund Returns')

import os

scheme_dict = {'Debt scheme': ['Debt Scheme - Banking and PSU Fund', 'Debt Scheme - Corporate Bond Fund', 'Debt Scheme - Credit Risk Fund', 'Debt Scheme - Dynamic Bond',
                                'Debt Scheme - Floater Fund', 'Debt Scheme - Gilt Fund with 10 year constant duration', 'Debt Scheme - Gilt Fund', 'Debt Scheme - Liquid Fund',
                                  'Debt Scheme - Long Duration Fund', 'Debt Scheme - Low Duration Fund', 'Debt Scheme - Medium Duration Fund', 'Debt Scheme - Medium to Long Duration Fund',
                                    'Debt Scheme - Money Market Fund', 'Debt Scheme - Overnight Fund', 'Debt Scheme - Short Duration Fund', 'Debt Scheme - Ultra Short Duration Fund'], 'Equity scheme': ['Equity Scheme - Contra Fund', 'Equity Scheme - Dividend Yield Fund', 'Equity Scheme - ELSS', 'Equity Scheme - Large & Mid Cap Fund', 'Equity Scheme - Large Cap Fund', 'Equity Scheme - Mid Cap Fund', 'Equity Scheme - Multi Cap Fund', 'Equity Scheme - Small Cap Fund', 'Equity Scheme - Value Fund'], 'Hybrid scheme': ['Hybrid Scheme - Aggressive Hybrid Fund', 'Hybrid Scheme - Arbitrage Fund', 'Hybrid Scheme - Balanced Hybrid Fund', 'Hybrid Scheme - Conservative Hybrid Fund', 'Hybrid Scheme - Dynamic Asset Allocation or Balanced Advantage', 'Hybrid Scheme - Equity Savings', 'Hybrid Scheme - Multi Asset Allocation'], 'Others': ['1', '1098 Days', '1099 Days', '1100 Days', '1194 DAYS', '54EB Growth', 'Annual Dividend', 'Compulsory Reinvestment', 'Direct', 'ELSS', 'Formerly Known as IIFL Mutual Fund', 'FV Rs 32.161', 'Gilt', 'Growth', 'Half Yearly Dividend', 'IDF', 'Income', 'Merger of Capex & Energy Opportunities', 'Money Market', 'Other Scheme - FoF Domestic', 'Other Scheme - FoF Overseas', 'Other Scheme - Gold ETF', 'Other Scheme - Index Funds', 'Other Scheme - Other  ETFs', 'Solution Oriented Scheme - Children’s Fund', 'Solution Oriented Scheme - Retirement Fund']}

scheme_types = list(scheme_dict.keys())

# Sidebar filters
selected_scheme_type = st.sidebar.selectbox('Select Scheme Type', scheme_types)


scheme_categories = ['All']+scheme_dict[selected_scheme_type]

selected_scheme_category = st.sidebar.selectbox('Select Scheme Category', scheme_categories)

direct_flag = st.sidebar.checkbox('Direct Flag')
growth_flag = st.sidebar.checkbox('Growth Flag')


selected_date = st.sidebar.date_input('Select Date', datetime.now())

sort_factor = st.sidebar.selectbox('Sort Factor', ['cagr_1_year', 'cagr_3_year', 'cagr_5_year', 'cagr_10_year'])

import streamlit as st

# Add a submit button
submit_button = st.sidebar.button('Submit')


if submit_button :
# or st.session_state.load_state:
    # st.session_state.load_state = True
    # Filtered DataFrame
    # filtered_df = df[ (df['scheme_category'] == selected_scheme_category)]
    compute()
        # st.write(top_10)


    


