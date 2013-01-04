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

result, data = conn.uid('search', None, "ALL") # search and return uids instead
i = 0

for uid in data[0].split():
	if i <= 21:
		typ, d = conn.uid('fetch' , uid, 'RFC822.SIZE')
		size = d[0].split()[2].split(')')[0]
		typ , d = conn.uid('fetch', uid , '(X-GM-THRID X-GM-MSGID)')
		print d
		print uid, '\t' ,size
	i = i + 1

conn.close()
conn.logout()


