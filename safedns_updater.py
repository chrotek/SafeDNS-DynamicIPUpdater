#!/usr/bin/env python3

import sys
import string
import time
import json
import requests
from pick import pick

records_dict=json.load(open('config/records.json', 'r'))

print ("LEN="+(str(len(records_dict))))

for record,data in records_dict.items():
    print(record+","+str(data))

 
