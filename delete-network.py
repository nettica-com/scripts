# Create a network based on the command line parameters

import sys
import os
import argparse
import requests

# Get the key from the environment
key = os.environ.get('NETTICA_API_KEY')
if key == None:
    # If the API key is not set in the environment, check args
    if len(sys.argv) > 1:
        key = sys.argv[1]
    else:
        # If the API key is not set in the environment or args, exit
        print('You must set NETTICA_API_KEY in the environment')
        sys.exit(1)


# Parse the command line arguments for the name, subnet, and DNS servers
parser = argparse.ArgumentParser(description='Create a network')
parser.add_argument('--name', help='Name of the network', required=True)
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

# Send the request to find the network
response = requests.get(url, headers=headers)

# Send the request to delete the network
for net in response.json():
    if net['netName'] == args.name:
        response = requests.delete(url + '/' + net['id'], headers=headers)
        break


# Check the response status code
if response.status_code == 200:
    print('Network deleted.')
else:
    print('Failed to delete network:', response.status_code)
    print(response.text)
