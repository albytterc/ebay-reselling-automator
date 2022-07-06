from bs4 import BeautifulSoup
import requests
import json


URL = "https://www.amazon.com/adidas-Entrada-Sweat-Hoodie-X-Small/dp/B093RDYKDW/ref=sr_1_1?pf_rd_i=20939775011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=6a7ab8db-753f-45a5-bf7d-ebd8957d5719&pf_rd_r=JWMGWMX0CBDXMANZ9EKJ&pf_rd_s=merchandised-search-5&pf_rd_t=101&qid=1656696743&s=apparel&sr=1-1&th=1"
# URL = input("Enter product URL: ")


HEADERS = ({'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})
 
webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")


# Extract item name
title = soup.find("span",attrs={"id":'productTitle'})
title_value = title.string
title_string = title_value.strip().replace(',', '')


# Extract price
price = soup.find("span", attrs={"class": 'a-offscreen'})
price_value = price.string


# Extract item description
desc = soup.find("ul", "a-unordered-list a-vertical a-spacing-mini")




# Print item title and cost
print(f"Item is {title_string} and it costs {price_value}")

print("")

#Print color
color = soup.find("span", attrs={"class": 'selection'})
color_value = color.string.strip()
print(f" Color is {color_value}")

describtion = []

#Print Descriptipn
for i in desc:
    describtion.append(i.string)

print("Description")
for i in describtion:
    print(i)
