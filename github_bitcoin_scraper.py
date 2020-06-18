import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta, date
import time

#get this year
today = datetime.date.today()
this_year = today.year
this_month = today.month    

# set up driver chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)

try:
    # open chrome browser
    browser.get("https://github.com/bitcoin/bitcoin/graphs/commit-activity")
    # wait for fully loaded
    time.sleep(10)
    html = browser.page_source
    # parse into BeautifulSoup object 
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.find(id='commit-activity-master')
    x_axis = section.find("g", {"class": "x axis"})
    ticks = x_axis.findAll("g", {"class": "tick"})
    # print(ticks)
    
    # get first date
    date1 = ticks[0].find("text").get_text()
    month, day = date1.split('/', 1)
    start_date = datetime.date(this_year, int(month), int(day)) 
    
    # get end date
    end_ticks = len(ticks)-1
    date2 = ticks[end_ticks].find("text").get_text()
    month, day = date2.split('/', 1)
    if (this_month <= int(month)) : this_year += 1 
    end_date = datetime.date(this_year, int(month), int(day)) 
    
    # make list of dates
    dates = []
    delta = timedelta(days=1)
    delta2 = timedelta(days=7)
    end_date += delta2
    while start_date <= end_date:
        dates.append(start_date.strftime("%Y-%m-%d"))
        start_date += delta
    # print(len(dates))

    # auto click bar chart element
    # make list of commits value
    commit_vals = []
    bars = browser.find_elements_by_class_name('bar')
    for bar in bars:
        bar.click()
        # print("tes '{}'".format(bar_klik))
        # grab commit values
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        section_detail = soup.find(id='commit-activity-detail')
        dots = section_detail.findAll("g", {"class": "dot"})
        commits = [dot.find("text").get_text() for dot in dots]
        commit_vals += commits
    # print(len(commit_vals))
        
    # finally convert it into csv file (dummy.csv)
    commit_stuff = pd.DataFrame(
        {
            'date': dates,
            'commits': commit_vals,
        })
    
    # print(commit_stuff)
    commit_stuff.to_csv('result.csv', index=False)

finally:
    browser.quit()