import math
import fractions

def fibonacci(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def primes(limit):
    limitn = limit+1
    not_prime = [False] * limitn
    primes = []

    for i in range(2, limitn):
        if not_prime[i]:
            continue
        for f in xrange(i*2, limitn, i):
            not_prime[f] = True

        primes.append(i)

    return primes

def prime_factorization(n, max_prime_digits=5):
    """Returns the prime factorization of n"""
    factorization = []
    for prime in primes(10 ** max_prime_digits):
        multiplicity = 0
        if n % prime == 0:
            while n % prime == 0:
                multiplicity += 1
                n /= prime
            factorization.append((prime, multiplicity))
        if n == 1:
            break
    return factorization

def coprime(a, b):
    if fractions.gcd(a, b) == 1:
        return True
    return False

def coprime_less(n):
    coprimes = []
    for i in range(1, n + 1):
        if coprime(i, n):
            coprimes.append(i)
    return coprimes

        
