import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

pd10 = pd.read_csv("combined_companies_with_ratios_top10.csv")

filtered_pd10 = pd10[pd10['Symbol'] == 'Not Found']['Name']

filtered_pd10_array = pd10[pd10['Symbol'] == 'Not Found']['Name'].astype(str).values


def check_if_ticker_present():
     
        try:
            symbol = stock_input.driver.find_element(By.XPATH, "//a[contains(@href, 'nseindia')]//span[@class='ink-700 upper']")
            return symbol.text
            # element_exists = True
        except NoSuchElementException:
            # element_exists = False
            try:
                symbol = stock_input.driver.find_element(By.XPATH, "//a[contains(@href, 'bseindia')]//span[@class='ink-700 upper']")
                return symbol.text
            except NoSuchElementException:
                symbol = "Not Found"
                return symbol

class CachedWebElement(WebElement):
            def __init__(self, driver, by, value):
                self.driver = driver
                self.by = by
                self.value = value
                self._element = None

            @property
            def element(self):
                if self._element is None:
                    self._element = self.driver.find_element(self.by, self.value)
                return self._element

service = Service(executable_path=r'chromedriver.exe')
driver = webdriver.Chrome(service=service)  # Replace with the path to your chromedriver executable

try:
    driver.get("http://www.screener.in/login/")

    id='sharathr013@gmail.com'
    password='imfbabu1'
    # stocklist = pd.read_csv(r"C:\Users\shara\Desktop\gpt-bot\mutual_funds\combined_companies_with_ratios.csv")
    # C:\Users\shara\Desktop\gpt-bot\mutual_funds\combined_companies_with_ratios.csv
    tickers=pd3[pd3.columns[0]]
   
    # time.sleep(10)
    # login.click()
    username_input = driver.find_element(By.ID, "id_username")
    username_input.send_keys(id)   # email id

    password_input = driver.find_element(By.ID, "id_password")
    password_input.send_keys(password)   # password

    button = driver.find_element(By.XPATH,"/html/body//form[@action='/login/']/button[@type='submit']")
    button.click()

    count=0
    symbol_text = []
    for stock in filtered_pd10_array:
            count+=1
            print(count)
            # ...

            
                
            stock_input = (By.CSS_SELECTOR, "div#desktop-search  .u-full-width")
            stock_input = CachedWebElement(driver, *stock_input)
            
            # stock_array = stock.split(" ")
            # stock_name = ""
            # for i in range(len(stock_array)):
            #      if len(stock_array[i])>1:
            #          stock_name = stock_name + stock_array[i]
            #          next_word = ( stock_array[i+1] if i+1 < len(stock_array) else "")
            #          break
            #      stock_name += stock_array[i] + " "

            stock_input.element.clear()
            stock = stock.replace(".","")
            for i in stock.split(" "):
                stock_input.element.send_keys(i+" ")
                time.sleep(0.5)
            time.sleep(1)
            try:
                # WebDriverWait(stock_input.driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[class="dropdown-content visible"]')))
                ul_element = stock_input.driver.find_element(By.XPATH, "//ul[@class='dropdown-content visible']")
                time.sleep(1)
                # li_elements = ul_element.find_elements(By.TAG_NAME, "li")
                # num_li_tags = len(li_elements)
                # print(num_li_tags)
                # if num_li_tags<=1:
                #     # stock_input.element.clear()
                #     stock_input.element.send_keys("\u0008")
                #     stock_input.element.send_keys("\u0008")
                #     time.sleep(2)
                #     stock_input.element.send_keys(Keys.ENTER)
                #     time.sleep(2)
                #     symbol = check_if_ticker_present()
                #     # print(symbol.text)
                #     symbol_text.append(symbol.text)

                #     continue
            except NoSuchElementException:
                symbol_text.append("Not Found")
                continue
            # # print(ul_element.text)
            # li_elements = ul_element.find_elements(By.TAG_NAME, "li")
            # num_li_tags = len(li_elements)
            # print(num_li_tags)
            # # WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[class="dropdown-content visible"]')))
            # time.sleep(1)
            # if num_li_tags>2:
            #     stock_input.element.send_keys(" "+next_word.replace(".",""))
            #     time.sleep(1)

            stock_input.element.send_keys(Keys.ENTER)
            # stock_input.element.send_keys(Keys.ENTER)
            time.sleep(1)

            
            # symbol = driver.find_element(By.XPATH, "//a[contains(@href, 'nseindia')]//span[@class='ink-700 upper']")
            try:
                symbol = check_if_ticker_present()
            except Exception as e:
                symbol = "Not Found"

            # ...

            # print(element_exists)

            # ...

            # print(symbol.text)
            symbol_text.append(symbol)
except Exception as e:
    print(e)
    symbol_text.append("Not Found")
    pass
            
pd10['Symbol']=symbol_text
pd10.to_csv("combined_companies_with_ratios_top10.csv", index=False)