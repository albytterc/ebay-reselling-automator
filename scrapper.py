from bs4 import BeautifulSoup
import requests
import json


URL = "https://www.amazon.com/adidas-Entrada-Sweat-Hoodie-X-Small/dp/B093RNCHD7/ref=sr_1_1?pf_rd_i=20939775011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=6a7ab8db-753f-45a5-bf7d-ebd8957d5719&pf_rd_r=JWMGWMX0CBDXMANZ9EKJ&pf_rd_s=merchandised-search-5&pf_rd_t=101&qid=1656696743&s=apparel&sr=1-1&th=1"
# URL = input("Enter product URL: ")


HEADERS = ({'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})
 
webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")




# Extract item name
def get_name():
    title = soup.find("span",attrs={"id":'productTitle'})
    title_value = title.string
    title_string = title_value.strip().replace(',', '')
    return(title_string)


# Extract price
def get_price():
    price = soup.find("span", attrs={"class": 'a-offscreen'})
    price_value = price.string
    return(price_value)


# Extract item description
# TODO: clean up text s
def get_description():
    desc = soup.find("ul", "a-unordered-list a-vertical a-spacing-mini")
    describtion = []
    for i in desc:
        describtion.append(i.string)
    return describtion

# Extract pictures
def get_pictures():
    pic = soup.findAll("span", {"class": "a-button-text"})
    pics = []
    for i in range(len(pic)):
        if pic[i].find('img'):
            pics.append(pic[i].find('img')['src'])
    pics.pop()
    return pics

# #Print color
def get_color():
    color = soup.find("span", attrs={"class": 'selection'})
    color_value = color.string.strip()
    return color_value



# print("name" + get_name())
# print("price" + get_price())
# print("description" + get_description())
# print("Pictures" + get_pictures())
# print("color" + get_color())

# # Print item title and cost
# print(f"Item is {title_string} and it costs {price_value}")

# print("")




# #Print Descriptipn
# for i in desc:
#     describtion.append(i.string)

# print("")
# print("Description")
# for i in describtion:
#     print(i)


# for i in pics:
#     print(i)