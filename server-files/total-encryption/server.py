#!/usr/local/bin/python
#
# Polymero
#

# Imports
import os, time, base64
from Crypto.Util.number import getPrime, inverse, GCD, long_to_bytes

# Local imports
from ltet import LTET
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

HDR_C0 = r"""|
|    ______   _____________________  _________________     ________  _     _ 
|   (_____ \ / ___________________ \(_________________)   (_______ \| |   | |
|    _____) | (____  _______ _____) )_  _  _ _     _ _     _ _____) ) |___| |
|   |  __  / \____ \|  ___  |  __  /| ||_|| | |   | | |   | |  __  /\_____  |
|   | |  \ \______) ) |   | | |  \ \| |   | | |___| | |___| | |  \ \______| |
|   |_|   \________/|_|   |_|_|   |_|_|   |_|\_____/ \_____/|_|   \_________|
|   + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ver.1 +
|   |                                                                       |
|   |                             Connecting...                             |"""
print(HDR_C0, end='\r', flush=True)

t1   = time.time()
ltet = LTET(1024)
t2   = time.time()

HDR_C1 = r"""|   |           Connected to the Remote Secure Armoury. ({:0.2f} s)
|   |                                                                       |
|   + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|
|                             SECURITY UPDATE LOG
|
|     - VER. 1 - All contents of the RSArmoury have now been secured
|                with layered RSA encryption + XOR blinding, LTET(1024).
|
|
|     PUBLIC KEYS:
|     {}
|     {}
|     {}
|
|""".format(t2-t1,*[b'.'.join([base64.urlsafe_b64encode(long_to_bytes(j)).rstrip(b'=') for j in [ltet.public['e'][i],ltet.public['n'][i]]]).decode() for i in range(3)])

print(HDR_C1, end='\r', flush=True)

while True:
    
    MENU = f"""|
|   {ltet.encrypt(b'[R]ecite our glorious motto')} 
|   {ltet.encrypt(b'[E]ncrypt custom message')} 
|   {ltet.encrypt(b'[P]rint our secret flag')} 
|   {ltet.encrypt(b'[Q]uit')} 
|"""

    try:

        print(MENU)
    
        choice = input('|\n|  >>> ')
        
        if choice.lower() == 'q':

            print(f"|\n|  {ltet.encrypt(b'Our secrets remain secured ~ !')}\n|")
        
            break

        elif choice.lower() == 'r':

            print("|\n|  {}".format(ltet.encrypt(b'"self plugging best plugging" - Polymero 2021')))

        elif choice.lower() == 'e':

            print(f"|\n|  {ltet.encrypt(b'Please enter your message in hex:')}")

            msg = input('|\n|  >>> ')

            try:

                print(f"|\n|  {ltet.encrypt(bytes.fromhex(msg))}")

            except:

                print(f"|\n|  {ltet.encrypt(b'USER INPUT ERROR -- Invalid input.')}")

        elif choice.lower() == 'p':

            print(f"|\n|  {ltet.encrypt(FLAG)}")

        else:

            print(f"|\n|  {ltet.encrypt(b'USER INPUT ERROR -- Unknown option.')}")
        
    except KeyboardInterrupt:
    
        print(f"\n|\n|  {ltet.encrypt(b'Our secrets remain secured ~ !')}\n|\n|")
        break
        
    except:
    
        print(f"|\n|  {ltet.encrypt(b'RUN ERROR -- An unexpected error occured.')}")
        break
