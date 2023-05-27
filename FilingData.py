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
from CandidateData import get_driver

switch = True
def exporter(row):
    file_name = 'FilingData.csv'
    global switch 
    if switch:
        switch = False
        pd.DataFrame(row,index=[0]).to_csv(file_name,index=False,mode='a')
    else:
        pd.DataFrame(row,index=[0]).to_csv(file_name,index=False,mode='a',header=False)

def cleanmylist(mylist):
    print('//////////////')
    print(type(mylist))
    print('//////////')
    clean_list = []

    for el in mylist:
        print(el)
        el = scraper_helper.cleanup(el)
        clean_list.append(el)
    print(clean_list)
    return clean_list

# Special_el is designed for the data fields in the columns as Amended and Document Image, as there is no text, but an icon, so this function replaces the icon with text true of empty string

def special_el(mylist):
    cleanlist = []
    for el in mylist:
        if 'class="material-icons colored ng-scope"' in el:
            el = 'true'
            cleanlist.append(el)
        else:
            el = ''
            cleanlist.append(el)
    return cleanlist

# Main function parse, which controls or runs the whole program with the help of other functions
def parse():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    csv_file = os.path.join(os.getcwd(), 'finance_links.csv')
    df = pd.read_csv(csv_file)
    links = df.iloc[:,0].tolist()

    for link in links:
        driver.get(link)

        resp = Selector(text=driver.page_source)
        time.sleep(3)
        wait = WebDriverWait(driver, 15) 
        Filing_Btn = wait.until(EC.element_to_be_clickable((By.XPATH, '(//md-tab-item)[4]')))

        time.sleep(3)
        Filing_Btn.click()
        time.sleep(1)
        resp = Selector(text=driver.page_source)
        
        try:
            more_val = wait.until(EC.element_to_be_clickable((By.XPATH, '(//span[@class="md-select-icon"])[1]')))
            more_val.click()
            fifty_opt = wait.until(EC.element_to_be_clickable((By.XPATH, '(//md-content[@class="_md"]/md-option[@class="ng-scope"])[4]')))
            fifty_opt.click()
        except (NoSuchElementException, ElementNotInteractableException, TimeoutException,ElementClickInterceptedException) :
            print(link)
            pass

        resp = Selector(text=driver.page_source)

        # time.sleep(1)

        # More_btns = driver.find_elements(By.XPATH,'//td[@class="md-cell"][position() mod 2=1]/a/i[@class="material-icons ng-scope"]')
        # try:
        #     for btn in More_btns:
        #         btn.click()
        #         time.sleep(1)
        # except NoSuchElementException:
        #     pass    

        # resp = Selector(text=driver.page_source)
      
        Candidate = resp.xpath('//div[contains(text(),"Candidate")]/following-sibling::div/text()').get()
        Candidate = scraper_helper.cleanup(Candidate)
        ReportName = resp.xpath('//td[@class="text-left light-blue-text  md-cell"]/a/text() | //td[@class="text-left md-cell"]/a/text()').getall()
        ReportName = cleanmylist(ReportName)
        ReportLink = resp.xpath('//td[@class="text-left light-blue-text  md-cell"]/a[@class="light-blue-text ng-binding ng-scope"]/@href | //td[@class="text-left md-cell"]/a/@href').getall()
        ReportLink = cleanmylist(ReportLink)
        ReportType = resp.xpath('//td[@class="text-left md-cell ng-binding ng-scope"]/text()').getall()
        ReportType = cleanmylist(ReportType)
        StartOfPeriod = resp.xpath('(//td[@class="text-left md-cell ng-scope"]/span[@class="ng-binding ng-scope"]/text())[position() mod 4=1]').getall()
        StartOfPeriod = cleanmylist(StartOfPeriod)
        EndOfPeriod = resp.xpath('(//td[@class="text-left md-cell ng-scope"]/span[@class="ng-binding ng-scope"]/text())[position() mod 4 =2]').getall()
        EndOfPeriod = cleanmylist(EndOfPeriod)
        DueDate = resp.xpath('(//td[@class="text-left md-cell ng-scope"]/span[@class="ng-binding ng-scope"]/text())[position() mod 4 =3]').getall()
        DueDate = cleanmylist(DueDate)
        FiledDate = resp.xpath('(//td[@class="text-left md-cell ng-scope"]/span[@class="ng-binding ng-scope"])[position() mod 4 =0]/text()').getall()
        FiledDate = cleanmylist(FiledDate)
        Amended = resp.xpath('(//td[@class="text-left md-cell ng-scope"])[position() mod 6 = 5] ').getall()
        Amended = special_el(Amended)
        DocumentImage = resp.xpath('(//td[@class="text-left md-cell ng-scope"])[position () mod 6 = 0]').getall()
        DocumentImage = special_el(DocumentImage)
        Year = resp.xpath('//td[@class="text-right md-cell ng-binding ng-scope"]/text()').getall()
        Year = cleanmylist(Year)
        iteration = len(ReportName)

        for x in range(iteration):
            print(ReportName[x])
            data= {
                'link': link,
                'candidate': Candidate,
                'ReportName': ReportName[x],
                'ReportLink': ReportLink[x],
                'reportType': ReportType[x],
                'start of period': StartOfPeriod[x],
                'End of period': EndOfPeriod[x],
                'Due Date': DueDate[x],
                'Filed Date': FiledDate[x],
                'amended': Amended[x],
                'document image': DocumentImage[x],
                'Year': Year[x],
            }
            exporter(data)
            print(data)
            x+=1
parse()






       


