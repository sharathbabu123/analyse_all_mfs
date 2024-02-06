import logging
import os
import time
from multiprocessing import Pool

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
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    service = Service()
    driver = webdriver.Chrome(service=service,options=options) 
    url = "https://mfiframes.mutualfundsindia.com/MutualFundIndia/Portfolio.aspx"
    driver.get(url)
    return driver

def get_schemes(driver):
    # Step 3: Select the dropdowns and choose the desired options
    schemes_dropdown = Select(driver.find_element(By.NAME, "ddlScheme"))
    schemes = [option.text for option in schemes_dropdown.options]
    # print(options)
    
    driver.quit()
    return schemes


current_directory = r"C:\Users\shara\Desktop\gpt-bot\mutual_funds"

# Step 2: Send a GET request to the website
driver = set_driver()
schemes_dropdown = Select(driver.find_element(By.NAME, "ddlScheme"))
schemes = [option.text for option in schemes_dropdown.options]
    # print(options)
    
driver.quit()

def scrape_portfolio(scheme):
    
        try:
            
            driver = set_driver()

            choose_scheme_dropdown = Select(driver.find_element(By.NAME, "ddlScheme"))
            choose_scheme_dropdown.select_by_visible_text(scheme)

            try:
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert

                # Interact with the popup
                alert.accept()
                time.sleep(1)
            except TimeoutException:
                pass


            ddlType = Select(driver.find_element(By.NAME, "ddlType"))
            ddlType_selected=ddlType.first_selected_option.text

            ddlFundHouse = Select(driver.find_element(By.NAME, "ddlFundHouse"))
            ddlFundHouse_selected=ddlFundHouse.first_selected_option.text
            
            ddlSubNature = Select(driver.find_element(By.NAME, "ddlSubNature"))
            ddlSubNature_selected=ddlSubNature.first_selected_option.text

            ddlCategory = Select(driver.find_element(By.NAME, "ddlCategory"))
            ddlCategory_selected=ddlCategory.first_selected_option.text

            port_date = driver.find_element(By.ID, "lblPortDate").text

            name = driver.find_element(By.ID, "lblFundNameBold").text

            div_portfolio = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "dvPortFolio")))
            
            try:
                btn_show_more = div_portfolio.find_element(By.NAME, "btnShowMoreButton")
                btn_show_more.click()
            except NoSuchElementException:
                pass
            table = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "tblPort")))
            table_html = table.get_attribute("outerHTML")

            soup = BeautifulSoup(table_html, 'html.parser')
            table_rows = soup.find_all('tr')
            data = []
            for row in table_rows[1:]:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                cols.append(port_date)  # Add port_date as a separate column
                cols.append(name)
                cols.append(ddlFundHouse_selected)
                cols.append(ddlType_selected)
                cols.append(ddlSubNature_selected)
                cols.append(ddlCategory_selected)
                data.append(cols)


            df = pd.DataFrame(data, columns=["Company Name", "Asset Type", "Percentage Allocation","Portfolio Date","Scheme Name","Fund House","Type","Sub-Category","Category"])  # Replace "Column1", "Column2", "Column3", ... with your desired column names
            if not os.path.exists(current_directory+"\\"+"HOLDING"):
                os.makedirs(current_directory+"\\"+"HOLDING")

            df.to_csv(current_directory+"\\HOLDING"+"\\"+name + ".csv", index=False)
            
            tables = driver.find_elements(By.CLASS_NAME, "table.table-bordered")
            table = tables[1]  
            table_html_sector = table.get_attribute("outerHTML")

            soup = BeautifulSoup(table_html_sector, 'html.parser')
            table_rows = soup.find_all('tr')
            data = []
            for row in table_rows[1:]:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                cols.append(name)
                cols.append(ddlFundHouse_selected)
                cols.append(ddlType_selected)
                cols.append(ddlSubNature_selected)
                cols.append(ddlCategory_selected)
                data.append(cols)
            df = pd.DataFrame(data,columns=["Sector Name", "Dummy", "Percentage Allocation","Scheme Name","Fund House","Type","Sub-Category","Category"])  # Replace "Column1", "Column2", "Column3", ... with your desired column names
            if not os.path.exists(current_directory+"\\"+"SECTOR_HOLDING"):
                os.makedirs(current_directory+"\\"+"SECTOR_HOLDING")

            df.to_csv(current_directory+"\\SECTOR_HOLDING"+"\\"+name + ".csv", index=False)
            driver.quit()
        except (NoSuchElementException, StaleElementReferenceException, UnexpectedAlertPresentException) as e:
            logging.error(e)
            driver.quit()
            


if __name__ == '__main__':
    pool = Pool()
    pool.map(scrape_portfolio, schemes[1:])
    # print(options)
    # for scheme in schemes[1:]:
    #     # print(fund_type)
    #     scrape_portfolio(scheme)
        