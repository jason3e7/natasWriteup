#! /usr/bin/python

import requests
import re

username = 'natas1'
password = ''

r = requests.get('http://natas1.natas.labs.overthewire.org/', auth=(username, password))
pattern = r'<!--The password for natas2 is (\w+) -->'
result = re.search(pattern, str(r.content))

print result.group(1)
