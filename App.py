"""
Created on Sat May 22 16:21:18 2021

streamlit app working alongside with GetFinvizData.py
"""

import streamlit as st
import GetFinvizData as gf
import GetYahooData as gy

# wrapper function to get required data from finviz
def getInfo(ticker):
    fin_table, desc_table = gf.getFinvizData(ticker)
    
    df_fin = gf.parseFinancials(fin_table)
    df_desc, proper_name = gf.parseDescription(desc_table)
    
    sector_img_url_tail = gf.getSectorURL(df_desc)
    industry_img_url_tail = gf.getIndustryURL(df_desc)
    
    df_fin_display = gf.extractSalientFinancials(df_fin)
    df_desc_display = gf.extractSalientDescription(df_desc)
    
    return sector_img_url_tail, industry_img_url_tail, df_fin_display, df_desc_display, proper_name


# Title
st.title('Get salient info of a stock ticker')

# Body
text = st.text_input('Enter a stock ticker available from Finvzi, e.g., AAPL',
                     max_chars = 5)
button = st.button('Get info from finviz')

if text or button:
    st.spinner('Please wait, working...')
    if gf.checkTicker(text)[0:10] == 'No results':
        st.write('No results found for ' + text.upper())
    else:
        # st.write('Extracting results for ' + text.upper())
        sector, industry, df_f, df_d, name = getInfo(text)
        earningsdate = gy.parseEarningsDate(text)
        st.write(name)
        st.write('Approximate Earnings: {}'.format(earningsdate))
        st.header('Delayed financial info')
        st.write(df_f)
        st.header('Sector > Industry info')
        st.write(df_d)
        st.image(gf.getTickerChart(text),
                 width = 860)
        st.image('https://finviz.com/{}'.format(sector),
                 width = 860)
        st.image('https://finviz.com/{}'.format(industry),
                 width = 860)




