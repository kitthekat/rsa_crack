"""
Christopher Kramer

Proof of RSA encryption security using algorithms to show time complexity
of cracking prime numbers of user-defined bit length.

exponential function:
$f(x) = 2^{(x-24)}$
$f(1024) \approx 1.0715 x 10^304 milliseconds \approx 3.3 x 10^293 years$

USAGE:
python rsacracking.py [optional n]

Where n = the ceiling of bit lengths to test (15, 16, ..., n)

Exports result of iterative cracking to Excel.
"""

import random
from datetime import datetime
from math import sqrt, ceil
from operator import eq, mod
from sys import argv
from typing import NoReturn, Optional

import pandas as pd


def is_prime(p: int) -> bool:
    """Testing for prime number

    Checks if a number is prime by iterating until the 
    ceiling rounded squareroot of the desired number.

    During iteration, if any values evenly denominate 
    into the desired number, the number is not prime

    Parameters
    -----------
    p : int
        A suspected prime integer
    """
    for i in range(2, ceil(sqrt(p))):
        if eq(mod(p, i), 0): return False
    return True


def is_prime_test(p: int) -> bool:
    """Generator-based prime number tester
    
    Test function to see if testing primes is more 
    efficient with generators. It's not.

    Checks if a number is prime by iterating until the 
    ceiling rounded squareroot of the desired number.

    During iteration, if any values evenly denominate 
    into the desired number, the number is not prime

    Parameters
    -----------
    p : int
        A suspected prime integer
    """
    def prime_checker(p):
        i = 2
        while i < ceil(sqrt(p)):
            yield eq(p % i, 0)
            i+=1
        yield True 
    return not(any(prime_checker(p)))


def n_bit_prime_generator(n: int = 256) -> int:
    """Bit prime generator
    
    Recursively generates an n-bit prime number based on parameter.
 
    Parameters
    -----------
    n : int
        Whole number indicating the bit size prime number to return (e.g. '256', '1028')
    """
    num = random.randint(2, 2**n)
    return num if is_prime(num) else n_bit_prime_generator(n)


def factor(pq: int) -> Optional[bool]:
    """Factoring prime numbers
    
    Finds a factor of a prime multiple.
    Similar to is_prime function, but prints
    factor instead of assessing truthiness.

    Parameters
    ----------
    pq: PrimeMultiple
        an integer representing a potential prime multiple
    """
    i = 0
    while not(eq(mod(pq, i), 0)): i += 1
    print(f'found: {i}')


def timer(n: int) -> tuple:
    """Time encryption
    
    Times factoring of a prime multiple to show extensibility of RSA encryption.
    """
    pq = n_bit_prime_generator(n) * n_bit_prime_generator(n)
    print(f'pq:{pq}')
    start = datetime.now()
    factor(pq)
    stop = datetime.now() - start
    print(stop)
    return stop, pq


def main(y: int) -> NoReturn:
    """Driver function
    
    Driver function for prime factoring functionality. 
    
    Tests different bitlengths up to user-defined bit ceiling
    and outputs timing to crack into DataFrame.

    DataFrame is exported into excel file for review.

    Parameters
    -----------
    y : int
        Bit ceiling representing cracking iteration max

    """
    df = pd.DataFrame(list(range(15, y)), columns=['BITS'])
    df[['Seconds', 'PQ']] = pd.DataFrame(df['BITS'].apply(timer).to_list(), index=df.index)
    df.to_excel('times.xlsx')


if __name__ == "__main__":
    try:
        assert int(argv[-1])
        n = int(argv[-1])
    except ValueError:
        print('Invalid input parameter, using bit ceiling n = 24 instead.')
        n = 24
    main(n)
