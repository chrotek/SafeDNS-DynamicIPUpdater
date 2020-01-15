#!/usr/bin/env python3

import string

API_TOKEN = "GEL2GLaUYwtZ8px8l675OFeVR0KGheO8;"
print ("Token : ".format(API_TOKEN))
#
#
#
#
## List Zones
#curl -sX GET https://api.ukfast.io/safedns/v1/zones -H "Authorization: $api_token" | grep -Po '"name":.*?[^\]",' | cut -f4 -d"
