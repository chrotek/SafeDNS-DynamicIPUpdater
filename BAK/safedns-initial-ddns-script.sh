#!/usr/bin/env bash

api_token=GEL2GLaUYwtZ8px8l675OFeVR0KGheO8;
echo "Token : "$api_token




# List Zones
curl -sX GET https://api.ukfast.io/safedns/v1/zones -H "Authorization: $api_token" | grep -Po '"name":.*?[^\\]",' | cut -f4 -d\"
