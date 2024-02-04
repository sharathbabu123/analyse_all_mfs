import logging
import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def set_driver():
    options = webdriver.ChromeOptions() 
    # options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    service = Service()
    driver = webdriver.Chrome(service=service,options=options) 
    url = "https://mfiframes.mutualfundsindia.com/MutualFundIndia/Portfolio.aspx"
    driver = set_driver()
    driver.get(url)
    return driver

def get_options(driver):
    # Step 3: Select the dropdowns and choose the desired options
    sub_category_dropdown = Select(driver.find_element(By.NAME, "ddlSubNature"))
    options = [option.text for option in sub_category_dropdown.options]
    # print(options)
    
    driver.quit()
    return options


current_directory = r"C:\Users\shara\Desktop\gpt-bot\mutual_funds"

# Step 2: Send a GET request to the website


for fund_type in get_options(set_driver())[2:3]:
    try:
        driver = set_driver()

        ddlCategory = Select(driver.find_element(By.NAME, "ddlCategory"))
        ddlCategory.select_by_index(0)
        
        ddlType = Select(driver.find_element(By.NAME, "ddlType"))
        ddlType.select_by_index(0)

        ddlSubNature = Select(driver.find_element(By.NAME, "ddlSubNature"))
        ddlSubNature.select_by_visible_text(fund_type)

        ddlFundHouse = Select(driver.find_element(By.NAME, "ddlFundHouse"))
        ddlFundHouse.select_by_index(0)
        
        choose_scheme_dropdown = Select(driver.find_element(By.NAME, "ddlScheme"))

        for i in range(1,len(choose_scheme_dropdown.options)):
            try:
                ddlType = Select(driver.find_element(By.NAME, "ddlType"))
                ddlType.select_by_index(0)

                ddlFundHouse = Select(driver.find_element(By.NAME, "ddlFundHouse"))
                ddlFundHouse.select_by_index(0)

                choose_scheme_dropdown = Select(driver.find_element(By.NAME, "ddlScheme"))
                choose_scheme_dropdown.select_by_index(i+1)
                
                name = WebDriverWait(driver, 2).until(EC.presence_of_element_located(By.ID, "lblFundNameBold")).text

                div_portfolio = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "dvPortFolio")))

                btn_show_more = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, "btnShowMoreButton")))
                btn_show_more.click()
                
                # Step 6: Wait for the table with id "tblPort" to load
                table = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "tblPort")))

                # Step 7: Copy the entire table
                table_html = table.get_attribute("outerHTML")
                # time.sleep(5)

                # Step 11: Get the text in span with id "lblPortDate"
                port_date = driver.find_element(By.ID, "lblPortDate").text
                print(port_date)

                # Step 9: Convert the HTML table to a dataframe
                soup = BeautifulSoup(table_html, 'html.parser')
                table_rows = soup.find_all('tr')
                data = []
                for row in table_rows[1:]:
                    cols = row.find_all('td')
                    cols = [col.text.strip() for col in cols]
                    cols.append(port_date)  # Add port_date as a separate column
                    cols.append(name)  # Add fund_type as a separate column
                    data.append(cols)
                df = pd.DataFrame(data, columns=["Company Name", "Asset Type", "Percentage Allocation","Portfolio Date","Scheme Name"])

                # print(df)
                # Step 10: Save the dataframe to a CSV file
                if not os.path.exists(current_directory+"\\"+"TOP_HOLDING"+"\\"+fund_type):
                    os.makedirs(current_directory+"\\"+"TOP_HOLDING"+"\\"+fund_type)

                df.to_csv(current_directory+"\\TOP_HOLDING"+"\\"+fund_type+"\\"+name + ".csv", index=False)
                
                # Step 7: Extract the table with class name "table table-bordered"
                tables = driver.find_elements(By.CLASS_NAME, "table.table-bordered")
                table = tables[1]  # Access the second match

                # Step 8: Copy the entire table
                table_html_sector = table.get_attribute("outerHTML")

                # Step 9: Print the HTML content of the table
                # print(table_html_sector)

                # Step 10: Convert the HTML table to a dataframe
                soup = BeautifulSoup(table_html_sector, 'html.parser')
                table_rows = soup.find_all('tr')
                data = []
                for row in table_rows[1:]:
                    cols = row.find_all('td')
                    cols = [col.text.strip() for col in cols]
                    cols.append(name)
                    data.append(cols)
                df = pd.DataFrame(data,columns=["Sector Name", "Dummy", "Percentage Allocation","Scheme Name"])  # Replace "Column1", "Column2", "Column3", ... with your desired column names

                # print(df)

                if not os.path.exists(current_directory+"\\"+"TOP_SECTOR_HOLDING"+"\\"+fund_type):
                    os.makedirs(current_directory+"\\"+"TOP_SECTOR_HOLDING"+"\\"+fund_type)
                # Step 11: Save the dataframe to a CSV file
                df.to_csv(current_directory+"\\TOP_SECTOR_HOLDING"+"\\"+fund_type+"\\"+name + ".csv", index=False)
            except Exception as e:
                print(e)
                

    except Exception as e:
        print(e)
        driver.quit()
        
    driver.quit()
    time.sleep(2)
    break