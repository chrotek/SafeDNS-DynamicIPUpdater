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
import configparser

# Define the variables that we later depend on for configuration
config = configparser.ConfigParser()
config.read('config.ini')
config['API'] = {}
config['RECORDS'] = {}
config['API']['key'] = 'null'
config['API']['update_interval'] = 'null'
api_url='https://api.ukfast.io/safedns/v1'

final_record_list = {}
new_subdomain_list = {}
api_key_loaded = False
ttl_problem = False
selected_records_loaded = False
update_interval_loaded = False


# CTRL + C Handling
def handler(signum, frame):
    print ('Exiting on CTRL+C')
    global exitbool
    exitbool=True
    sys.exit(130)

# Variables needed for the CTRL+C Function
global exitbool
exitbool=False
signal.signal(signal.SIGINT, handler)

# The save_config function will save our config in config.ini
def save_config():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# The api_key_input function will read API Key from User input, and add it to the config.
def api_key_input():
    global api_key
    print("Please enter API Key, and press enter.  CTRL + C to quit")
    api_key = input()
    config['API']['key'] = api_key
    save_config()
    api_key_load()

# The api_key_load function will load a stored API Key from config.ini, then test it. If the API Returns a 401 Error (Invalid API Key), this will ask for a new one
def api_key_load():
    global api_token
    config.read('config.ini')
    api_key = config['API']['key']   
#    print ("API KEY : "+api_key)
    global api_key_loaded
    api_key_loaded = True
    api_token= {
        'Authorization': api_key,
    }
    response=requests.get(api_url+"/zones", headers=api_token)
    if response.status_code == 401:
        print("API Key Invalid!")
        api_key_input()

# The select_domains function requests a list of domains using SafeDNS API, then displays a list for the user to select domains from
def select_domains():
    domain_list = json.loads(json.dumps(requests.get(api_url+"/zones", headers=api_token).json()['data']))
    title = 'Please choose the domains you want to make a dynamic record on: '
    def get_label(option): return option.get('name')
    global selected_domains
    selected_domains = pick(domain_list, title, multi_select=True, indicator='*', options_map_func=get_label)
    return(selected_domains)

# The select_subdomains function uses domains selected in select_domains , Queries their existing records with the SafeDNS API  and displays the list for the user to select specific records with. 
# In this function we also strip out SOA , NS and MX records, because it doesn't make sense for them to be dynamic
def select_subdomains(domain):
    new_subdomain_list=[]
    current_subdomain_list = json.loads(json.dumps(requests.get(api_url+"/zones/"+domain+"/records", headers=api_token).json()['data']))
    title = "Please choose the record you want to make dynamic on {}. \n \n  (record name, record type)".format(domain)
    def get_label(option):
        return option.get('name'),option.get('type')
    global selected_subdomains
    global final_record_list
    for key in current_subdomain_list:
        if str(key['type']) != 'SOA' and str(key['type']) != 'NS' and str(key['type']) != 'MX':
            new_subdomain_list.append(key)
    new_x=(len(final_record_list))
    selected_subdomains = pick(new_subdomain_list, title, multi_select=True, indicator='*', options_map_func=get_label)
    for x in range(len(selected_subdomains)):
        strdata=str(selected_subdomains[x])
        splitdata = strdata.split("'")
        record_id_x=splitdata[2]
        record_id=record_id_x.strip(': , ,')
        record_name=splitdata[5]
        record_type=splitdata[9]
        record_zone=domain
        record_list=[record_id,record_name,record_type,record_zone]
        final_record_list[x] = [record_list]
        config['RECORDS'][str(new_x)] = str(record_list)
        global selected_records_loaded
        selected_records_loaded = True
        new_x +=1

# The load_records_config function will read the previously selected domains from the config.ini file. 
def load_records_config():
    config.read('config.ini')
    for key in config['RECORDS']:
#        print("Key" + key+" Data: " + config['RECORDS'][key])
        final_record_list[key] = config['RECORDS'][key]
        global selected_records_loaded
        selected_records_loaded = True 

# The select records funtion will load the API Key, then call the select_domains function, and finally call the select_subdomains function with the selected domains
def select_records():
    if api_key_loaded is not True:
        api_key_load()
    config.remove_section('RECORDS')
    config['RECORDS'] = {}
    for domaindata in (select_domains()):
        str_domain_data = str(domaindata)
        split_domain_data = str_domain_data.split("'")
        select_subdomains(split_domain_data[3])
    save_config()
    load_records_config()

# The check_update_interval function will load the stored update_interval. If this doesn't exist will ask for one to be inputted. 
def check_update_interval():
    global update_interval
    global update_interval_loaded
    update_interval=config['API']['update_interval']
    print ("Update interval "+update_interval)#debug
    if(update_interval=='null'):
        write_update_interval()
    update_interval_loaded = True
#    confirm_selected_ttl()
    
# The write_update_interval will ask the user to input an update interval, and save it in config.ini
def write_update_interval():
    print("How frequently do you want to update your records (in seconds)")
    global update_interval
    update_interval = input()
    config['API']['update_interval']=update_interval
    global update_interval_loaded
    update_interval_loaded = True
    save_config()    

# The confirm_ttl function will query the TTL of the domain name the function is called with.
# If the TTL is higher than the specified update interval, display a warning thet either the update interval should be raised, or the ttl should be lowered
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
            print("Domain "+domain_x+"'s SOA TTL ("+domain_soa_ttl+") is higher than your specified update frequency("+update_interval+")")
            global ttl_problem
            ttl_problem = True
        else:
            ttl_problem = False

# The confirm_selected_ttl function iterates over the records the user selected, and calls the confirm_ttl function for each one.
# If any one of the domains has a Higher TTL, display warnings and wait for input to continue.
def confirm_selected_ttl():
    if selected_records_loaded is not True:
        select_records()
    domain_list_ttl_check=[]
    for x in final_record_list:
        entry=str(final_record_list[x]).split("'")
        if entry[7] not in domain_list_ttl_check:
            domain_list_ttl_check.append(entry[7])
#        print("TTL Check List: "+str(domain_list_ttl_check))
    for domain in domain_list_ttl_check:
        confirm_ttl(domain)
    if ttl_problem is True:
        print("\nThis will cause delays in propegation. Please enter a new update frequency that is a higher value. \nAlternatively change the domain's TTL to a lower value")
        print("Press ENTER to continue\n")
        input()

# A test function. This just loops over the domains and breaks the config into individual variables.
# Useless for now, but later I'll turn this into the function that actually updates the records.
def loop_over_records_template():
    for x in final_record_list:
        record=str(final_record_list[x]).split(",")
        record_id=record[0].strip("[,'")
        record_name=record[1].replace("'","")
        record_type=record[2].replace("'","").replace("]","")
        print("ID: "+record_id+" Name: "+record_name+" Type: "+record_type)

# The main_menu function displays a menu of the options the user can choose, and calls the relevant functions.
def main_menu():

    title = 'Choose an option (press SPACE to mark, ENTER to continue): '
    options = ['Full configuration','Set API Key','Set Records','Set Update Freqency','Exit']
    selected = pick(options, title, min_selection_count=1)
    if selected[1] == 0:
        api_key_load()
        select_records()
        write_update_interval()
        confirm_selected_ttl()
        main_menu()
    elif selected[1] == 1:
        api_key_input()
        main_menu()
    elif selected[1] == 2:
        api_key_load()
        select_records()
        main_menu()
    elif selected[1] == 3:
        api_key_load()
        write_update_interval()
        load_records_config()
        confirm_selected_ttl()
        main_menu()
    elif selected[1] == 4:
        sys.exit(0)

main_menu()
