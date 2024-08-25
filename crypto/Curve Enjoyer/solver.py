from sage.rings.factorint import factor_trial_division
from ecdsa import ellipticcurve
from pwn import *
from sympy import sqrt_mod
from sage.all import EllipticCurve, Zmod
from sympy.ntheory.modular import crt
from Crypto.Util.number import *

# io = process(["python3","server.py"])
io = remote("103.217.145.97","8015")

def checkPoint(p, a, b, x, y1):
    y2 = (pow(x, 3, p) + a*x + b) % p
    y = sqrt_mod(y2,p)
    return y == y1

def getIn(bits):
    io.sendlineafter(b'the prime: ',str(bits).encode())
    io.recvuntil(b'p = ')
    p = int(io.recvline().decode().strip())
    io.recvuntil(b'G = ')
    # io.recvuntil(b'P = ')
    P = [int(i) for i in io.recvline().decode().strip()[1:-1].split(',')]
    io.recvuntil(b'Q = ')
    Q = [int(i) for i in io.recvline().decode().strip()[1:-1].split(',')]
    return p, P, Q


# we have two point and recovery a and b
def recover(X, Y, p):
    x1,y1 = X
    x2,y2 = Y
    c1 = x1**3 - y1**2
    c2 = x2**3 - y2**2
    k = x1-x2
    c = c1-c2

    a = (pow(k,-1,p)*-c)%p
    b = -1*(a*x1 + x1**3 -y1**2)%p
    return a, b

def solver(g, h, modd):
    cek = 1
    ret = None, None
    for i in range(2, modd):
        if(h*i==g):
            if(cek==1):
                ret = i, modd
                cek = 2
            elif(cek==2):
                return None, None            
    return ret

m = []
r = []
for _ in range(300):
    print("Generating dataset:",_)
    p, P, Q = getIn(128)
    a, b = recover(P, Q, p)
    curve = ellipticcurve.CurveFp(p, a, b)
    E = EllipticCurve(Zmod(p),[a,b])
    order = E.order()
    P = E(P[0], P[1])
    Q = E(Q[0], Q[1])
    # print(order)

    limitnum = 20000
    fact = [i for i in factor_trial_division(order, limitnum)]
    for i, j in fact:
        modd = pow(i, j)
        if(modd<limitnum):
            g = Q*((order)//modd)
            h = P*((order)//modd)
            if(g[0]==0 or h[0]==0 or g[0]==h[0]): 
                pass
            else:
                rs, ms = solver(g, h, modd)
                # print(rs, ms)
                if(ms!= None and rs != None):
                    m.append(ms)
                    r.append(rs)
            
print(m, r)
hasil = crt(m, r)
flag = long_to_bytes(int(hasil[0]))
print(flag)

