import streamlit as st
from st_pages import Page, add_page_title, show_pages

show_pages(
    [
        Page("pages/Mutual_Fund_Portfolio_Analysis.py", "Mutual_Fund_Portfolio_Analysis", "🏠"),
        Page("pages/Mutual_Fund_Returns.py", "Mutual_Fund_Returns", ":books:"),
    ]
)

