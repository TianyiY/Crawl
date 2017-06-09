# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time

browser = webdriver.Firefox()
browser.get('https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?asq=j1%2FH5AOhJ0W3BK%2BWt020EfJQTqC6DkjEgNK47tKSd5A6Yc3t3l9%2F%2BOVQXPmA%2BQww26q94bt1tGnwdDIYSwDVxJLEwz0mKadF1YZiPRWXyaHG5FDY1Dfl9V0tN8fdMJMrkI2OY%2BkVOzT7Yatmd02nyifgl192HCtnaIXBoIK4t%2BriFLZO%2F6LnwagetqA02gMdBp0eoREr2xLYHgqmk0Io4PmQ37H75t9OpMjQpD86dJ%2Fi9gFJ3zoRUUxA1bXicT8i&city=4729&cid=1744603&tag=5536c5aa-eeb4-4b5e-8e0f-cfc3ff07f63f&tick=636325111809&pagetypeid=1&origin=US&gclid=&aid=82364&userId=869576d1-6621-48f7-a1bf-ce3c3ad758bc&languageId=1&sessionId=yk1ysvwb3kd5azty0bzmfrdq&storefrontId=3&currencyCode=USD&htmlLanguage=en-us&trafficType=User&cultureInfoName=en-US&checkIn=2017-06-17&checkOut=2017-06-18&los=1&rooms=1&adults=2&children=0&childages=&priceCur=USD&hotelReviewScore=5&ckuid=869576d1-6621-48f7-a1bf-ce3c3ad758bc')
soup=BeautifulSoup(browser.page_source, "lxml")
while len(soup.select('.btn-right'))>0:
    for i in soup.select('.hotel-info ul li h3'):
        print i.text
    time.sleep(5)
    browser.find_element_by_id("paginationNext").click()
    soup = BeautifulSoup(browser.page_source, "lxml")
browser.close()
