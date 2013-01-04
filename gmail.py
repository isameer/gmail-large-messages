import imaplib
import random
import time
from email.parser import HeaderParser

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
    imap_conn.select('[Gmail]/All Mail')

    return imap_conn

conn = connect()


typ, data = conn.search(None, 'ALL')
i = 0
max = 0
max_id = 0

for num in data[0].split():
	if i >= 0:
		typ, d = conn.fetch(num, 'RFC822.SIZE')
		size = d[0].split()[2].split(')')[0]
		print num, '\t' ,size
		if size > max:
			max = size
			max_id = num
	i = i + 1

conn.close()
conn.logout()


