import ebay_api
import scrapper
from ebay_rest import DateTime, Error, Reference
import ebay_rest.a_p_i as ebay


# TODOS:
# setup beautifulsoup with headers
# get webpage with get request
# pass webpage response to beautiful soup
# setup authentication with the ebay api (oauth2.0)
# get access tokens, application and user
# Ask user for URL
# extract data from url with get request
# prepare data for post request
# send post request to ebay with listing data
# save details into sql database


def set_item_data():
    item_data = {
        "condition": "USED_GOOD",
        "packageWeightAndSize": {
            "dimensions": {
                "height": 6,
                "length": 2,
                "width": 1,
                "unit": "INCH"
            },
            "weight": {
                "value": 1,
                "unit": "POUND"
            }
        },
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 1
            }
        }
    }

    item_data['product'] = {}
    product_info = item_data['product']
    product_info['title'] = scrapper.get_name()[:79]
    product_info['aspects'] = scrapper.get_details()
    product_info['imageURLs'] = scrapper.get_pictures()
    product_info['imageURLs'][0] = 'https://m.media-amazon.com/images/I/61XOOWH7pCL._AC_SL1000_.jpg'

    return item_data


def main():
    # scrapper.set_url()
    try:
        api = ebay.API(application='sandbox_1', user='sandbox_1', header='US')
    except Error as error:
        print(f'Error {error.number} is {error.reason}  {error.detail}.\n')
    else:

        item_data = set_item_data()

        sku = "MO20USBLUN"

        offer_data = {
            "sku": sku,
            "marketplaceId": "EBAY_US",
            "format": "FIXED_PRICE",
            "availableQuantity": 1,
            "categoryId": "30120",
            "listingDescription": scrapper.get_description(),
            "listingPolicies": {
                "fulfillmentPolicyId": "3*********0",
                "paymentPolicyId": "3*********0",
                "returnPolicyId": "3*********0"
            },
            "pricingSummary": {
                "price": {
                    "currency": "USD",
                    "value": scrapper.get_price()
                }
            },
            "quantityLimitPerBuyer": 1,
            "includeCatalogProductDetails": True,
        }

        merchant_location_data = {
            "location": {
                "address": {
                    "addressLine1": "625 6th Ave",
                    "addressLine2": "Fl 2",
                    "city": "New York",
                    "stateOrProvince": "NY",
                    "postalCode": "10011",
                    "country": "US"
                }
            },
            "locationInstructions": "Items ship from here.",
            "name": "Cell Phone Vendor 6th Ave",
            "merchantLocationStatus": "ENABLED",
            "locationTypes": [
                "STORE"
            ]
        }
        merchant_loc_key = 'NYCLOC6TH'

        ebay_api.create_listing(api, sku, item_data, offer_data, merchant_location_data, merchant_loc_key)


if __name__ == '__main__':
    main()
