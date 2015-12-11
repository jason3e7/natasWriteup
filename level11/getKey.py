#! /usr/bin/python

import requests
import re
import base64
from urllib import unquote

username = 'natas11'
password = ''

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
	
r = requests.get('http://natas11.natas.labs.overthewire.org/', auth=(username, password))
pattern = r'data=(\S+)'
result = re.search(pattern, str(r.headers['set-cookie']))
xorKey = '{"showpassword":"no","bgcolor":"#ffffff"}'
key = findReapet(xor_encrypt(base64.b64decode(unquote(result.group(1))), xorKey))
payload = '{"showpassword":"yes","bgcolor":"#ffffff"}'
data = base64.b64encode((xor_encrypt(payload, key)))

headers = {'Cookie':'data=' + data}
r = requests.get('http://natas11.natas.labs.overthewire.org/', auth=(username, password), headers=headers)
pattern = r'The password for natas12 is (\w+)'
result = re.search(pattern, str(r.content))

print result.group(1)
