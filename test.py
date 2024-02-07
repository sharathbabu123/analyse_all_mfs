import os

import pandas as pd

df = pd.read_csv('scheme_details_with_scheme_type.csv')

unique_scheme_types = df['scheme_type'].unique()


output_folder = 'mf_info'
os.makedirs(output_folder, exist_ok=True)

for scheme_type in unique_scheme_types:
    os.makedirs(f'{output_folder}/{scheme_type}', exist_ok=True)
    unique_scheme_categories = df[df['scheme_type'] == scheme_type]['scheme_category'].unique()
    for category in unique_scheme_categories:
        category_df = df[(df['scheme_category'] == category) & (df['scheme_type'] == scheme_type)]
        category_df.to_csv(f'{output_folder}/{scheme_type}/{category}.csv', index=False)
