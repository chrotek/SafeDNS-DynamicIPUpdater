#!/usr/bin/env python3

import sys
import string
import time
import json
import requests
from pick import pick 
API_TOKEN= {
    'Authorization': 'lz2lkW8cmEGSIUhC0JnIkouhhiPYB8WM',
}


safedns_domain_list = json.loads(json.dumps(requests.get('https://api.ukfast.io/safedns/v1/zones', headers=API_TOKEN).json()['data']))

domains = []

domaindict = {}

for domain in range(0, (len(safedns_domain_list))):
    safedns_domain_dict = (json.loads(str(json.dumps(safedns_domain_list[domain]))))
    print (safedns_domain_dict['name'])
    domains.append(safedns_domain_dict['name'])
#    domaindict['name'] = 


print ("--------------------------------------------------")

print(type(safedns_domain_dict))
print(domains)
print(safedns_domain_dict)
print("Domains in list: "+str(len(domains)))
time.sleep(1)


title = 'Please choose the domains you want to make a dynamic record on: '

def get_label(option): return option.get('name')


selected = pick(safedns_domain_dict, title, multi_select=True, indicator='*', options_map_func=get_label)

print(selected)





# title = 'Please choose an option: '
# options = [{'label': 'option1'}, {'label': 'option2'}, {'label': 'option3'}]
#  
# def get_label(option): return option.get('label')
#    
# selected = pick(options, title, multi_select=True, indicator='*', options_map_func=get_label)
#
# print(selected)





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


