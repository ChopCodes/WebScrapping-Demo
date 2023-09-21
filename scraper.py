from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

#Starting URL
starturl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/" 

#Browser/Client Path address for selenium
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")

#Telling Client to get StartURL
browser.get(starturl)

#Empty Array for planet data to be stored
planetdata = []

#A Function to scrap() details
def scrap():
    #First For Loop to get data of first 10 lisitngs in starturl
    for i in range(0,10):
        #Intizializing Soup
        ##browser.page_source is the HTML source code of the current page in your browser (client)
        ## a parser is a component that processes input data to convert it into a format that is easier for the computer to understand1
        soup = BeautifulSoup(browser.page_source,"html.parser")
        #getting data according from UL tags in for loop
        for ultag in soup.find_all("ul",attrs={"class","exoplanet"}):
            litags = ultag.find_all("li")
            templist = []
            #for loop for getting the data from the index[0]
            for index,litag in enumerate(litags):
                if index == 0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
        #append data in planetdata variable
        planetdata.append(templist)
    # Click on the next page button to scrape data from the next page
    browser.find_element(by=By.XPath,value='//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
scrap()

#creation for .csv file
headers=["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]
planetdf = pd.DataFrame(planetdata,columns=headers)
planetdf.to_csv('scrapped_data.csv',index = True,index_label="id")