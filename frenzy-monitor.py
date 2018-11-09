# import the necessary python packages to create a monitor 
# proxymanager makes using proxies really easy
# requests is needed so that we can make requests to the www!
from proxymanager import ProxyManager
from datetime import datetime
import requests
import json
import time

# this api url is a given. normally you will have to do some "hunting" for api URLs on certain sites.
url = 'https://frenzy.shopifyapps.com/api/flashsales'

# discord webhook to send your message to
webhook = 'https://discordapp.com/api/webhooks/437424451890577422/xzJuZAkw8ZKIQmE1KrnuRmHkn_Y9WLpeLbTuvoQKPJetzQsGvDGQFQVfCMWAYCMuoyjC'

# a list that will store all current item ids that were found
items = []

# import proxies from your proxies.txt file through the proxymanager package
proxy_manager = ProxyManager('proxies.txt')

# initialize the data for the site, get all the current ids
def initialize(url):
    proxydict = proxy_manager.next_proxy()
    proxies = proxydict.get_dict()
    try:
        # send a request and get all the data from this URL
        r = requests.get(url, proxies=proxies)
        data = json.loads(r.text)
        
        # you will have to know how to read throuh json or dicts in python
        # in order to traverse through the data. you can find examples online
        for sale in data['flashsales']:
            # storing all ids found in the URL to our list of items
            id = sale['id']
            items.append(id)
        print('[' + time.strftime("%I:%M:%S") + '] - Initialized frenzy')
    except:
        pass

def monitor(url):
    proxydict = proxy_manager.next_proxy()
    proxies = proxydict.get_dict()
    while True:
        try:
            r = requests.get(url, proxies=proxies)
            data = json.loads(r.text)
            for sale in data['flashsales']:
                id = sale['id']
                if id not in items:
                # if the id is not in our list of items, then this means
                # that it is a new item! we want to get the details
                    items.append(id)
                    title = sale['title']
                    image = sale['image_urls'][0]
                    description = sale['shop']['name']
                    available = sale['started_at']
                    dropzone = sale['dropzone']
                    pickuponly = sale['pickup']
                    if dropzone == []:
                        dropzone = 'Worldwide'
                    else:
                        dropzone =  (str(dropzone[0]['lat'] + ', ' + str(dropzone[0]['lng']))
                    print("New item found:",title, image, desc, available, dropzone)
            time.sleep(5)
        except:
            pass
        
initialize(url)
monitor(url)
