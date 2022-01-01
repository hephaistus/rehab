#Collection of functions for modular arithmetic.
#Most of them are based on Wikipedia's explaination.

import random

def gcd(a,b):
    if b > a:
        return gcd(b,a)
    
    if b == 0:
        return a
    
    return gcd(b, a%b)

def extended_gcd_internal(a,b,u,u_1,v,v_1):
    #Assumuption : a >= b, init with u=0, u_1 = 1, v=1, v_1=0
    if b == 0:
        return (a, u_1, v_1)
    
    #print("a="+str(a)+" b="+str(b)+ " u="+str(u)+" v="+str(v))
    q = a//b
    
    tmp = u
    u = u_1 - u*q
    u_1 = tmp

    tmp = v
    v = v_1 - v*q
    v_1 = tmp

    return extended_gcd_internal(b, a%b, u,u_1,v,v_1)

def extended_gcd(a,b):
    if b > a:
        (g,v,u)= extended_gcd_internal(b,a,0,1,1,0)
        return (g,u,v)
    
    return extended_gcd_internal(a,b,0,1,1,0)

def legendre_symbol(a,p):
    #determine that a is quadratic residue or non-residue mod p
    #If return value is 1 -> is quadratic residue, -1 -> non residue, 0 -> multiple of p

    return pow(a,(p-1)//2,p)

def sqrt_mod(a,p):
    if p%4 != 3:    
        print("Can't calculate prime fast...")
    else:
        target = pow(a, (p-3)//4, p)
        (g,u,v) = extended_gcd(target,p)
        return u

def Tonelli_Shanks(n,p):
    #Can find square root of modular p. When n is quadratic residue.
    #Find q, s that n - 1 = q * 2^s
    s = 0
    tmp = p- 1
    while(tmp%2 == 0):
        tmp = tmp//2
        s = s + 1
    q = tmp

    #Find z which is quadratic non residue mod p
    rnd = random.randint(1,p-1)

    while(legendre_symbol(rnd,p) != p-1):
        rnd = random.randint(1,p-1)

    z = rnd

    #print("z = "+str(z))

    m = s
    c = pow(z,q,p)
    t = pow(n,q,p)
    r = pow(n,(q+1)//2, p)

    while(t != 0 and t != 1):
        tmp = t
        i = 0
        while(tmp != 1):
            upper = pow(2,i) 
            tmp = pow(tmp,upper,p)
            i = i+1
            
        
        #print("i = "+str(i))

        b = pow(c, (pow(2, m-i-1, p-1)),p)
        m = i
        c = pow(b,2,p)
        t = t*c %p
        r = r*b %p

        #print("t = "+str(t))
    return r

def CRT(num_list, mod_list):
    #num_list = [a1,a2,a3], mod_list = [m1,m2,m3] then this finds x such that x = a1 mod m1, x = a2 mod m2, x = a3 mod m3.
    x = num_list[0]
    m = mod_list[0]

    for i in range(1,len(mod_list)):
        (g,u,v) = extended_gcd(m, mod_list[i])
        x = num_list[i]*m*u + x*mod_list[i]*v
        m = m*mod_list[i]
    
    return x%m
