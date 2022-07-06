import requests
import json
import sys
from ebay_rest import DateTime, Error, Reference
import ebay_rest.a_p_i as ebay_api
import ebay_rest.api.sell_inventory.api.inventory_item_api as inv
from bs4 import BeautifulSoup

# setup beautifulsoup with headers
# get webpage with get request
# pass webpage response to beautiful soup
# setup authentication with the ebay api (oauth2.0)

'''
config_path = "/home/codio/workspace/ebay-oauth-python-client/test/config/ebay-config-sample.json"
  my_scopes = [
      "https://api.ebay.com/oauth/api_scope",
      "https://api.ebay.com/oauth/api_scope/sell.inventory", 
      "https://api.ebay.com/oauth/api_scope/sell.account"
  ]
  credentialutil.load(config_path)

  oauth.generate_user_authorization_url(env_type=environment.SANDBOX, scopes=my_scopes)
  app_token = oauth.get_application_token(env_type=environment.SANDBOX, scopes=my_scopes)
  user_token = oauth.get_access_token(env_type=environment.SANDBOX, refresh_token=app_token, scopes=my_scopes)

 print(f"my app token {app_token}")
 header = {
     "Content-Type": "application/x-www-form-urlencoded",
     "Authorization": "Basic "
 }

 with open(config_path) as auth_file:
     auth_data = json.load(auth_file)

 url = f"https://api.sandbox.ebay.com/identity/v1/oauth2/{app_token}"
'''


def test_api_call():
    print(f"eBay's official date and time is {DateTime.to_string(DateTime.now())}.\n")

    print("All valid eBay global id values, also known as site ids.")
    print(Reference.get_global_id_values(), '\n')

    try:
        api = ebay_api.API(application='sandbox_1', user='sandbox_1', header='US')
    except Error as error:
        print(f'Error {error.number} is {error.reason}  {error.detail}.\n')
    else:
        try:
            # print("The five least expensive iPhone things now for sale on-eBay:")
            #
            # for record in api.buy_browse_search(q='iPhone', sort='price', limit=5):
            #     if 'record' not in record:
            #     else:
            #         item = record['record']
            #         print(f"item id: {item['item_id']} {item['item_web_url']}")

            item_data = {

                "product": {

                    "title": "Test listing - do not bid or buy - awesome Apple watch test 2",

                    "aspects": {

                        "Feature": ["Water resistance", "GPS"],

                        "CPU": ["Dual-Core Processor"]

                    },

                    "description": "Test listing - do not bid or buy \n Built-in GPS. Water resistance to 50 meters.1 A new lightning-fast dual-core processor. And a display that\u2019s two times brighter than before. Full of features that help you stay active, motivated, and connected, Apple Watch Series 2 is designed for all the ways you move ",

                    "upc": ["888462079525"],

                    "imageUrls": [

                        "http://store.storeimages.cdn-apple.com/4973/as-images.apple.com/is/image/AppleInc/aos/published/images/S/1/S1/42/S1-42-alu-silver-sport-white-grid?wid=332&hei=392&fmt=jpeg&qlt=95&op_sharpen=0&resMode=bicub&op_usm=0.5,0.5,0,0&iccEmbed=0&layer=comp&.v=1472247758975",

                        "http://store.storeimages.cdn-apple.com/4973/as-images.apple.com/is/image/AppleInc/aos/published/images/4/2/42/stainless/42-stainless-sport-white-grid?wid=332&hei=392&fmt=jpeg&qlt=95&op_sharpen=0&resMode=bicub&op_usm=0.5,0.5,0,0&iccEmbed=0&layer=comp&.v=1472247760390",

                        "http://store.storeimages.cdn-apple.com/4973/as-images.apple.com/is/image/AppleInc/aos/published/images/4/2/42/ceramic/42-ceramic-sport-cloud-grid?wid=332&hei=392&fmt=jpeg&qlt=95&op_sharpen=0&resMode=bicub&op_usm=0.5,0.5,0,0&iccEmbed=0&layer=comp&.v=1472247758007"

                    ]

                },

                "condition": "NEW",

                "packageWeightAndSize": {

                    "dimensions": {

                        "height": 5,

                        "length": 10,

                        "width": 15,

                        "unit": "INCH"

                    },

                    "packageType": "MAILING_BOX",

                    "weight": {

                        "value": 2,

                        "unit": "POUND"

                    }

                },

                "availability": {

                    "shipToLocationAvailability": {

                        "quantity": 10

                    }

                }

            }

            api.sell_inventory_create_or_replace_inventory_item(body=item_data, content_language="en-US",
                                                                sku="3B1QM5L80B")
            api.sell_

            merchant_location_key = {

                "location": {

                    "address": {

                        "addressLine1": "2********e",

                        "addressLine2": "B********3",

                        "city": "S*****e",

                        "stateOrProvince": "**",

                        "postalCode": "9***5",

                        "country": "US"

                    }

                },

                "locationInstructions": "Items ship from here.",

                "name": "W********1",

                "merchantLocationStatus": "ENABLED",

                "locationTypes": [

                    "WAREHOUSE"

                ]

            }

            api.sell_inventory_delete_inventory_location(merchant_location_key=merchant_location_key['name'])

            api.sell_inventory_create_inventory_location(body=merchant_location_key,
                                                         merchant_location_key=merchant_location_key['name'])

            print("LOCATIONS")
            for loc in api.sell_inventory_get_inventory_locations():
                print(json.dumps(loc, indent=2))

            print("ITEMS")
            for item in api.sell_inventory_get_inventory_items():
                print(json.dumps(item, indent=2))

            offer_data = {
                "sku": "sk12315516321",
                "marketplaceId": "EBAY_US",
                "format": "FIXED_PRICE",
                "availableQuantity": 75,
                "categoryId": "30120",
                "listingDescription": "Lumia phone with a stunning 5.7 inch Quad HD display and a powerful octa-core processor.",
                "listingPolicies": {
                    "fulfillmentPolicyId": "3*********0",
                    "paymentPolicyId": "3*********0",
                    "returnPolicyId": "3*********0"
                },
                "pricingSummary": {
                    "price": {
                        "currency": "USD",
                        "value": "272.17"
                    }
                },
                "quantityLimitPerBuyer": 2,
                "includeCatalogProductDetails": True
            }

            # THIS LINE BELOW DOESN'T WORK BECAUSE IT NEEDS A VALID FULFILLMENTPOLICYID
            api.sell_inventory_create_offer(body=offer_data, content_language="en-US")


        except Error as error:
            print(f'Error {error.number} is {error.reason} {error.detail}.\n')
        else:
            pass


#    print(help(ebay.API))
#    print(help(ebay.Reference))
#    print(help(ebay.DateTime))
#    print(help(ebay.Error))

# get access tokens, application and user
# Ask user for URL 
# extract data from url with get request
# prepare data for post request 
# send post request to ebay with listing data
# save details into sql database


def main():
    test_api_call()


if __name__ == '__main__':
    main()
