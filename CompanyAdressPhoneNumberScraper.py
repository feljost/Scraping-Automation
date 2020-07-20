#####################################################
# ----------FOR EDUCATIONAL PURPOSES ONLY-----------#
# This script gathers company adresses & Phone      #
# numbers by webscraping europages.co.uk.           #
#                                                   #
# INSTRUCTIONS:                                     #
#     1. download webdriver and adjust line 40      #
#     2. Define a list of companies called "list"   #
#     3. Save dataframe 'df' in any format you      #
#        like.                                      #
#                                                   #
#####################################################

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


## Initialise the Dataframe
df = pd.DataFrame(columns=['Company Name', 'URL', 'Phone Number', 'Address', 'Country'])

## Loop through all companies
for i in list:
    company = i
    company_search_name = company.replace(" ","%20")
    company_search_name = company.replace(",","")

    try:  #if no results come up, it will return error --> go to "except"
        url = 'https://www.europages.co.uk/companies/{}.html'.format(company_search_name)
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')

        company_url = soup.find('a', href=True, attrs={'class': "company-name display-spinner"})['href']

        print(company_url)

        # specifies the path to the chromedriver.exe
        driver = webdriver.Chrome('XXX CHOOSE WEBDRIVER HERE XXX')
        
        driver.get(company_url)

        ### Code block stolen from stackoverflow ###
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.click-tel.icon.icon-telephone"))))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.click-tel.icon.icon-telephone"))).click()
        phone = (WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "info-tel-num"))).get_attribute("innerHTML"))

        print("Name:", company)
        print("Phone Number:", phone)

        try:
            address = driver.find_element_by_tag_name('dd').get_attribute("innerHTML").replace("<pre>","").replace("</pre>","")
        except:
            address = "Not Available"
            
        try:
            country = driver.find_element_by_css_selector('span.upper').get_attribute("innerHTML")
        except:
            country = "Not Available"
        
        
        df = df.append({'Company Name': company, 'URL': company_url, 'Phone Number': phone, 'Address': address, 'Country': country}, ignore_index=True)

        driver.close()
        
    except:
        print("Couldn't find company", company)
        phone = "Not Available"
    
