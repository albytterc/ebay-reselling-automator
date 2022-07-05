import requests
import json
import sys
import ebay_rest
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
    print(f"eBay's official date and time is {ebay_rest.DateTime.to_string(ebay_rest.DateTime.now())}.\n")

    print("All valid eBay global id values, also known as site ids.")
    print(ebay_rest.Reference.get_global_id_values(), '\n')

    try:
        api = ebay_rest.API(application='sandbox_1', user='sandbox_1', header='US')
    except ebay_rest.Error as error:
        print(f'Error {error.number} is {error.reason}  {error.detail}.\n')
    else:
        try:
            print("The five least expensive iPhone things now for sale on-eBay:")        
            for record in api.buy_browse_search(q='iPhone', sort='price', limit=5):
                if 'record' not in record:
                    pass    # TODO Refer to non-records, they contain optimization information.
                else:
                    item = record['record']
                    print(f"item id: {item['item_id']} {item['item_web_url']}")
        except ebay_rest.Error as error:
            print(f'Error {error.number} is {error.reason} {error.detail}.\n')
        else:
            pass

#    print(help(ebay_rest.API))
#    print(help(ebay_rest.Reference))
#    print(help(ebay_rest.DateTime))
#    print(help(ebay_rest.Error))

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
