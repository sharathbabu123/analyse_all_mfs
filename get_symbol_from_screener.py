import pandas as pd

df = pd.read_csv('scheme_details.csv')
df['scheme_type'] = df['scheme_category'].apply(lambda x: 'Equity scheme' if 'Equity Scheme' in x else ('Debt scheme' if 'Debt Scheme' in x else ('Hybrid scheme' if 'Hybrid Scheme' in x else 'Others')))
df.to_csv('scheme_details_with_scheme_type.csv', index=False)