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
from sympy import isprime

import sys

sys.setrecursionlimit(10**9)


def n_bit_prime_generator(n: int = 256) -> int:
    """Bit prime generator
    
    Recursively generates an n-bit prime number based on parameter.
 
    Parameters
    -----------
    n : int
        Whole number indicating the bit size prime number to return (e.g. '256', '1028')
    """
    return num if isprime(num := random.randint(2, 2 ** n)) else n_bit_prime_generator(n)


def factor(pq: int) -> NoReturn:
    """Factoring prime numbers

    Finds a factor of a prime multiple.
    Similar to is_prime function, but prints
    factor instead of assessing truthiness.

    Functional programming note:
    This could be written recursively as

        factor(pq, __i + 1) if not(eq(mod(pq, __i), 0)) and lt(__i, ceil(sqrt(pq))) \\
            else print('found: {__i}')

    if a parameter __i = 2 is added to the function definition.
    However, this hits python's recursion limit, even with maxing
    Window recursion setting. Therefor this is left as-is.

    Parameters
    ----------
    pq: PrimeMultiple
        an integer representing a potential prime multiple

    __i: int
        iterable value used for recursion
    """
    i = 2
    while not (eq(mod(pq, i), 0)) and lt(i, ceil(sqrt(pq))):
        i += 1
    print(f'found: {i}')


def timer(n: int) -> tuple:
    """Time encryption
    
    Times factoring of a prime multiple to show extensibility of RSA encryption.
    """
    return (
               start := datetime.now(),
               (pq := n_bit_prime_generator(n) * n_bit_prime_generator(n), factor(pq))[0],
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
        .map(lambda x: (x[0], x[1][1], x[1][0]))  # timer outputs a tuple, so unpacking
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
