def left_rotation(x,n,w):
    #cyclic rotation x <<< n with modulus (2**w)
    n=n%w
    x1 = (x << n) & ((2**w)-1)
    x2 = (x&((2**w)-1)) >> (w-n)
    return x1|x2

def hex_to_arr_byte(x):
    #Divide hex to one bytes and save them in array. -> gives little endian form
    res = []
    modulus = 2**8
    while(x!=0):
        byt = x%modulus
        res.append(byt)
        x = x>>8
    return res

def RC5_key_schedule(w,r,b,K):
    #magic constant P, Q
    if w == 16:
        P = 0xb7e1
        Q = 0x9e37
    elif w == 32:
        P = 0xb7e15163
        Q = 0x9e3779b9
    else: # w==64
        P = 0xB7E151628AED2A6B
        Q = 0x9E3779B97F4A7C15

    modulus = 2**w

    u=w//8
    c = b//u
    L = []
    for i in range(0,c):
        l = 0
        for j in range(0,u):
            l = (l<<8) + (K[i*u + j])
        L.append(l)
    L.reverse()

    res_k = []
    res_k.append(P)
    for i in range(1,2*r+2):
        res_k.append((res_k[i-1]+Q)%modulus)
    print(res_k)

    i = 0
    j = 0
    A = 0
    B = 0

    t = max(c,2*r+2)
    for s in range(1,3*t+1):
        res_k[i] = (res_k[i]+A+B)%modulus
        res_k[i] = left_rotation(res_k[i],3,w)
        A = res_k[i]
        i = (i+1)%(2*r+2)

        L[j] = (L[j] + A + B)
        L[j] = left_rotation(L[j],(A+B),w)
        B = L[j]
        j = (j+1)%c

    return res_k

def RC5_enc(M,w,r,b,K):
    modulus = 2**w

    res_k = RC5_key_schedule(w,r,b,K)
    print(res_k)

    m = bytearray.fromhex(M)

    A = int.from_bytes(m[:w//8], byteorder="little")
    B = int.from_bytes(m[w//8:], byteorder="little")

    A = (A+res_k[0])%modulus
    B = (B+res_k[1])%modulus

    for i in range(1,r+1):
        A = left_rotation(A^B,B,w)
        A = (A+res_k[2*i])%modulus

        B = left_rotation(A^B,A,w)
        B = (B+res_k[2*i+1])%modulus

    C = A.to_bytes(w//8,byteorder="little")+B.to_bytes(w//8,byteorder="little")
    return C.hex()

def test_RC5():
    #test RC5 algo with test vector
    M = "65C178B284D197CC"
    key = "5269F149D41BA0152497574D7F153125"
    K=hex_to_arr_byte(int(key,16))
    #print(int.from_bytes(K, byteorder="little"))
    w=32
    r=12
    b=16
    C = "EB44E415DA319824"
    res = RC5_enc(M,w,r,b,K)
    print(int(C,16) == int(res,16))

test_RC5()