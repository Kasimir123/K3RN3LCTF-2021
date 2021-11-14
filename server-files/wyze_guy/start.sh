#!/bin/bash
KERNEL=./vmlinux-4.9.0-3-4kc-malta
INITRD=./initrd.img-4.9.0-3-4kc-malta
HDD=./chall.qcow2
EXTRA_PORT=4444

qemu-system-mipsel -M malta -m 512 \
                   -kernel ${KERNEL} \
		   		-initrd ${INITRD} \
				-hdd ${HDD} \
				   -net nic,model=e1000 \
                   -net user,hostfwd=tcp:0.0.0.0:${EXTRA_PORT}-:4444 \
                   -display none -vga none -nographic \
                   -append 'nokaslr root=/dev/sda1 r'

exit 0
