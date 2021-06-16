"""
Created on Sat May 22 15:55:47 2021

Module to scrape Finviz data

"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

# Set up the request headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Pragma': 'no-cache',
    'Referrer': 'https://google.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}


# Level 0 function: check if ticker is in Finviz
def checkTicker(stock_ticker):
    url = 'https://finviz.com/search.ashx?p=' + stock_ticker
    html = requests.post(url, headers = headers).text
    soup = BeautifulSoup(html,'html.parser')
    return soup.find('h4').text.strip()


# Level 0 function: scrape data for a single stock ticker
def getFinvizData(stock_ticker):
    url = 'https://finviz.com/quote.ashx?t=' + stock_ticker
    html = requests.post(url, headers = headers).text
    soup = BeautifulSoup(html,'html.parser')
    
    fin_table = soup.find('table', attrs = {'class': 'snapshot-table2'}) #this is where the meat is
    desc_table = soup.find('table', attrs = {'class': 'fullview-title'}) #gives basic profile info

    return fin_table, desc_table

# Level 0 function: get the stock's chart from finviz
def getTickerChart(stock_ticker):
    url = 'https://charts2.finviz.com/chart.ashx?t=' + stock_ticker
    return url

# Level 1 function: parse financial data in the fin_table
def parseFinancials(fin_table):
    table = fin_table
    main_list = []
    for counter, cell in enumerate(table.find_all('td')):
        if counter % 2 == 0:
            temp_list = []
            temp_list.append(cell.text)
        else:
            temp_list.append(cell.text)
            main_list.append(temp_list)
    
    df_fin = pd.DataFrame(main_list, columns = ['Desc', 'Value'])
    
    return df_fin

# Level 1 function: parse description data - sector | industry | country
def parseDescription(desc_table):
    table = desc_table
    text = table.find('td', attrs = {'class': 'fullview-links'}).text
    temp_list = [i.strip() for i in text.split('|')]
       
    df_desc = pd.DataFrame([['sector','industry','country'], temp_list], index = ['Desc', 'Value']).T
    
    proper_name = table.find('a', attrs = {'class': 'tab-link'}).text
    
    return df_desc, proper_name

# Level 2 function: get the url tail of the ticker's sector chart from df_desc
def getSectorURL(df_desc):
    df_desc = df_desc
    
    #get sector url
    sector = df_desc.iloc[0, 1]
    sector_format = sector.lower().replace(' ', '')
    sector_url = 'https://finviz.com/groups.ashx?g=sector&v=410&o=name'
    sector_html = requests.post(sector_url, headers = headers).text
    sector_soup = BeautifulSoup(sector_html,'html.parser')

    sector_img_url_tail = sector_soup.findAll('img', {'src' : re.compile('{}*'.format(sector_format))})[0].get('src')
    
    return sector_img_url_tail

# Level 2 function: get the url tail of the ticker's industry chart from df_desc
def getIndustryURL(df_desc):
    df_desc = df_desc
    
    #get industry url
    industry = df_desc.iloc[1, 1]
    industry_format = industry.lower().replace(' ', '').replace('&', '').replace('-', '')
    industry_url = 'https://finviz.com/groups.ashx?g=industry&v=410&o=name'
    industry_html = requests.post(industry_url, headers = headers).text
    industry_soup = BeautifulSoup(industry_html,'html.parser')
    
    industry_img_url_tail = industry_soup.findAll('img', {'src' : re.compile('{}*'.format(industry_format))})[0].get('src')
    
    return industry_img_url_tail

# Level 2 function: get salient information out of df_desc
def extractSalientDescription(df_desc):
    df = df_desc
    
    #removing default index / rearranging index for better display
    df.set_index('Desc', inplace = True)
    
    return df

# Level 2 function: get salient information out of df_fin
def extractSalientFinancials(df_fin):
    df_fin = df_fin
    #get salient info
    df = df_fin[df_fin['Desc'].isin(['Index', 
                                     'Market Cap', 
                                     'Price', 
                                     'Prev Close', 
                                     'Avg Volume'
                                     ])]
    #removing default index / rearranging index for better display
    df.set_index('Desc', inplace = True)
    df = df.reindex(['Price',
                     'Prev Close',
                     'Index',
                     'Market Cap',
                     'Avg Volume'
                     ])
    
    return df