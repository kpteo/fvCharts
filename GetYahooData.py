"""
Created on Wed Jun 16 22:55:47 2021

Module to scrape Yahoo data

"""

from bs4 import BeautifulSoup
import requests


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

def readFinancialsYahoo(stock_ticker):
    url = 'https://finance.yahoo.com/quote/' + stock_ticker
    html = requests.get(url, headers).text
    soup = BeautifulSoup(html,'html.parser')
    
    table = soup.find('table', attrs = {'class': 'W(100%) M(0) Bdcl(c)'})

    return table

def parseEarningsDate(stock_ticker):
    table = readFinancialsYahoo(stock_ticker)
    info = table.find('td', attrs = {'data-test': 'EARNINGS_DATE-value'})
    earnings = info.text
    
    # simple error handling for ticker without earnings like ETF
    if info is None:
        earnings = 'no earnings date found'
    
    return earnings