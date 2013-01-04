import imaplib
import random
import time
from email.parser import HeaderParser
import urllib

import xoauth

MY_EMAIL = ''
MY_TOKEN = '' 
MY_SECRET = '' 

def connect():
    nonce = str(random.randrange(2**64 - 1))
    timestamp = str(int(time.time()))

    consumer = xoauth.OAuthEntity('anonymous', 'anonymous')
    access = xoauth.OAuthEntity(MY_TOKEN, MY_SECRET)
    token = xoauth.GenerateXOauthString(
        consumer, access, MY_EMAIL, 'imap', MY_EMAIL, nonce, timestamp)

    imap_conn = imaplib.IMAP4_SSL('imap.googlemail.com')
    imap_conn.authenticate('XOAUTH', lambda x: token)
    imap_conn.select('INBOX')

    return imap_conn



i = 1
max = 0
max_id = 0

parser = HeaderParser()

conn = connect()
conn.select('[Gmail]/All Mail')

f = open('sizes_ALL_sorted.txt' , 'r')
lines = f.readlines()

for line in lines:
	if i <= 250:
		d = line.split()
		typ, data = conn.fetch(d[1] , 'RFC822.HEADER')
		msg = parser.parsestr(data[0][1])
		params = urllib.urlencode({'from': msg['From'] , 'to' : msg['To'] , 'subject' : msg['Subject']})
		searchurl = 'https://mail.google.com/mail/#advanced-search/' + params + '&subset=all&within=1d'
		typ, data = conn.fetch(d[1] , 'RFC822.SIZE')
		size = data[0].split()[2].split(')')[0]
		print i , '\t' , int(size)/(1024*1024) ,'MB' , '\t' , msg['From'] ,'\t' , msg['Subject'] , '\t' , searchurl
	i = i + 1

conn.close()
conn.logout()


