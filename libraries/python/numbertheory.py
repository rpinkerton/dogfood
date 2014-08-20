import math
import fractions

def fibonacci(n):
    """Returns the nth fibonacci number"""
    if n == 0:
        return 1
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def primes(limit):
    """Returns a list of primes up to limit"""
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

def is_prime(num):
    """Returns whether or not a given number is prime"""
    result = True
    for prime in primes(int(math.ceil(math.sqrt(num)))):
        result &= coprime(prime, num)
    return result

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

def divisors(n):
    """Returns all the divisors of n"""
    divisors = []
    if n == 1 or n == 0:
        return []
    for num in range(2, int(math.ceil(math.sqrt(n))) + 1):
        if n % num == 0:
            divisors.append(num)
            divisors.append(n / num)
    if math.sqrt(n) % 1 == 0:
        divisors.remove(int(math.sqrt(n)))
    if n / math.ceil(math.sqrt(n)) % 1 == 0 and math.sqrt(n) % 1 != 0:
        divisors.remove(int(math.ceil(math.sqrt(n))))
        divisors.remove(int(n / math.ceil(math.sqrt(n))))
    divisors.append(1)
    return divisors

def mul_order(num, base):
    """Returns the multiplicative order of num mod base"""
    order = 1
    current = num
    while current % base != 1:
        current = (current * num) % base
        order += 1
    return order

def coprime(a, b):
    """Returns a boolean indicating whether two numbers are coprime"""
    if fractions.gcd(a, b) == 1:
        return True
    return False

def coprime_less(n):
    """Returns the list of numbers less than n which are coprime"""
    coprimes = []
    for i in range(1, n + 1):
        if coprime(i, n):
            coprimes.append(i)
    return coprimes

def euler_totient(n):
    """Returns the euler totient of n"""
    factorization = prime_factorization(n)
    totient = n
    for prime, _ in factorization:
        totient *= (1.0 - 1.0/prime)
    return int(totient)

def moebius(n):
    """Returns the moebius function of n"""
    factorization = prime_factorization(n)
    result = 1
    for _, multiplicity in factorization:
        if multiplicity != 1:
            return 0
        result *= -1
    return result
