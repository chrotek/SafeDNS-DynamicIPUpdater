#!/usr/bin/env python3

import string
import time
import json
import requests
from consolemenu import *
from consolemenu.items import *

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

def show_main_menu():
    # Create the menu
    menu = ConsoleMenu("----| UKFast SafeDNS Dynamic IP Updater |----", "       ---| Configuration Tool |---")
    
    # Create some items
    
    # MenuItem is the base class for all items, it doesn't do anything when selected
    menu_item = MenuItem("Menu Item")
    
    # A FunctionItem runs a Python function when selected
    function_item = FunctionItem("Call a Python function", input, ["Enter an input"])
    
    # A CommandItem runs a console command
    command_item = CommandItem("Run a console command",  "touch hello.txt")
    
    # A SelectionMenu constructs a menu from a list of strings
    selection_menu = SelectionMenu(["item1", "item2", "item3"])
    
    # A SubmenuItem lets you add a menu (the selection_menu above, for example)
    # as a submenu of another menu
    submenu_item = SubmenuItem("Submenu item", selection_menu, menu)
    
    # Once we're done creating them, we just add the items to the menu
    menu.append_item(menu_item)
    menu.append_item(function_item)
    menu.append_item(command_item)
    menu.append_item(submenu_item)
    
    # Finally, we call show to show the menu and allow the user to interact
    menu.show()

show_main_menu()

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


