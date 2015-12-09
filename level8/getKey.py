#! /usr/bin/python

import requests
import re
import binascii
import base64

username = 'natas8'
password = ''

r = requests.get('http://natas8.natas.labs.overthewire.org/index-source.html', auth=(username, password))
pattern = r'\$encodedSecret&nbsp;=&nbsp;\"(\w+)\";'
result = re.search(pattern, str(r.content))
encodeSecret = result.group(1)

binaryStr = binascii.unhexlify(encodeSecret)
payload = {'secret':base64.b64decode(binaryStr[::-1]), 'submit':'submit'}
r = requests.post('http://natas8.natas.labs.overthewire.org/', auth=(username, password), data=payload)
pattern = r'The password for natas9 is (\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)
