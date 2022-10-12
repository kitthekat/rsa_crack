"""
Christopher Kramer

While the main module in this git (rsacracking.py) is relatively functional,
this is an attempt to use more traditional functional techniques to execute this
package.

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
from operator import eq, mod, lt
from sys import argv
from typing import NoReturn

from functional import seq

import sys

sys.setrecursionlimit(10**6)


def is_prime(p: int) -> bool:
    """Testing for prime number

    Checks if a number is prime by iterating until the 
    ceiling rounded square root of the desired number.

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
    return any(map(lambda i: not(eq(mod(p, i), 0)), range(2, ceil(sqrt(p)))))


def n_bit_prime_generator(n: int = 256) -> int:
    """Bit prime generator
    
    Recursively generates an n-bit prime number based on parameter.
 
    Parameters
    -----------
    n : int
        Whole number indicating the bit size prime number to return (e.g. '256', '1028')
    """
    return num if is_prime(num := random.randint(2, 2 ** n)) else n_bit_prime_generator(n)


def factor(pq: int, __i: int = 2) -> NoReturn:
    """Factoring prime numbers
    
    Finds a factor of a prime multiple.
    Similar to is_prime function, but prints
    factor instead of assessing truthiness.

    Parameters
    ----------
    pq: PrimeMultiple
        an integer representing a potential prime multiple

    __i: int
        iterable value used for recursion
    """
    print(f'found: {__i}') if all([not(eq(mod(pq, __i), 0)), lt(__i, ceil(sqrt(pq)))]) else factor(pq, __i + 1)


def timer(n: int) -> tuple:
    """Time encryption
    
    Times factoring of a prime multiple to show extensibility of RSA encryption.
    """
    return (
               start := datetime.now(),
               factor(n_bit_prime_generator(n) * n_bit_prime_generator(n)),
               datetime.now() - start
           )[1:]


def main(y: int) -> NoReturn:
    """Driver function
    
    Driver function for prime factoring functionality. 
    
    Tests different bitlengths up to user-defined bit ceiling
    and outputs timing to crack into DataFrame.

    DataFrame is exported into Excel file for review.

    Parameters
    -----------
    y : int
        Bit ceiling representing cracking iteration max

    """
    (
        seq(range(15, y))  # convert nbits range to functional sequence
        .map(lambda x: (x, timer(x)))  # map timer function, but keep original sequence
        .map(lambda x: (x[0], x[1][0], x[1][1]))  # timer outputs a tuple, so unpacking
        .to_pandas(columns=['BITS', 'Seconds', 'PQ'])
        .to_excel('times.xlsx')
    )


if __name__ == "__main__":
    try:
        assert int(argv[-1])
        n = int(argv[-1])
    except ValueError:
        print('Invalid input parameter, using bit ceiling n = 24 instead.')
        n = 24
    main(n)
