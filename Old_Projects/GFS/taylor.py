import numpy as np
from numpy import prod


def factorial(n):
    fac = 1
    if n > 0:
        for i in range(1,n+1):
            fac=fac*i
    return fac

def taylor_approxmation(k,x):
    value = 0
    for n in range(k):
        value = value + ((x**(2*n)*((-1)**n))/factorial(2*n))
    return value

def func(x):
    return taylor_approxmation(10,x)

print(func(3.142))
print(func(6.283))
