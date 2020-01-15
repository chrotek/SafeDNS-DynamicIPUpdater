#!/usr/bin/env python3

import string
import time
import json
import requests

API_TOKEN= {
    'Authorization': 'lz2lkW8cmEGSIUhC0JnIkouhhiPYB8WM',
}


safedns_domain_list = json.loads(json.dumps(requests.get('https://api.ukfast.io/safedns/v1/zones', headers=API_TOKEN).json()['data']))

domains = []

for domain in range(0, (len(safedns_domain_list))):
    safedns_domain_dict = (json.loads(str(json.dumps(safedns_domain_list[domain]))))
    print (safedns_domain_dict['name'])
    domains.append(safedns_domain_dict['name'])



print ("--------------------------------------------------")

print("Domains in list: "+str(len(domains)))

# MENU CODE










# #########################################
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


