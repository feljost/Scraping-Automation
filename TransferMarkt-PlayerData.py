#####################################################
# ----------FOR EDUCATIONAL PURPOSES ONLY-----------#
# This script gathers football player data from     #
# transfermarkt.com                                 #
#                                                   #
# INSTRUCTIONS:                                     #
#     1. Set starting and ending ID (line 93&94)    #
#     2. adjust the proxy (proxy or timeout needed) #
#     3. Run Script :)                              #
#                                                   #
#####################################################

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
from lxml import html
from random import randint
from retry import retry

# initialise
df = pd.DataFrame(columns=[0])
errors = 0


@retry(tries=200, delay=3, jitter=15)
def GetWebsite(i):
   
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    url_i = "https://www.transfermarkt.com/danilo-goiano/profil/spieler/" + str(i)

    # Initialize Beautiful Soup Objects
    headers = {"User-Agent":"Mozilla/5.0"}

    # Try to get the website.
    result = requests.get(url_i, headers=headers, proxies={'https': "https://p.webshare.io:19999"})
    
    if result.status_code != 200:
        errors = errors + 1
        print(f"[{current_time}] Error, Status Code: {result.status_code}")
        print(f"[{current_time}] Error number {errors}")
        
        raise IOError
    else: 
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        print(f"[{current_time}] Website {i} successfully gathered.", end=' ')
    
    return soup, src



def ParseHTML(soup, src, df):
    
    # Find the Name of the player
    try:
        name = soup.find('h1').getText()
    except:
        name = np.nan

    # Find the League of the player
    try:
        league = soup.find('span', class_="mediumpunkt").getText().replace(' ','').replace('\t','').replace('\n','')
        if league == "Lastposition:":
            league = np.nan
    except:
        league = np.nan

    # Find the Max Value of the player
    try:
        max_value = soup.find_all("div", class_="right-td")[-1].getText().replace(' ','').split('\n')[1]
    except:
        max_value = np.nan

    # Get everything we can from the Html table
    df_i = pd.read_html(str(src))[0]

    # Append Name and Value to the previously created datatable
    df_i = df_i.replace(r'\\n','', regex=True)
    df_i = df_i.append([['Full Name',name],['Max Value',max_value], ['League',league],['PlayerID',i]])

    print(f"... Player loaded into DataFrame")

    return df_i



if __name__ == '__main__':
    start = 1  # set starting integer
    end = 2000   # set ending integer
    starttime = time.perf_counter()

    for i in range(start, end):
        
        # Get Website
        Website = GetWebsite(i)
        
        # Scrape out the necessary Infos
        df_i = ParseHTML(soup=Website[0], src=Website[1], df=df)

        # Merge the new table [df_i] to the master table [df]
        df = pd.merge(df, df_i, on=0, how='outer')

        # Save Raw output to Excel File
        df.to_excel('DF_raw.xlsx')
    
        # Save Transformed output to Excel File
        df_t = df.transpose()
        headers = df_t.iloc[0]
        df_t  = pd.DataFrame(df_t.values[1:], columns=headers)
        df_t.to_excel('DF_transformed.xlsx')

    endtime = time.perf_counter()
    print(f'There were {errors} errors in this instance.')
    print(f'Scraping Function Finnished in {round(endtime-starttime,2)} seconds and gathered {end-start} players.')

    print(df)
