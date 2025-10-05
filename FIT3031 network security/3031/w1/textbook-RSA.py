import random
from random import randint
import os

# Python implementation of Fermat's primality test to generate prime numbers of any bit length.
# (https://github.com/bopace/generate-primes)
def generate_big_prime(n):
    found_prime = False
    while not found_prime:
        p = randint(2**(n-1), 2**n)
        if isPrime(p, 5):
            return p
def isPrime(num, test_count):
    if num == 1:
        return False
    if test_count >= num:
        test_count = num - 1
    for x in range(test_count):
        val = randint(1, num - 1)
        if pow(val, num-1, num) != 1:
            return False
    return True

# greatest common factor
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

# A fast and effient implementation of power mod 
# (https://helloacm.com/compute-powermod-abn/)
def powmod(a, b, n):
    r = 1
    while b > 0:
        if b & 1 == 1:
            r = r * a % n
        b //= 2
        a = a * a % n
    return r

#returns y  such that e * y == 1 modulo phi
#https://stackoverflow.com/questions/44044143/why-is-my-rsa-implementation-in-python-not-working
def invert(e, phi):
    a, b, u = 0, phi, 1
    while(e > 0):
        q = b // e
        e, a, b, u = b % e, u, e, a-q*u
    if (b == 1):
        return a % phi
    else:
        print("Must be coprime!")

# generate a key pair
def rsa_keygen(N):
    status = True

    p = random.getrandbits(N//2)
    q = random.getrandbits(N//2)

    e = 65537
    n =  p * q
    phi_n = ( p - 1) * ( q - 1)
    if gcd(e , phi_n) == 1:
        d = invert(e, phi_n )
    else :
        status = False
        d = -1
    return status , n , e , d

def main():
    _ , n , e , d = rsa_keygen(2048)
    random.seed(a = os.urandom (512), version = 2)
    r = randint(0,10000 )
    c = powmod(r , e , n )
    print( 'n ={}\n e ={}\n'.format (n ,e))
    print( 'Random number is {} '.format(r))
    print( 'Encrypted random number is \n{} '.format(c))                                   
if __name__ == '__main__':
    main()
