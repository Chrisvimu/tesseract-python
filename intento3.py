import time
import unittest
import pickle
import csv
import os.path # < -- For checking if the file exists

from os import path # < -- For checking if the file exists
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC #test look where it's used.
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import getpass # < -- IMPORT for login secure pssword

serverUrl = 'http://localhost:4444/wd/hub'
class HackerNewsSearchTest:

    def __init__(self, path):
        print('> Init WebDriver <')
        try:
            self.browser = webdriver.Chrome(executable_path=path)
        except:
            print('An exception occurred')

    def login(self, doc_url): #Step One, works?
        print('> Start execution login step <')
        #Should use the below link but it dosen't work, so I'm using the above one untill I fix the process for image downloading
        try:
            url = 'https://partnertools.uberinternal.com/document/' + doc_url
            self.browser
            self.browser.get(url)
            time.sleep(7)
            self.fill_login_form()
            self.cookies_to_file()
            print('> End execution login step <')
        except:
            print('An exception occurred')

    def fill_login_form(self):
        try:
            search_box = self.browser.find_element_by_id('username')
            search_box.send_keys('christian.vimu@uber.com')
            time.sleep(3)
            #html = self.browser.page_source
            #print('---------------------------------------------------')
            #print(html) # this was to check if the page was working, and username was avaliable
            self.browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[3]/form/div/div[3]/div/button').click()
            time.sleep(6)
            self.browser.find_element_by_xpath('//*[@id="password"]')
            print('found it, going to sleep')
            #This doesn't take into account the manual navigation of the driver, so for now I'll just manually do the Duolingo process
            getpass.getpass("Press Enter after You are done logging in") #Press once inside google to begin scrapping:
            time.sleep(3)
        except:
            print('An exception occurred')

    def cookies_to_file(self):
        try:
            pickle.dump(self.browser.get_cookies(), open(r"C:\Users\Chris Villarroel\Documents\repo\test1\tesseract-python\costaRicaTaxResources\cookies\cookies.pkl","wb")) #Try 2
            time.sleep(4)
        except:
            print('An exception occurred')

    def show_cookies_in_console(self):
        try: 
            print(f'> Browser Cookies: {self.browser.get_cookies()}')
        except:
            print('An exception occurred')

    def set_cookies(self):
        try:
            cookies = pickle.load(open(r"C:\Users\Chris Villarroel\Documents\repo\test1\tesseract-python\costaRicaTaxResources\cookies\cookies.pkl","rb"))
            for cookie in cookies:
                self.browser.add_cookie(cookie)
        except:
            print('An exception occurred')

    def download_images(self, docUuid):
        try:
            print('testing to download more images')
            with open(r'C:\Users\Chris Villarroel\Documents\repo\test1\tesseract-python\costaRicaTaxResources\pictures\\' + docUuid + '.png', 'wb') as file:
                if(self.browser.find_element_by_xpath('//*[@id="app-container-inner"]/div[3]/div/div[1]/div/img')):
                    l = self.browser.find_element_by_xpath('//*[@id="app-container-inner"]/div[3]/div/div[1]/div/img')
                else:
                    print('----------- '+ docUuid +' ----------------')
                file.write(l.screenshot_as_png)
        except:
            print('An exception occurred')
    
    def read_csv_docs(self):
        try:
            filePath = (r'C:\Users\Chris Villarroel\Documents\repo\test1\tesseract-python\costaRicaTaxResources\report\report.csv')
            print('> reading the CSV file <')
            with open(filePath, "r" ) as theFile:
                reader = csv.DictReader(theFile, delimiter=',')

                ordered_dict_from_csv = list(reader)
            return ordered_dict_from_csv
        except:
            print('An exception occurred')
    
    def get_url_doc(self, dataFrame):
        try:
            dataForTesting = dict(dataFrame[0])
            doc_url = dataForTesting['document_uuid']
            return(doc_url)
        except:
            print('An exception occurred')

    def go_to_file(self, dataFrame):
        try:
            print('> Start to execution go to file step <')
            docUuid = self.get_url_doc(dataFrame)
            url = 'https://partnertools.uberinternal.com/document/' + docUuid
            self.browser.get(url)
            self.set_cookies()
            self.browser.refresh()
            time.sleep(5)
            for row in dataFrame:
                docUuid = row['document_uuid']
                if(path.exists(r'C:\Users\Chris Villarroel\Documents\repo\test1\tesseract-python\costaRicaTaxResources\pictures\\' + docUuid + '.png')):
                    print('-----------------Already scrapped----------------')
                    pass                    
                else:
                    url = 'https://partnertools.uberinternal.com/document/' + docUuid
                    self.browser.get(url)
                    time.sleep(3)
                    self.download_images(docUuid)
                    print('--------------------------------------------------------')
            print('> Finish to execution go to file step <')
        except:
            print('An exception occurred')

    def tearDown(self):
        try:
            print('> Last step, cry <')
            self.browser.quit()
        except:
            print('An exception occurred')

    def orchestrator(self):
        try:
            dataFrame = self.read_csv_docs()
            docTest = self.get_url_doc(dataFrame)
            self.login(docTest)
            #till here it's done, I need to do the for and go search the documents in a loop
            self.go_to_file(dataFrame)
            self.tearDown()
        except:
            print('An exception occurred')


if __name__ == "__main__":
    try:
        scrapper = HackerNewsSearchTest(r'C:\Users\Chris Villarroel\Documents\repo\test1\tesseract-python\costaRicaTaxResources\driver\chromedriver.exe')
        scrapper.orchestrator()
    except:
            print('An exception occurred')