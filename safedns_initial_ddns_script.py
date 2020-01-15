#!/usr/bin/env python3

import sys
import string
import time
import json
import requests
from pick import pick 


def api_key_write():
    try:
        f = open("config/apikey","w+")
        api_key = input()
        f.write(api_key)
        f.close()
    except IOError:
        print("Couldn't save API Key")
    finally:
        f.close()

def api_key_load():

    try:
        f = open("config/apikey")
        # Do something with the file
        print(f.readlines())
    
    except IOError:
        api_key_write()
    finally:
        f.close()
    
    response=requests.get('https://api.ukfast.io/safedns/v1/zones', headers=api_token)
    print(response.status_code)
    if response.status_code == 401:
        print("API Key Invalid! Please enter a new one and press enter:")
        api_key_write()
        api_key_load()

api_token= {
    'Authorization': '---lz2lkW8cmEGSIUhC0JnIkouhhiPYB8WM',
}
api_url='https://api.ukfast.io/safedns/v1'

api_key_load()

# API Key functions work, but add extra characters to the key. the below code is fine, just not running becuase i'm teasting the above, i'm going to bed now. nighty night                  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

sys.exit(0)


final_record_list = {}

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
    configfile.write(config)
    configfile.close()

select_records()




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


