import math
from random import *

#Algorithm is made by using the Shank's algorithm from below URL.
#https://www.rieselprime.de/ziki/Modular_square_root#Modulus_congruent_to_1_modulo_8

def Shanks(a,m):
    #a is number for v^2 == a (mod m)
    #m is prime
    #Use this algo when m%8==1
    e = 1
    while(((m-1)%(2**e)) == 0):
        e = e+1
    e = e-1
    q = (m-1)//(2**e)
    #print("e="+str(e)+" q="+str(q))

    x = randint(1,m)
    z = pow(x,q,m)
    while(pow(z,(e-1)%(m-1),m)==1):
        x = randint(1,m)
        z = pow(x,q,m)

    y = z
    r = e
    x = pow(a,(q-1)//2,m)
    v = (a*x)%m
    w = (v*x)%m

    while(w!=1):
        k = 1
        while(pow(w,2**k,m) != 1):
            k = k+1
        if(r==k):
            return (1,1)
        d = pow(y,pow(2,r-k-1,m-1),m)
        y = pow(d,2,m)
        r = k
        v = (d*v)%m
        w = (w*y)%m
    #v and -v is solution
    return (v,(-v)%m)
