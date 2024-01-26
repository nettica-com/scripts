# Create a network based on the command line parameters

import sys
import os
import argparse
import json
import time
import requests

# Get the key from the environment
key = os.environ.get('NETTICA_API_KEY')
if key == None:
    # If the API key is not set in the environment, check args
    if len(sys.argv) > 1:
        key = sys.argv[1]
    else:
        # If the API key is not set in the environment or args, exit
        print('You must set NETTICA_API_KEY in the environment or pass it as an argument')
        sys.exit(1)


# Parse the command line arguments for the name, subnet, and DNS servers
parser = argparse.ArgumentParser(description='Create a network')
parser.add_argument('--name', help='Name of the network', required=True)
parser.add_argument('--subnet', help='Subnet of the network', required=True)
parser.add_argument('--dns', help='DNS servers for the network', required=False)
args = parser.parse_args()

# Create a new request


# Set the request URL
url = 'https://my.nettica.com/api/v1.0/net'

# Set the request headers
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-API-KEY': key
}

# Set the request payload
payload = {
    'netName': args.name,
    'subnet': [ args.subnet ],
}

# Add the DNS servers if they were specified
if args.dns:
    payload['dns'] = [ args.dns ]

# Send the request to create the network
response = requests.post(url, headers=headers, json=payload)

# Check the response status code
if response.status_code == 200:
    print('Network created successfully!')
    print (json.dumps(response.json(), indent=2))
else:
    print('Failed to create network:', response.status_code)
    print(json.dumps(response.json(), indent=2))
