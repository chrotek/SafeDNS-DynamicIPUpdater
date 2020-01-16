#!/usr/bin/env python3

import sys
import string
import time
import json
import requests
from pick import pick 
import ast
import signal

def handler(signum, frame):
    print ('Exiting on User Instruction')
    global exitbool
    exitbool=True
    exit(0)

global exitbool
exitbool=False
signal.signal(signal.SIGINT, handler)

def api_key_write():
    try:
        configfile = open("config/apikey","w+")
        api_key = input()
        configfile.write(api_key)
    except IOError:
        print("Couldn't save API Key")
    finally:
        configfile.close()
        api_key_load()

def api_key_load():
    global api_key
    global api_token
    try:
        configfile = open("config/apikey","r")
    except IOError:
        print("Couldn't read API Key. Please input this and press enter")
        api_key_write()
    finally:
        with open('config/apikey', 'r') as file:
            api_key = file.read().replace('\n', '')
    api_token= {
        'Authorization': api_key,
    }
    response=requests.get('https://api.ukfast.io/safedns/v1/zones', headers=api_token)
    if response.status_code == 401:
        print("API Key Invalid! Please enter a new one and press enter:")
        if exitbool == True:
            exit(0)
        api_key_write()
        api_key_load()

def select_domains():
    domain_list = json.loads(json.dumps(requests.get(api_url+"/zones", headers=api_token).json()['data']))
    title = 'Please choose the domains you want to make a dynamic record on: '
    def get_label(option): return option.get('name')
    global selected_domains
    selected_domains = pick(domain_list, title, multi_select=True, indicator='*', options_map_func=get_label)
    return(selected_domains)

def select_subdomains(domain):
    current_subdomain_list = json.loads(json.dumps(requests.get(api_url+"/zones/"+domain+"/records", headers=api_token).json()['data']))
    title = 'Please choose the record you want to make dynamic.'
    def get_label(option): return option.get('name')
    global selected_subdomains
    selected_subdomains = pick(current_subdomain_list, title, multi_select=True, indicator='*', options_map_func=get_label)
    print(selected_subdomains)
    for x in range(len(selected_subdomains)):
        strdata=str(selected_subdomains[x])
        splitdata = strdata.split("'")
        record_id_x=splitdata[2]
        record_id=record_id_x.strip(': , ,')
        record_name=splitdata[5]
        record_type=splitdata[9]
        record_list=[record_id,record_name,record_type]
        print("ID "+record_id)
        print("Name "+record_name)
        print("Type "+record_type)
        print("List "+str(record_list))
        final_record_list[x] = [record_list]


def select_records():
    for domaindata in (select_domains()):
        str_domain_data = str(domaindata)
        split_domain_data = str_domain_data.split("'")
        print(split_domain_data[3])
        select_subdomains(split_domain_data[3])
    print(final_record_list)
    config = json.dumps(final_record_list)
    configfile = open("config/records.json","w+")
    configfile.write( 'records_dict = '+repr(config)+'\n')
    configfile.close()

def check_update_interval():
    try:
        configfile = open("config/update_interval","r")
    except IOError:
        print("Couldn't read Update Interval. Please input a value in minutes and press enter")
        write_update_interval()
    finally:
        with open('config/update_interval', 'r') as file:
            update_interval = file.read().replace('\n', '')
            print("UpdateInterval "+update_interval)

def write_update_interval():
    try:
        configfile = open("config/update_interval","w+")
        update_interval = input()
        configfile.write(update_interval)
    except IOError:
        print("Couldn't save Update Interval")
    finally:
        configfile.close()   
        check_update_interval()

api_url='https://api.ukfast.io/safedns/v1'
final_record_list = {}

##### Some functions commented out for me to test each one. Don't delete them
#api_key_load()
#select_records()
check_update_interval()


# TO - DO
# Check the Update Interval is not greater than the domain's TTL


# NOTES
#
## List Zones
#curl -sX GET https://api.ukfast.io/safedns/v1/zones -H "Authorization: $api_token" | grep -Po '"name":.*?[^\]",' | cut -f4 -d"

###########################
# CODEBIN
# ----------------------
#api_full_response = json.dumps(get_domain_list.json())
#api_full_response_dict = json.loads(api_full_response)

#print (api_full_response_dict['data'])
# -----------------------
# get_domain_list = requests.get('https://api.ukfast.io/safedns/v1/zones', headers=API_TOKEN)

# safedns_domain_list = json.loads(json.dumps(get_domain_list.json()['data']))
# print (safedns_domain_list)
# -----------------------------
# print (type(safedns_domain_list))#
# print (safedns_domain_list[1])
# print (len(safedns_domain_list))

#for x in range(0, (len(safedns_domain_list))):
#    print ("domain: "+str(x)) #DEBUG
#    print (safedns_domain_list[x])
#    safedns_domain_dict = (json.loads(str(json.dumps(safedns_domain_list[x]))))
#    print (safedns_domain_dict['name'])


