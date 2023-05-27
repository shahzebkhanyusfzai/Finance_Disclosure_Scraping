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
from CandidateData import exporter, get_driver

switch = True
def exporter(row):
    file_name = 'CandidateData.csv'
    global switch 
    if switch:
        switch = False
        pd.DataFrame(row,index=[0]).to_csv(file_name,index=False,mode='a')
    else:
        pd.DataFrame(row,index=[0]).to_csv(file_name,index=False,mode='a',header=False)

def get_driver():
    options = Options()
    options.add_argument("--disable-blink-features")
    options.add_argument("start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-logging')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    return driver

def parse():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    csv_file = os.path.join(os.getcwd(), 'Candidate.csv')
    df = pd.read_csv(csv_file)
    links = df.iloc[:,0].tolist()
    for link in links:
        driver.get(link)
        resp = Selector(text=driver.page_source)
        time.sleep(5)
        resp = Selector(text=driver.page_source)
        name = resp.xpath('//div[@class="section-title ng-binding"]/text()').get()
        party = resp.xpath('//span[@class="candidate-type ng-binding"]/text()').get()
        candidate_for = resp.xpath('//a[@class="light-blue-text ng-binding"]/text()  | (//div[@class="black-text mt-xs"]/span/text())[1]').getall()
        candidate_for = ' '.join(candidate_for)
        status = resp.xpath('//div[contains(text(),"Status")]/following-sibling::div/text()').get()
        status = scraper_helper.cleanup(status)
        Address = resp.xpath('//div[contains(text(),"Address")]/following-sibling::div/text()').get()
        Address = scraper_helper.cleanup(Address)
        Phone_no = resp.xpath('//div[contains(text(),"Phone")]/following-sibling::div/text()').get()
        Phone_no = scraper_helper.cleanup(Phone_no)
        Principal_committee = resp.xpath('//div[contains(text(),"Principal")]/following-sibling::div/text()').get()
        Principal_committee = scraper_helper.cleanup(Principal_committee)
        Election = resp.xpath('//div[contains(text(),"Election")]/following-sibling::div/text()').get()
        Election = scraper_helper.cleanup(Election)
        date_reg = resp.xpath('//div[contains(text(),"Date")]/following-sibling::div/text()').get()
        date_reg = scraper_helper.cleanup(date_reg)
        Candidate = resp.xpath('//div[contains(text(),"Candidate")]/following-sibling::div/text()').get()
        Candidate = scraper_helper.cleanup(Candidate)
        Committee_off = resp.xpath('(//div[contains(text(),"Committee Officers")]/following-sibling::div/text())[1]').get()
        Committee_off = scraper_helper.cleanup(Committee_off)
        total_contribution = resp.xpath('//div[contains(text(),"Total Contribution")]/following-sibling::div/text()').get()
        total_contribution = scraper_helper.cleanup(total_contribution)
        total_Exp = resp.xpath('//div[contains(text(),"Total Expend")]/following-sibling::div/text()').get()
        total_Exp = scraper_helper.cleanup(total_Exp)
        Funds = resp.xpath('//div[contains(text(),"Funds")]/following-sibling::div/text()').get()
        Funds = scraper_helper.cleanup(Funds)
        Non_money = resp.xpath('//div[contains(text(),"Non")]/following-sibling::div/text()').get()
        Non_money = scraper_helper.cleanup(Non_money)

        data = {
            'name': name,
            'republican': party,
            'Candidate for': candidate_for,
            'Status': status,
            'Address': Address,
            'Phone No': Phone_no,
            'Principal Committee': Principal_committee,
            'Election': Election,
            'Date Registered': date_reg,
            'Candidate ID': Candidate,
            'Committee Officer': Committee_off,
            'Total Expense': total_Exp,
            'Total Contributions': total_contribution,
            'Total Expenditures': total_contribution,
            'Funds Balance': Funds,
            'Nonmoney Contribution': Non_money,
            'Link': link

        }
        print(data)
        exporter(data)

parse()


       


