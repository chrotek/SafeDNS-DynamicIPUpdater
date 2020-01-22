#!/usr/bin/env python3

import sys
import string
import time
import json
import requests
from requests import get
from pick import pick
import ast
import signal
import dns.resolver
import re
import configparser
from datetime import datetime

config = configparser.ConfigParser()

api_url='https://api.ukfast.io/safedns/v1'

now = datetime.now()
final_record_list = {}
api_key_loaded = False
selected_records_loaded = False
update_interval_loaded = False
record_needs_update=False
query_ip_address=dns.resolver.query("myip.opendns.com", "A")
for rdata in query_ip_address:
    current_ip = rdata.address

# uncomment this line to force an update with a fake IP. Good for testing config and debugging
# current_ip="1.2.3.4"


def handler(signum, frame):
    print ('Exiting on CTRL+C')
    global exitbool
    exitbool=True
    sys.exit(130)

global exitbool
exitbool=False
signal.signal(signal.SIGINT, handler)



def api_key_load():
    global api_token
    config.read('config.ini')
    api_key = config['API']['key']   
    global api_key_loaded
    api_key_loaded = True
    api_token= {
        'Authorization': api_key,
    }
    response=requests.get(api_url+"/zones", headers=api_token)
    if response.status_code == 401:
        print("API Key Invalid! Please run config script")
        sys.exit(1)

def load_records_config():
    config.read('config.ini')
    for key in config['RECORDS']:
        final_record_list[key] = config['RECORDS'][key]
        global selected_records_loaded
        selected_records_loaded = True 


def loop_over_records_template():
    for x in final_record_list:
        record=str(final_record_list[x]).split(",")
        record_id=record[0].strip("[,'")
        record_name=record[1].replace("'","")
        record_type=record[2].replace("'","").replace("]","")
        print("ID: "+record_id+" Name: "+record_name+" Type: "+record_type)


def loopdomains():
    records_to_update=[]
    for x in final_record_list:
        record=str(final_record_list[x]).split(",")
        record_id=record[0].replace("'","").replace("[","")
        record_name=record[1].replace("'","").replace(" ","")
        record_type=record[2].replace(" ","").replace("'","").replace("[","")
        record_zone=record[3].replace(" ","").replace("'","").replace("]","")
        query_record_ip=json.loads(json.dumps(requests.get(api_url+"/zones/"+record_zone+"/records/"+record_id, headers=api_token).json()['data'])) 
        record_ip=query_record_ip["content"]
        if (current_ip != record_ip):
            global record_needs_update
            record_needs_update=True
            records_to_update.append(record)

        for y in records_to_update:
            record_id_to_update=y[0].replace("'","").replace("[","")
            record_name_to_update=y[1].replace("'","").replace(" ","")
            record_type_to_update=y[2].replace(" ","").replace("'","").replace("[","")
            record_zone_to_update=y[3].replace(" ","").replace("'","").replace("]","")         
            postdata = {
            'name':record_name_to_update, 
            'type':record_type_to_update, 
            'content':current_ip
            }
            api_response=requests.patch(api_url+"/zones/"+record_zone+"/records/"+record_id, headers=api_token, data=postdata)
            if api_response.status_code == 200:
                print("Updated "+record_name+"\t"+record_type+" record , to match current IP "+current_ip+" Instead of "+record_ip)
            else:
                print("API Issue. Status Code "+str(api_response.status_code))
                sys.exit(1)
    if record_needs_update == False:
        print("All domains already have our current IP, So no updates nescessary")


print("Running Checks at "+now.strftime("%H:%M:%S")+" On "+now.strftime("%d/%m/%Y"))
api_key_load()
load_records_config()
loopdomains()
print("------------------------------------------------------------------------")
