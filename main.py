
# ARGUMENT PARSER #############################################

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("conf", help="Path to config.ini") 
args = parser.parse_args()


# MODULES #####################################################

import ovh
import json
import configparser
import requests
import sys
import os


sys.stdout.write('Reading config.ini... ')
sys.stdout.flush()
config = configparser.ConfigParser()
config.read(args.conf)
print('\033[92mOK\033[0m')


# Instanciate an OVH Client.
# You can generate new credentials with full access to your account on
# the token creation page
client = ovh.Client(
    endpoint='ovh-eu',               # Endpoint of API OVH Europe (List of available endpoints)
    application_key=config['API']['KEY'],    # Application Key
    application_secret=config['API']['SECRET'], # Application Secret
    consumer_key=config['API']['CONSUMER_KEY'],       # Consumer Key
)

#ck = client.new_consumer_key_request()
#ck.add_rule(method="GET",path= "/*")
#ck.request()

ext_ip = requests.get('https://api.ipify.org/?format=json')
ext_ip = ext_ip.json()['ip']

dyn_host_list = client.get('/domain/zone/zwanto.org/dynHost/record')

for record in dyn_host_list:
    dyn_host = client.get('/domain/zone/zwanto.org/dynHost/record/' + str(record))
    a = requests.get('http://www.ovh.com/nic/update?system=dyndns&hostname=' + dyn_host['subDomain'] + '.' + dyn_host['zone'] + '&myip=' + ext_ip,auth =(config['DYNDNS']['USER'],config['DYNDNS']['PASSWORD']))
    print(a.content)