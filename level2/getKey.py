#! /usr/bin/python

import requests
import re

username = 'natas2'
password = ''

r = requests.get('http://natas2.natas.labs.overthewire.org/files/users.txt', auth=(username, password))
pattern = r'natas3:(\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)
