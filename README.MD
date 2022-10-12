Simple proof-of-concept showing exponentiality of cracking time for RSA encryption

By: Christopher Kramer

Proof of RSA encryption security using algorithms to show time complexity
of cracking prime numbers of user-defined bit length.

Output shows the exponential cracking time function:

$f(x) = 2^{(x-24)}$

Indicating that a bitlength of 1024 will take a long time to crack conventionally:

$f(1024) \approx 1.0715 x 10^304 milliseconds \approx 3.3 x 10^293 years$

USAGE:
python rsacracking.py [optional n]

Where n = the ceiling of bit lengths to test (15, 16, ..., n)

Exports result of iterative cracking to Excel.
