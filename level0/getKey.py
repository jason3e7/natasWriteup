#! /usr/bin/python

import requests
import re

username = 'natas0'
password = 'natas0'

r = requests.get('http://natas0.natas.labs.overthewire.org/', auth=(username, password))
pattern = r'<!--The password for natas1 is (\w+) -->'
result = re.search(pattern, str(r.content))

print result.group(1)
