#!/usr/bin/env bash

api_token=GEL2GLaUYwtZ8px8l675OFeVR0KGheO8;
echo "Token : "$api_token




# List Zones
curl -X GET https://api.ukfast.io/safedns/v1/zones -H "Authorization: $api_token"
