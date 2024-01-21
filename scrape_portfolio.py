import logging
import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

logging.getLogger().addHandler(logging.NullHandler())

current_directory = r"C:\Users\shara\Desktop\gpt-bot\mutual_funds"


def set_driver():
    options = webdriver.ChromeOptions() 
    options.add_argument('--headless')

    prefs = {"download.default_directory" : r"C:\Users\shara\gpt-bot\mutual_funds" }

    options.add_experimental_option("prefs",prefs)

    options.add_argument('--disable-blink-features=AutomationControlled')

    # driver = webdriver.Chrome()

    # service = Service(executable_path=r"C:\Users\shara\Desktop\gpt-bot\mutual_funds\chromedriver.exe")
    service = Service()
    # Step 1: Set up the Selenium webdriver
    driver = webdriver.Chrome(service=service,options=options)  # Replace with the path to your chromedriver executable
    return driver


# Step 2: Send a GET request to the website
url = "https://mfiframes.mutualfundsindia.com/MutualFundIndia/Portfolio.aspx"
driver = set_driver()
driver.get(url)

# fund_type="Multi Cap Fund"
# Step 3: Select the dropdowns and choose the desired options
sub_category_dropdown = Select(driver.find_element(By.NAME, "ddlSubNature"))
options = [option.text for option in sub_category_dropdown.options]
# print(options)
driver.quit()
time.sleep(2)


for fund_type in options[1:]:
    try:
        driver = set_driver()  # Replace with the path to your chromedriver executable

# Step 2: Send a GET request to the website
        url = "https://mfiframes.mutualfundsindia.com/MutualFundIndia/Portfolio.aspx"
        driver.get(url)
        # clear_dropdowns(driver)

        # print(fund_type)
        ddlSubNature = Select(driver.find_element(By.NAME, "ddlSubNature"))
        ddlSubNature.select_by_visible_text(fund_type)

        choose_scheme_dropdown = Select(driver.find_element(By.NAME, "ddlScheme"))
        # print(len(choose_scheme_dropdown.options))

        for i in range(len(choose_scheme_dropdown.options)):
            try:
                # print(i+1)
                ddlFundHouse = Select(driver.find_element(By.NAME, "ddlFundHouse"))
                ddlFundHouse.select_by_index(0)

                time.sleep(1)
                choose_scheme_dropdown = Select(driver.find_element(By.NAME, "ddlScheme"))
                choose_scheme_dropdown.select_by_index(i+1)  
                try:
                    name = driver.find_element(By.ID,"lblFundNameBold").text
                except NoSuchElementException as e:
                    continue
                # print(name)

                # Step 4: Wait for the div id "dvPortFolio" to load
                wait = WebDriverWait(driver, 10)
                div_portfolio = wait.until(EC.presence_of_element_located((By.ID, "dvPortFolio")))

                # Step 5: Click on the input tag with name "btnShowMoreButton"
                btn_show_more = div_portfolio.find_element(By.NAME, "btnShowMoreButton")
                ActionChains(driver).move_to_element(btn_show_more).click().perform()

                # Step 6: Wait for the table with id "tblPort" to load
                table = wait.until(EC.presence_of_element_located((By.ID, "tblPort")))

                # Step 7: Copy the entire table
                table_html = table.get_attribute("outerHTML")
                # time.sleep(5)

                # Step 8: Print the HTML content of the table
                # print(table_html)

                # Step 9: Convert the HTML table to a dataframe
                soup = BeautifulSoup(table_html, 'html.parser')
                table_rows = soup.find_all('tr')
                data = []
                for row in table_rows[1:]:
                    cols = row.find_all('td')
                    cols = [col.text.strip() for col in cols]
                    data.append(cols)
                df = pd.DataFrame(data, columns=["Company Name", "Asset Type", "Percentage Allocation"])  # Replace "Column1", "Column2", "Column3", ... with your desired column names

                # print(df)
                # Step 10: Save the dataframe to a CSV file
                if not os.path.exists(current_directory+"\\"+fund_type):
                    os.makedirs(current_directory+"\\"+fund_type)

                df.to_csv(current_directory+"\\"+fund_type+"\\"+name + ".csv", index=False)
                
            except NoSuchElementException as e:
                pass
                # print("Element not found:", e)
            except StaleElementReferenceException as e:
                pass
                # print("Stale element reference:", e)
        driver.quit()
    except NoSuchElementException as e:
        # print("Element not found:", e)
        pass
    except StaleElementReferenceException as e:
        # print("Stale element reference:", e)
        pass
    except UnexpectedAlertPresentException as e:
        # print("Unexpected alert present:", e)
        pass

time.sleep(5)
# Step 10: Close the webdriver

