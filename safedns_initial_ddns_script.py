#!/usr/bin/env python3

import sys
import string
import time
import json
import requests
from pick import pick 
import ast
import signal
import dns.resolver
import re
# from pprint import pprint

def handler(signum, frame):
    print ('Exiting on User Instruction')
    global exitbool
    exitbool=True
    exit(130)

global exitbool
exitbool=False
signal.signal(signal.SIGINT, handler)

def api_key_write():
    try:
        configfile = open("config/apikey","w+")
        print("Please enter API Key, and press enter.  CTRL + C to quit")
        api_key = input()
        if api_key == 'quit':
            print("You typed QUIT!!")
            exitbool=True
            sys.exit(0)

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
            global api_key_loaded
            api_key_loaded = True
    api_token= {
        'Authorization': api_key,
    }
    response=requests.get('https://api.ukfast.io/safedns/v1/zones', headers=api_token)
    if response.status_code == 401:
        print("API Key Invalid!")
        if exitbool == True:
            exit(130)
        api_key_write()
#        api_key_load()

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
#    print(selected_subdomains)
    for x in range(len(selected_subdomains)):
        strdata=str(selected_subdomains[x])
        splitdata = strdata.split("'")
        record_id_x=splitdata[2]
        record_id=record_id_x.strip(': , ,')
        record_name=splitdata[5]
        record_type=splitdata[9]
        record_list=[record_id,record_name,record_type]
#        print("ID "+record_id)
#        print("Name "+record_name)
#        print("Type "+record_type)
#        print("List "+str(record_list))
        final_record_list[x] = [record_list]
        global selected_records_loaded
        selected_records_loaded = True 

def select_records():
    if api_key_loaded is not True:
        print("You need to load the API Key first")
        api_key_load()

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
    global update_interval
    try:
        configfile = open("config/update_interval","r")
    except IOError:
        print("Couldn't read Update Interval.")
        write_update_interval()
    finally:
        with open('config/update_interval', 'r') as file:
            update_interval = file.read().replace('\n', '')
            global update_interval_loaded
            update_interval_loaded = True
#   i         print("UpdateInterval "+update_interval)

def write_update_interval():
    try:
        configfile = open("config/update_interval","w+")
        print("How frequently do you want to update your records (in seconds)")
        update_interval = input()
        configfile.write(update_interval)
    except IOError:
        print("Couldn't save Update Interval")
        write_update_interval()
    finally:
        configfile.close()   
        check_update_interval()

def confirm_ttl(domain_x):
    if selected_records_loaded is not True:
        print("You need to select some records")
        select_records()
    domain_y=str(re.findall("\.([a-z\.]+)*$", domain_x))
    domain=domain_y.strip("[ , ] , '")
    response = dns.resolver.query(domain, 'SOA')
    if response.rrset is not None:
        domain_soa_ttl_x = str(re.findall("[0-9]+$", str(response.rrset)))
        domain_soa_ttl = domain_soa_ttl_x.strip("[ , ] , '")
        if int(domain_soa_ttl) > int(update_interval):
            print("Domain "+domain+"'s SOA TTL ("+domain_soa_ttl+") is higher than your specified update frequency("+update_interval+")")
            print("This will cause delays in propegation. Change your domain's TTL for optimum results")

def confirm_selected_ttl():
    for x in final_record_list:
        entry=str(final_record_list[x]).split("'")
        print("NAME:"+str(entry[3]))
        confirm_ttl(str(entry[3]))



def main_menu():

    title = 'Choose an option (press SPACE to mark, ENTER to continue): '
    options = ['Full configuration','Set API Key','Set Records','Set Update Freqency','Exit']
    selected = pick(options, title, min_selection_count=1)
    if selected[1] == 0:
#       print("1- Full config")
        api_key_load()
        select_records()
        write_update_interval()
        confirm_selected_ttl()
        main_menu()
    elif selected[1] == 1:
#       print("2- Set API Key")
        api_key_write()
        main_menu()
    elif selected[1] == 2:
#       print("3- Set Records")
        select_records()
        main_menu()
    elif selected[1] == 3:
#        print("4- Set Update Freqency")
        write_update_interval()
        confirm_selected_ttl()
        main_menu()
    elif selected[1] == 4:
#        print("5- Exit")
        sys.exit(0)

api_url='https://api.ukfast.io/safedns/v1'
api_key_loaded = False
selected_records_loaded = False
update_interval_loaded = False
final_record_list = {}
main_menu()
#def confirm_ttl(domain_x):
#    if selected_records_loaded is not True:
#        print("You need to select some records")
#        select_records()
#    domain_y=str(re.findall("\.([a-z\.]+)*$", domain_x))
#    domain=domain_y.strip("[ , ] , '")
#    response = dns.resolver.query(domain, 'SOA')
#    if response.rrset is not None:
#        domain_soa_ttl_x = str(re.findall("[0-9]+$", str(response.rrset)))
#        domain_soa_ttl = domain_soa_ttl_x.strip("[ , ] , '")
#        if int(domain_soa_ttl) > int(update_interval):
#            print("Domain "+domain+"'s SOA TTL ("+domain_soa_ttl+") is higher than your specified update frequency("+update_interval+")")
#            print("This will cause delays in propegation. Change your domain's TTL for optimum results")

sys.exit(0)








#api_key_load()
#select_records()
check_update_interval()
print(final_record_list)
for x in final_record_list:
    entry=str(final_record_list[x]).split("'")
    print("NAME:"+str(entry[3]))
    confirm_ttl(str(entry[3]))



#write_update_interval() 
#confirm_ttl("cloud.chrotek.co.uk")
#confirm_ttl("chrotek.co.uk")
confirm_ttl("gwin.cloud.chrotek.co.uk")
#main_menu()
sys.exit(0)


# TO - DO
# - Check the Update Interval is not greater than the domain's TTL
# - Add record type to menu when selecting records

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


