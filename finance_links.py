import scrapy
from selenium import webdriver
from scrapy import selector
import pandas as pd
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from scrapy.selector import Selector
import scraper_helper
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException, ElementClickInterceptedException
from math import ceil
from CandidateData import get_driver  


def iterNum(total_el):
    total_el = scraper_helper.cleanup(total_el)
    total_el = total_el.split()[-1]
    total_el = int(total_el)
    total_el = total_el/10
    myIter = round(total_el)
    print(myIter)
    return myIter


links = []

def extract_links():
    global driver
    resp = Selector(text=driver.page_source)
    mylinks = resp.xpath('//td[@class="text-left md-cell"]/a/@href').getall()
    wait = WebDriverWait(driver, 120)
    time.sleep(40)
    resp = Selector(text=driver.page_source)
    Next_page = wait.until(EC.element_to_be_clickable((By.XPATH,'(//button/md-icon[@class="ng-scope"])[2]')))
    Next_page.click()
    for lnk in mylinks:
        links.append(lnk)

def parse():
    global driver    
    link = 'https://financial-disclosures.sos.arkansas.gov/index.html#/explore/candidate'
    driver.get(link)
    time.sleep(10) 
    wait = WebDriverWait(driver, 15)
    resp = Selector(text=driver.page_source)
    Filter_Btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//li/button[contains(text(),"Clear Filter")]')))
    Filter_Btn.click()

    total_el = resp.xpath('(//span[@class="label ng-binding"]/text())[2]').get()
    myIter = iterNum(total_el)
    for x in range(myIter):
        extract_links()



 
driver = get_driver()
parse()
df = pd.DataFrame(links)
df.to_csv('finance_links.csv', index=False)






       


