import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


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


options = webdriver.ChromeOptions() 
# options.add_argument('--headless')

# prefs = {"download.default_directory" : r"C:\Users\shara\gpt-bot\mutual_funds" }
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')


service = Service(executable_path=r'chromedriver.exe')
driver = webdriver.Chrome(service=service,options=options)  # Replace with the path to your chromedriver executable


try:

    driver.get("http://www.screener.in/login/")

    id='sharathr013@gmail.com'
    password='imfbabu1'
    stocklist = pd.read_csv(r"C:\Users\shara\Desktop\gpt-bot\mutual_funds\combined_companies_with_ratios.csv")
    # C:\Users\shara\Desktop\gpt-bot\mutual_funds\combined_companies_with_ratios.csv
    tickers=stocklist[stocklist.columns[0]]
   
    # time.sleep(10)
    # login.click()
    username_input = driver.find_element(By.ID, "id_username")
    username_input.send_keys(id)   # email id

    password_input = driver.find_element(By.ID, "id_password")
    password_input.send_keys(password)   # password

    button = driver.find_element(By.XPATH,"/html/body//form[@action='/login/']/button[@type='submit']")
    button.click()
    symbol_text=[]
    count=0
    for stock in tickers:
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
            time.sleep(0.1)
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
        
    stocklist['Symbol']=symbol_text
        
except Exception as e:
    print("Error:", str(e))
