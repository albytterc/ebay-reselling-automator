import requests
import json
import sys
from ebay_rest import DateTime, Error, Reference
import ebay_rest.a_p_i as ebay_api
import copy


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

def get_merchant_key(api):
    for loc in api.sell_inventory_get_inventory_locations():
        if 'record' in loc:
            loc_obj = loc['record']
            loc_key = loc_obj['merchant_location_key']
            return loc_key
    return None


def create_inventory_location(api):
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
    try:
        api.sell_inventory_create_inventory_location(body=merchant_location_data, merchant_location_key=merchant_loc_key)
    except Error:
        pass



def create_inventory_item(api):
    item_data = {
        "product": {
            "title": "Motorola G Power",
            "description": "Smartphone from 2020. Used, but in great condition. No scratches or marks.",
            "aspects": {
                "Features": ["3D Depth Sensor", "Accelerometer"],
                "Operating System": ["Android"]
            },
            "brand": "Motorola",
            "mpn": "Moto G Power",
            "imageUrls": [
                "https://i.ebayimg.com/images/g/sncAAOSwfzBiOYiR/s-l1600.jpg",
                "https://i.ebayimg.com/images/g/S0sAAOSwQaFiOYiS/s-l500.jpg"
            ]
        },
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

    api.sell_inventory_create_or_replace_inventory_item(body=item_data, content_language="en-US",
                                                        sku="MO20USBLVE")


# sets fulfillment, payment, and return policies.
# Returns a dictionary of the three policy ids
def get_account_policies(api):

    fulfillment_policy_data = {
        "categoryTypes": [
            {
                "name": "ALL_EXCLUDING_MOTORS_VEHICLES"
            }
        ],
        "marketplaceId": "EBAY_US",
        "name": "Domestic free shipping",
        "handlingTime": {
            "unit": "DAY",
            "value": "1"
        },
        "shippingOptions": [
            {
                "costType": "FLAT_RATE",
                "optionType": "DOMESTIC",
                "shippingServices": [
                    {
                        "buyerResponsibleForShipping": "false",
                        "freeShipping": "true",
                        "shippingCarrierCode": "USPS",
                        "shippingServiceCode": "USPSPriorityFlatRateBox"
                    }
                ]
            }
        ]
    }

    fulfillment_policy = api.sell_account_get_fulfillment_policy_by_name("EBAY_US", "Domestic free shipping")
    fulfillment_policy_id = fulfillment_policy["fulfillment_policy_id"]


    payment_policy_request = {
        "name": "default payment policy",
        "marketplaceId": "EBAY_US",
        "categoryTypes": [
            {
                "name": "ALL_EXCLUDING_MOTORS_VEHICLES",
                "default": True
            }
        ],
        "paymentMethods": [
            {
                "paymentMethodType": "PERSONAL_CHECK"
            }
        ]
    }

    payment_policy_response = api.sell_account_get_payment_policy_by_name("EBAY_US", "default payment policy")
    payment_policy_id = payment_policy_response["payment_policy_id"]

    return_policy_request = {
        "name": "no returns",
        "marketplaceId": "EBAY_US",
        "returnsAccepted": False
    }

    # return_policy_response = api.sell_account_create_return_policy(return_policy_request)
    return_policy_response = api.sell_account_get_return_policy_by_name("EBAY_US", "no returns")
    return_policy_id = return_policy_response["return_policy_id"]

    policy_ids = {
        'fulfillmentPolicyId': fulfillment_policy_id,
        'paymentPolicyId': payment_policy_id,
        'returnPolicyId': return_policy_id
    }

    return policy_ids


def get_offer_id(offer_response):
    for item in offer_response:
        if 'record' in item:
            return item['record']['offer_id']


# Creates offer if not already made
# always returns offer id, either of newly created offer, or of already existing offer based on item SKU
def create_offer(api):
    policy_dict = get_account_policies(api)

    offer_data = {
        "sku": "MO20USBLVE",
        "marketplaceId": "EBAY_US",
        "format": "FIXED_PRICE",
        "availableQuantity": 1,
        "categoryId": "30120",
        "listingDescription": "test",
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
        "includeCatalogProductDetails": True,
    }

    offer_data["listingPolicies"].update(policy_dict)
    offer_data['merchantLocationKey'] = get_merchant_key(api)

    try :
        response = api.sell_inventory_create_offer(body=offer_data, content_language="en-US")
        return response['offer_id']
    except Error:
        return get_offer_id(api.sell_inventory_get_offers(sku=offer_data['sku']))

# delete all inventory items and locations, also any offers
def clear_entity(api):
    # accessors = []
    # entity_list = None
    # if entity == 'item':
    #     entity_list = api.sell_inventory_get_inventory_items()
    # elif entity == 'location':
    #     entity_list = api.sell_inventory_get_inventory_locations()
    # elif entity == 'offer':
    #     entity_list = api.sell_inventory_get_offers(accessor)
    #
    # for ent in entity_list:

    # to delete item, use sku
    item_skus = []
    for item in api.sell_inventory_get_inventory_items():
        if 'record' in item:
            item_obj = item['record']
            item_sku = item_obj['sku']
            item_skus.append(item_sku)

    for sku in item_skus:
        api.sell_inventory_delete_inventory_item(sku)

    # to delete location, use merchant_location_key
    loc_keys = []
    for loc in api.sell_inventory_get_inventory_locations():
        if 'record' in loc:
            loc_obj = loc['record']
            loc_key = loc_obj['merchant_location_key']
            loc_keys.append(loc_key)

    for key in loc_keys:
        api.sell_inventory_delete_inventory_location(key)

    # to delete offer, use offer_id
    '''
    try:
        for sku in item_skus:
            for offer in api.sell_inventory_get_offers(sku=sku):
                if 'record' in offer:
                    print(offer)
    except Error as error:
        print(f'Error {error.number} is {error.reason}  {error.detail}.\n')
    '''


def test_api_call():

    try:
        api = ebay_api.API(application='sandbox_1', user='sandbox_1', header='US')
    except Error as error:
        print(f'Error {error.number} is {error.reason}  {error.detail}.\n')
    else:
        try:
            print("Starting...")
            create_inventory_location(api)
            create_inventory_item(api)
            offer_resp = create_offer(api)
            publish_resp = api.sell_inventory_publish_offer(offer_id=offer_resp)
            print(publish_resp)

        except Error as error:
            print(f'Error {error.number} is {error.reason} {error.detail}.\n')
        else:
            pass


def driver():
    test_api_call()


driver()



