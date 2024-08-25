from pwn import *

def getMess():
    io = remote("27.112.79.222","8012")
    io.recvuntil(b'n = ')
    n = int(io.recvline().decode().strip())
    io.recvuntil(b'e = ')
    e = int(io.recvline().decode().strip())
    io.recvuntil(b'c = ')
    c = int(io.recvline().decode().strip())
    io.close()
    return n, e, c

with open("data3.txt","wb") as f:
    for _ in range(500):
        n,e,c = getMess()
        f.write(f'{n}:{e}:{c}\n'.encode())
