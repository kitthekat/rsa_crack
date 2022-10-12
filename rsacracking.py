"""
Christopher Kramer

exponential function:
$f(x) = 2^{(x-24)}$
$f(1024) \approx 1.0715 x 10^304 milliseconds \approx 3.3 x 10^293 years$

USAGE:
python rsacracking.py [optional n]

Where n = the ceiling of bit lengths to test (15, 16, ..., n)
"""

import random
from datetime import datetime
from math import sqrt, ceil
from operator import gt, eq, mod
from sys import argv
from typing import NoReturn

import pandas as pd

#  typehints
BitCeiling = int
BitLength = int
PrimeFactor = int
PrimeMultiple = int


def is_prime(p: int) -> bool:
    """Testing for prime number

    Checks if a number is prime by iterating until the 
    ceiling rounded squareroot of the desired number.

    During iteration, if any values evenly denominate 
    into the desired number, the number is not prime 
    """
    for i in range(2, ceil(sqrt(p))):
        if eq(p % i, 0): return False
    return True

def is_prime_test(p: int) -> bool:
    """Generator-based prime finder
    
    Test function to see if testing primes is more 
    efficient with generators. It's not.

    Checks if a number is prime by iterating until the 
    ceiling rounded squareroot of the desired number.

    During iteration, if any values evenly denominate 
    into the desired number, the number is not prime 
    """
    def prime_checker(p):
        i = 2
        while i < ceil(sqrt(p)):
            yield eq(p % i, 0)
            i+=1
        yield True
    return not(any(prime_checker(p)))

def nBitPrime(n: BitLength) -> int:
    num = random.randint(0, 2**n)
    return num if all([gt(num, 2), is_prime(num)]) else nBitPrime(n)


def factor(pq: PrimeMultiple) -> NoReturn:
    for i in range(2, pq + 1):
        if eq(mod(pq, i), 0):
            print(f'found: {i}')
            return True


def timer(n: BitLength) -> tuple:
    pq = nBitPrime(n) * nBitPrime(n)
    print(f'pq:{pq}')
    start = datetime.now()
    factor(pq)
    stop = datetime.now() - start
    print(stop)
    return datetime.now() - start, pq


def main(y: BitCeiling) -> NoReturn:
    df = pd.DataFrame(list(range(15, y)), columns=['BITS'])
    df[['Seconds', 'PQ']] = pd.DataFrame(df['BITS'].apply(timer).to_list(), index=df.index)
    df.to_excel('times.xlsx')


if __name__ == "__main__":
    try:
        assert int(argv[-1])
        n = int(argv[-1])
    except ValueError:
        n = 24
    main(n)
