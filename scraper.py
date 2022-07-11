import requests
from bs4 import BeautifulSoup

URL = ""


def set_url():
    global URL
    URL = input("Enter a valid Amazon product URL: ")


HEADERS = ({
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/103.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
})

# Send requests
set_url()
webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")

if webpage.ok:
    # Extract item name
    def get_name():
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.string
        title_string = title_value.strip().replace(',', '')
        return title_string


    # Extract price
    def get_price():
        price = soup.find("span", attrs={"class": 'a-offscreen'})
        price_value = str(price.string)
        return price_value[1:]


    # Extract item description
    def get_description():
        desc = soup.find_all(
            'ul', {"class": "a-unordered-list a-vertical a-spacing-mini"})
        description = []
        for i in desc:
            if i.find_all("span", {"class": "a-list-item"}):
                for j in i:
                    description.append(j.string)

        for i in description:
            if i == '' or i == '\n' or i == ' ':
                description.remove(i)

        # Get rid of None and irrelevant details
        description = [i for i in description if i]
        description.pop(0)

        result_str = "<ul>"
        for line in description:
            result_str += f"<li>{line}</li>"

        return result_str + '</ul>'


    # Extract pictures
    def get_pictures():
        pic = soup.findAll("span", {"class": "a-button-text"})
        pics = []
        for i in range(len(pic)):
            if pic[i].find('img'):
                pics.append(pic[i].find('img')['src'])
        pics.pop()
        return pics


    # Extract Details
    def get_details():
        details = {}

        # Get Key
        key_unfiltered = soup.findAll(
            "span", {"class": "a-size-base a-text-bold"})
        key = []
        for i in key_unfiltered:
            key.append(i.string)

        key = [i for i in key if i]
        key.pop(0)

        # Get Value
        val_unfiltered = soup.findAll("td", {"class": "a-span9"})
        val = []
        for i in val_unfiltered:
            if i.find("span", {"class": "a-size-base"}):
                for j in i:
                    val.append(str(j.string))

        for i in val:
            if i == ' ' or len(i) < 2:
                val.remove(i)

        val = list(filter(str.strip, val))

        # create a dictionary with the key and val
        for i in range(len(key)):
            details[key[i]] = [val[i]]

        return details


    def get_sku():
        unfiltered_sku = soup.find_all("td", {"class": "a-size-base prodDetAttrValue"})
        return str(unfiltered_sku[2].string).strip()

else:
    print("Error with URL")
