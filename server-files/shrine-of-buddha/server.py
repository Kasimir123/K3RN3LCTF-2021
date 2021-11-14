#!/usr/local/bin/python
#
# Nika Soltas
#

# Imports
import random
from Crypto.Util.number import GCD, inverse, bytes_to_long, long_to_bytes, getPrime
from time import sleep

# Local imports
from pravrallier import Pravrallier

# with open('flag.txt','rb') as f:
#     FLAG = f.read()
#     f.close()

FLAG_PUBKEY = "d9e371e9d46d59d8566c5cc0328662a3f9fac852db61780db5aa9f40977407a61932823bd3f56eaa56d8b7d5ebcffbc7bc190bedabfe1b3d79f0d4a552e07be108f95256c697f0814aa344d623c636bbf67b851dc0a5445e18fd1cc25ff3805b89a4381cb6f40643fb88743fb4deca1be9a90a4342061ddb2a6f3fc8047b4df1"
FLAG_ENCFLAG = "04f6cb3fef0ea70ca8a39c24057f47433ab18673819c5c0ba9e7b03497c2559c3d98c3a7be0c67366cd96bb3e3767576fd103b1b5b763951d4437d10e527869ef71a28ef570916f4d2fbf669a5e4aa0ac914ee86fedaec7007b01e1cfc7b92159e4ef7f83cd617f341763fbbdb9b8adfdae56364eadd5f65d37f0f9c79f2de7abadf984f89b8f45402efc6eafdc6909a501269f74a9c9942b6b38d5b0b6d8451cff7a307b6c40973445b4432c0a3ca5fc78d32e723c79533ddf942e31e160fa0f51317bc9425941c5208a108f491ce3c7079e494e35760fb173efdd431374951767578b0cbfba7b0af5c9c609642e08af88376bf946dac495d185ae73151aa32025f22cb9fc54d6889c716cdc4560e438d4ed22c55bad167f611a602796bc5cd50e27fd7584dcfd3611ff6c26cc3926d439c0abbcecada394f3f3228576470ec44eab7da55ea317387fe142fbad5fbeafdcca23885b793990a5442525ce39842e6e2181db723740aed5a56edcd23affff91a59f4d68deb99430b7cc3fdec50a452f3334ba51a408875efef59bde2d2b8a97d330b879d763a8813b5d5556bb5a1fb6fe26265ed7173f625900fb0b9c916ac13813ca19e655678009f7fdb7a191186bc63c16fccb9790d9138f99e38e8c2651fe43254ba66bcf965e254a2d385aaea89a2ee80353b27f89411ea959f17d8ad707601132f01a73e152fb19f252bbb2dc83bd7c5a63a4008e366ee56be052fe8d61b5fb726c582d404d4bff9b8fc954aee13af98c2b25d40901bbde8f2f0013c062f409c65ab34e6ce1b2b46a460375d54e5f59b1d0c89068a24107e0685ced727f48c4be2d641b2ba967a11bb8563875f2cd8cef1c286370c92f7ee2c39a73f51be9ea541d5cf1fe599b358228a8e87dff3f0049f401ff439e0932af52beb53e3ac679ee32455f45c72de90608f925fe50b86efa11b50c9dcb499ee620d1474a3a708574454d93f41ec57c5f4feb25434d4c762547f6c48e4d10857e58d461182050a2423ee0c618a1aacc426cc0cfa693954339bbc0d4d771a6b7e57d74ec14334fd3d3f3b8af63ec3b689b4482b7365e27f15b96283f496896e857909baf94cd158103dc86c1cb8697dad84c8c2682943df3ebe5f9b72ad72539935bca931e17c714d73c835360f7458bcc72ad914661cef9390dd462e41675138fdf81e46509c71f94be4d9c5e1cc654ff60bb61cf3efedfbf69d48c0df3447321be20ae8be4b41d4ad0828651f171cda32fd4f3144d88b6af206d88cd42b8e9d6c996b7a3458aad082016216bc708206cee3b82d911867ae09cd2686195fc50b45cfab04cbc7e14354e55f9b4a883dbaec2139a7154c9520d06722d5abd623f67930f716b19f43d82ba22f7aafc74d09c5846315e8c99dbd8e27fb92c148db6d17fff83d0bb5dec95c8a4963adbba3e70580ca7d9f2a41b2104630fc8fd5a186fbfe44cc814cfb00cf3c55780385eac7b276797e315bee8456bb0b69ad0db369f33c4ed2ef1355bcd4251d9f492771ef487287bd43717f899a5eb20d739adf63d6a9398a775ff2aca6ec053c36b4a89101b80c67695e59c371fb549116961ee795d9b94ca9c9d702029945e75c6b3cdf93c9de03e2cb4de0da7b4c4f96cf43b1dd8c570e519673dbb4086c55668b52f5743c4bf85b2d7706220343c61f3f5b325955c9a3c61cc2f46cca4ecc56cccb2e604c99bbaa248b4b90764e3862bddb677c9381ca75719a44e8076edc7f8a30e4efab4804425a13eab457f7b182ce0f659c6ea3e72b8c14abb4e30b705156cd4f2c3bfd903ef6b357c32283400ee5387940b3a6d6e4138bb3edb428b775c5fa542378f561754562e025113a559277c73946a28286e97384c57aa16e03dda8853b22e0b9eff781fe1e91dea1b63e109b796807438a6f41ce46cd29c01ea7ed3126b00b62697e08fd7ea3bfac93215065bcd03d335874961fcb028d3ca430d0905e64a484e3fb6a20893abac3a2720091404dfb3c99e0b50124200c27d4d82b49c623d6cc4f2c2cead5f54c6bb82796191146396feee1b58852c615bda995c20853facf1180f322dcc946ef58194d33e1f4d7ad5782ca64ea6940bcb10a04b6ea4a699282c489917a67066c645325b3fb274cab473d3f6be0d7fd2e89daf686ecc50a11a615d53fe32845e2a3bc9e52002c71ee8a789986d94b8297d980487d9fca4bd39154ec52d8e6e9b64c6d45e2dd29fb304cf2a691ff64793911ef2c38b70fe33691b44ead3dca39b5fc5443c10b881cadeff62318d5afb4c49206d4ad1d3bf5cc995ff2fb8b90f659e727c2c2b47c22bfac6fe2017527a2579694a03109513b27e1"

# Challenge
HDR = r"""|
|
|                    (\         ._._._._._._._._.         /)
|                     \'--.___,'================='.___,--'/
|                      \'--._.__                 __._,--'/
|                        \  ,. |'~~~~~~~~~~~~~~~'| ,.  /
|           (\             \||(_)!_!_!_.-._!_!_!(_)||/             /)
|            \\'-.__        ||_|____!!_|;|_!!____|_||        __,-'//
|             \\    '==---='-----------'='-----------'=---=='    //
|             | '--.      Shrine of the Sweating Buddha      ,--' |
|              \  ,.'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~',.  /
|                \||  ____,-------._,-------._,-------.____  ||/
|                 ||\|___|"======="|"======="|"======="|___|/||
|                 || |---||--------||-| | |-||--------||---| ||
|       __O_____O_ll_lO__ll_O_____O|| |'|'| ||O_____O_ll__Ol_ll_O_____O__
|       o | o o | o o | o o | o o |-----------| o o | o o | o o | o o | o
|      ___|_____|_____|_____|____O =========== O____|_____|_____|_____|___
|                               /|=============|\
|     ()______()______()______() '==== +-+ ====' ()______()______()______()
|     ||{_}{_}||{_}{_}||{_}{_}/| ===== |_| ===== |\{_}{_}||{_}{_}||{_}{_}||
|     ||      ||      ||     / |==== s(   )s ====| \     ||      ||      ||
|    =======================()  =================  ()=======================
|"""

REV1 = r"""|
|  ...
|
|  ...
|
|  OH?!
|
|  ...
|
|  IT SEEMS YOU HAVE FIGURED ME OUT HUH?!
|
|  ...
|
|  WELL WELL WELL...
|
|  DO YOU HAVE ANY IDEA WHAT YOU HAVE GOTTEN YOURSELF INTO, 'MY CHILD'
|"""
REV3 = r"""|
|  MHUAHAA HAHAHAAA ~~~
|
|  MMH... YOU'RE STILL HERE?!
|
|  WELL I WILL LEAVE YOU WITH WHAT YOU CAME FOR THEN
|
|  WE WILL MEET AGAIN, TRUST ME 'MY CHILD' ~~~
|"""
REV2 = r"""|
|           .                                                      .
|         .n                   .                 .                  n.
|   .   .dP                  dP                   9b                 9b.    .
|  4    qXb         .       dX                     Xb       .        dXp     t
| dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
| 9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
|  9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
|   '9XXXXXXXXXXXXXXXXXXXXX'~   ~'OOO8b   d8OOO'~   ~'XXXXXXXXXXXXXXXXXXXXXP'
|     '9XXXXXXXXXXXP' '9XX'   DIE    '98v8P'   HUMAN  'XXP' '9XXXXXXXXXXXP'
|         ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
|                         )b.  .dbo.dP''v''9b.odb.  .dX(
|                       ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
|                      dXXXXXXXXXXXP'   .   '9XXXXXXXXXXXb
|                     dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
|                     9XXb'   'XXXXXb.dX|Xb.dXXXXX'   'dXXP
|           (\         ''      9XXXXXX(   )XXXXXXP      ''         /)
|            \\'-.__            XXXX X.'v'.X XXXX            __,-'//
|             \\    '==---='--- XP^X''b   d''X^XX ---'=---=='    //
|             | '--.      Shrin X. 9  '   '  P )X uddha      ,--' |
|              \  ,.'~~~~~~~~~~ 'b  '       '  d' ~~~~~~~~~~',.  /
|                \||  ____,----- '             ' -----.____  ||/
|                 ||\|___|"======="|"======="|"======="|___|/||
|                 || |---||--------||-| | |-||--------||---| ||
|       __O_____O_ll_lO__ll_O_____O|| |'|'| ||O_____O_ll__Ol_ll_O_____O__
|       o | o o | o o | o o | o o |-----------| o o | o o | o o | o o | o
|      ___|_____|_____|_____|____O =========== O____|_____|_____|_____|___
|                               /|=============|\
|     ()______()______()______() '==== +-+ ====' ()______()______()______()
|     ||{_}{_}||{_}{_}||{_}{_}/| ===== |_| ===== |\{_}{_}||{_}{_}||{_}{_}||
|     ||      ||      ||     / |==== s(   )s ====| \     ||      ||      ||
|    =======================()  =================  ()=======================
|"""

COMPLIMENTS = [
    "You are doing great so far, stay strong my child ~~~",
    "Your personality looks beautiful as is, but do not be afraid to evolve my child ~~~",
    "You have come this far already, yet let us dare to go even further my child ~~~",
    "We are sincerily proud of you my child ~~~",
    "We like your music taste, mind sharing some more with us my child? ~~~",
    "Our thoughts will always come and go, stay vigilant for those that inflict pain my child ~~~",
    "Drop by drop, our sweat will fertilise these lands my child ~~~",
    "Dreams have to be sown and left alone to grow, only then can we reap our rewards my child ~~~",
    "Your worries are just, but they are also just worries my child ~~~",
    "To give away our time is the most generous gesture to all, my child ~~~",
    "We appreciate your efforts and support your chosen path, my child ~~~",
    "If anything is worth doing, do it with pride my child ~~~",
    "Pleasure is temporary, but trust may last forever my child ~~~",
    "Death is not the end. Your actions and gifts will live forever, my child ~~~"
]


# Ask the Buddha to come in.
SB = Pravrallier()

print(HDR)

print("|\n|                  Welcome to the shrine of the Sweating Buddha.")
print("|\n|                           This shrine's key (n) is:")
print("|\n|        {}".format(long_to_bytes(SB.n).hex()[:64]))
print("|        {}".format(long_to_bytes(SB.n).hex()[64:128]))
print("|        {}".format(long_to_bytes(SB.n).hex()[128:192]))
print("|        {}".format(long_to_bytes(SB.n).hex()[192:]))


# PHASE 1
while True:

    try:

        if SB.i == 7:
            print("|\n|\n|  As you walk away with your fortune ticket, you see a lost ticket lying at the bottom of the stairs.")
            print("|  Maybe you should try to decipher it?")
            input("|\n|   Press enter to pick it up...")

            cip, card = SB.encrypt_worry("Tell him: \"I worry that your tyrannical charades are over, false prophet!\"".encode())
            SB.print_card(cip, card)

        worry = input('|\n|\n|  Share the burden of your worry, my child ~~~\n|\n|   >> ')

        if worry[:13] != "I worry that ":
            print("|\n|  Format your worries properly, my child ~~~ [start with 'I worry that ']")
            continue

        if worry == "I worry that your tyrannical charades are over, false prophet!":
            break

        compl = random.SystemRandom().choice(COMPLIMENTS)
        print("|\n|\n|  {}\n|".format(compl))

        SB.print_card(*SB.encrypt_worry(worry.encode()))

    except KeyboardInterrupt:

        print("\n|\n|  Safe travels, my child ~~~\n|\n")
        exit(0)

    except:

        print("|\n|\n|  That is not a request I can fullfill my child ~~~")


# PHASE 2
#encflag = SB.encrypt_flag(FLAG, order=13, txt=REV_TXT)[0]

def pfint(x, char_delay=.1, row_delay=1):
    for row in x.split('\n'):
        for i in range(len(row)):
            print(row[:i], end='\r', flush=True)
            sleep(char_delay)
        print(row)
        sleep(row_delay)

pfint(REV1, char_delay=.08, row_delay=.8)

pfint(REV2, 0.002, row_delay=0)

print("|\n|                  Welcome to the shrine of the Sweating Buddha.")
print("|\n|                           This shrine's key (n) is:")
print("|\n|        {}".format(FLAG_PUBKEY[:64]))
print("|        {}".format(FLAG_PUBKEY[64:128]))
print("|        {}".format(FLAG_PUBKEY[128:192]))
print("|        {}".format(FLAG_PUBKEY[192:]))

pfint(REV3, char_delay=.08, row_delay=.8)

input("|\n|\n|   Press enter to open the gift...")

print("|\n|\n|  Flag: {}".format(FLAG_ENCFLAG))
