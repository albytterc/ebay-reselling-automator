from bs4 import BeautifulSoup
import requests
import json
import re


URL = "https://www.amazon.com/Moto-Power-Unlocked-Smartphone-T-Mobile/dp/B08L5MN4LV/ref=sr_1_14?crid=1VCJ3UG6VQ86N&keywords=motorola+g+power&qid=1657210497&sprefix=motorola+g+power%2Caps%2C222&sr=8-14#renewedProgramDescriptionBtfSection"
# URL = input("Enter product URL: ")


HEADERS = ({'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})
 
# Send requests
webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")

if webpage.ok:



    # Extract item name
    def get_name():
        title = soup.find("span",attrs={"id":'productTitle'})
        title_value = title.string
        title_string = title_value.strip().replace(',', '')
        return(title_string)


    # # Extract price
    def get_price():
        price = soup.find("span", attrs={"class": 'a-offscreen'})
        price_value = price.string
        return(price_value)


    # # Extract item description
    # # TODO: clean up text s
    def get_description():
        desc = soup.find_all('ul', {"class": "a-unordered-list a-vertical a-spacing-mini"})
        describtion = []
        for i in desc:
            if i.find_all("span", {"class": "a-list-item"}):
                for j in i:
                    describtion.append(j.string)
        
        for i in describtion:
            if i == '' or i == '\n' or i == ' ':
                describtion.remove(i)
        
        # Get rid of None and irrelevant details
        describtion = [i for i in describtion if i]
        describtion.pop(0)

        return describtion


    # # Extract pictures
    def get_pictures():
        pic = soup.findAll("span", {"class": "a-button-text"})
        pics = []
        for i in range(len(pic)):
            if pic[i].find('img'):
                pics.append(pic[i].find('img')['src'])
        pics.pop()
        return pics

 
else:
    print("Error with URL")
