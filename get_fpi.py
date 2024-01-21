import calendar
import datetime
import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

start_date = datetime.date(2021, 8, 15)
end_date = datetime.date(2023, 11, 30)

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'August', 'Sep', 'Oct', 'Nov', 'Dec']
current_date = start_date
month_array = []

while current_date <= end_date:
    # print(current_date.strftime("%b%d%Y"))
    if current_date.day == 15 or current_date.day == calendar.monthrange(current_date.year, current_date.month)[1]:
        month = current_date.strftime("%b%d%Y")
        month_array.append(month)
    # time.sleep(0.5)
    # Move to the next month
    current_date = datetime.date(current_date.year, current_date.month, current_date.day) + datetime.timedelta(days=1)

print(month_array)
# time.sleep(5)


service = Service(executable_path=r'chromedriver.exe')
driver = webdriver.Chrome(service=service)  # Replace with the path to your chromedriver executable


for month in month_array:

    try:
        driver.get("https://www.fpi.nsdl.co.in/web/StaticReports/Fortnightly_Sector_wise_FII_Investment_Data/FIIInvestSector_"+month+".html")
    

        # Wait for the page to load
        time.sleep(5)


        # Find the div with id "dvFortnightly"
        div_fortnightly = driver.find_element(By.ID, 'dvFortnightly')

        # Find the table inside the div
        table = div_fortnightly.find_element(By.TAG_NAME, 'table')


        # Convert the table into a dataframe
        df = pd.read_html(table.get_attribute('outerHTML'))[0]

        # print(df)

        file_path = os.path.join("FPI\\", month + ".csv")
        df.to_csv(file_path, index=False)
        # You can now process the table data as needed
        # ...
    except Exception as e:
        print("An error occurred while accessing the website:", str(e))

# Quit the driver
driver.quit()



time.sleep(5)
