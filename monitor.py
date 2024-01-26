# This program monitors your Nettica VPN connections and
# sends an email if endpoint connections are down
#
# It utilizes the Nettica API at https://my.nettica.com/api/docs/
# and the Python Requests library.  To install the Requests library
# run the following command: pip install requests
#

import os
import sys
import time
import smtplib
import subprocess
from email.mime.text import MIMEText
import requests

# Set the email addresses
fromaddr = 'alerts@nettica.com'
toaddrs  = 'xxx@nettica.com'

# Set the email message
msg = MIMEText('Nettica:  Your device %s with VPN %s is down')
msg['Subject'] = 'Nettica VPN Alert'
msg['From'] = fromaddr
msg['To'] = toaddrs

# Call Nettica API to get the status of your VPN connections
# You will need to replace the API key with your own
# You can get your key from the Nettica Admin web site
# at https://my.nettica.com/account

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


# Create a notify map so we don't send multiple emails
# for the same device
notify = {}

# Call the API to get the status of your VPN connections

# Create a new request

# Set the request URL
Url = 'https://my.nettica.com/api/v1.0/device'

# Set the request headers
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'X-API-KEY': key }

# Loop forever
while True:
    # Make the request
    r = requests.get(Url,headers=headers)

    # Check the response status code
    if r.status_code != 200:
        print (r.text + str(r.status_code))
        sys.exit(1)

    # Get the response data
    devices = r.json()

    # The results is a list of devices and their associated VPNs.
    # Loop through the list and check the status of each VPN
    for device in devices:
        for vpn in device['vpns']:
            if (vpn['current']['endpoint'] != '') and ('lastSeen' in device):
                print( device['name'] + ' ' + vpn['name'] + ' ' + vpn['current']['endpoint'] + ' ' + device['lastSeen'])
                now = time.time()
                parts = device['lastSeen'].split('.')
                lastSeen = time.mktime(time.strptime(parts[0], "%Y-%m-%dT%H:%M:%S"))
                if (now - lastSeen) > 300 and (device['id'] in notify) == False:
                    print('Sending email')
                    # Set the message text
                    print( 'Nettica: Your device %s with VPN %s is down' % (device['name'], vpn['netName']))
                    msg.set_payload('Nettica:  Your device %s with VPN %s is down' % (device['name'], vpn['name']))
                    # Send the email
                    # server = smtplib.SMTP('localhost')
                    # server.sendmail(fromaddr, toaddrs, msg.as_string())
                    # server.quit()
                    # Put the device into a notify list so we don't send multiple emails
                    notify[device["id"]] = True
                else:
                    # The device is back up, send an email
                    if device['id'] in notify and notify[device["id"]] == True:
                        msg.set_payload('Nettica:  Your device %s with VPN %s is back up' % (device['name'], vpn['name']))
                        # Send the email
                        # server = smtplib.SMTP('localhost')
                        # server.sendmail(fromaddr, toaddrs, msg.as_string())
                        # server.quit()
                        print( 'Nettica: Your device %s with VPN %s is back up' % (device['name'], vpn['netName']))
                    notify[device["id"]] = False

    # Wait 60 seconds before checking again
    time.sleep(60)
