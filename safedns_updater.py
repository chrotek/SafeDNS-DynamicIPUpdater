#!/usr/bin/env python3

import sys
import string
import time
import json
import requests
from pick import pick

#records_dict=json.load(open('config/records.json', 'r'))
#
#print ("LEN="+(str(len(records_dict))))
#
#for record,data in records_dict.items():
#    print(record+","+str(data))

import ast


file = open("config/records.json", "r")
data = file.readlines()
file.close()

for line in data:
    var_name, var_val = line.split(" = ")
    for possible_num_types in range(3):  # Range is the == number of types we will try casting to
        try:
            var_val = int(var_val)
            break
        except (TypeError, ValueError):
            try:
                var_val = ast.literal_eval(var_val)
                break
            except (TypeError, ValueError, SyntaxError):
                var_val = str(var_val).replace("\n","")
                break
    locals()[var_name] = var_val


print (records_dict)




file = open("config/apikey", "r")
data = file.readlines()
file.close()

for line in data:
    var_name, var_val = line.split(" = ")
    for possible_num_types in range(3):  # Range is the == number of types we will try casting to
        try:
            var_val = int(var_val)
            break
        except (TypeError, ValueError):
            try:
                var_val = ast.literal_eval(var_val)
                break
            except (TypeError, ValueError, SyntaxError):
                var_val = str(var_val).replace("\n","")
                break
    locals()[var_name] = var_val


print (api_key)

