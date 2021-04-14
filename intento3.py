import time
import unittest
import pickle
import csv

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
        self.browser = webdriver.Chrome(executable_path=path)


    def login(self, url): #Step One, works?
        print('> Start execution login step <')
        # url = 'https://uber.onelogin.com/login2'
        #Should use the below link but it dosen't work, so I'm using the above one untill I fix the process for image downloading
        #url = 'https://partnertools.uberinternal.com/document/425b6991-0722-4925-9479-d97c3913c9a8'
        self.browser
        self.browser.get(url)
        time.sleep(7)
        self.fill_login_form()
        self.cookies_to_file()
        print('> End execution login step <')

    def fill_login_form(self):
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

    def cookies_to_file(self):
        pickle.dump(self.browser.get_cookies(), open(r"C:\Users\Chris Villarroel\Documents\repo\costaRicaTaxResources\cookies\cookies.pkl","wb")) #Try 2
        time.sleep(4)

    def show_cookies_in_console(self):
        print(f'> Browser Cookies: {self.browser.get_cookies()}')

    def set_cookies(self):
        cookies = pickle.load(open(r"C:\Users\Chris Villarroel\Documents\repo\costaRicaTaxResources\cookies\cookies.pkl","rb"))
        for cookie in cookies:
            self.browser.add_cookie(cookie)

    def download_images(self):
        print('testing to download more images')
        with open(r'C:\Users\Chris Villarroel\Documents\repo\costaRicaTaxResources\pictures\testOne.png', 'wb') as file:
            l = self.browser.find_element_by_xpath('//*[@id="app-container-inner"]/div[3]/div/div[1]/div/img')
            file.write(l.screenshot_as_png)
    
    def read_csv_docs(self):
        filePath = (r'C:\Users\Chris Villarroel\Documents\repo\costaRicaTaxResources\report\report.csv')
        with open(filePath, "r" ) as theFile:
            reader = csv.DictReader(theFile, delimiter=',')
            return reader
        

    def process_image(self):
        print('processing image')
        

    def go_to_file(self, url):
        print('> Start to execution go to file step <')
        # url = 'https://partnertools.uberinternal.com/document/425b6991-0722-4925-9479-d97c3913c9a8'
        self.browser.get(url)
        self.set_cookies()
        self.browser.refresh()
        time.sleep(5)
        self.browser.get(url)
        time.sleep(5)
        self.download_images()
        print('> Finish to execution go to file step <')

    def tearDown(self):
        print('> Last step, cry <')
        self.browser.quit()

    def orchestrator(self):
        dataForTesting = self.read_csv_docs()
        self.login('https://partnertools.uberinternal.com/document/425b6991-0722-4925-9479-d97c3913c9a8')
        for row in dataForTesting:
            docUuid = dataForTesting['document_uuid']
            print(docUuid)
        self.go_to_file('https://partnertools.uberinternal.com/document/425b6991-0722-4925-9479-d97c3913c9a8')
        self.tearDown()



if __name__ == "__main__":
    scrapper = HackerNewsSearchTest(r'C:\Users\Chris Villarroel\Documents\repo\costaRicaTaxResources\driver\chromedriver.exe')
    scrapper.orchestrator()