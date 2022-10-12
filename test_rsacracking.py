
import unittest
import os
import rsacracking
from io import StringIO
from unittest.mock import patch
import datetime


class rsacrackingTest(unittest.TestCase):
	"""
	Tests for functions in the rsacracking module.
	"""
	def setUp(self):
		self.n = 24
		self.outpath = 'testing_times.xlsx'
		self.prime_ns = [
			3, 5, 7, 11, 13, 17, 19,
			23, 29, 31, 37, 41, 43,
			47, 53, 59, 61, 67, 71,
			73, 79, 83, 89
		]
		self.not_prime_ns = [
			4, 6, 8, 10, 12, 14, 16, 18,
			20, 22, 24, 26, 28, 30, 32, 34,
			36, 38, 40, 42, 44, 46, 48, 50,
			52, 54, 56, 58, 60, 62, 64, 66
		]

	def tearDown(self):
		os.remove(self.outpath) if os.path.exists(self.outpath) else None

	def test_is_prime_positive(self):
		"""
		Tests 3 conditions:
			1) does is_prime return a boolean type output
			2) does is_prime correctly classify a known prime number (output = True)
			3) does is_prime correctly classify a series of known prime numbers
		"""
		p_test = rsacracking.is_prime(self.prime_ns[0])
		self.assertIsInstance(p_test, bool)
		self.assertTrue(p_test)
		self.assertTrue(all([rsacracking.is_prime(p) for p in self.prime_ns]))

	def test_is_prime_negative(self):
		"""
		Tests 3 conditions:
			1) does is_prime return a boolean type output
			2) does is_prime correctly classify a known non-prime number (output = False)
			3) does is_prime correctly classify a series of known non-prime numbers
		"""
		p_test = rsacracking.is_prime(self.not_prime_ns[-1])
		self.assertIsInstance(p_test, bool)
		self.assertFalse(p_test)
		self.assertFalse(all([rsacracking.is_prime(p) for p in self.not_prime_ns]))

	def test_n_bit_prime_generator(self):
		"""
		Tests 2 conditions:
			1) does n_bit_prime_generator output an integer
			2) does n_bit_prime_generator return a prime number
				*this assumes the is_prime function works correctly, tested above
		"""
		prime_n = rsacracking.n_bit_prime_generator(self.n)
		self.assertIsInstance(prime_n, int)
		self.assertTrue(rsacracking.is_prime(prime_n))

	@patch('builtins.print')
	def test_factor(self, mock_print):
		rsacracking.factor(self.prime_ns[-1])
		mock_print.assert_called_with('found: 10')

	def test_timer(self):
		out = rsacracking.timer(self.n)
		self.assertIsInstance(out, tuple)
		self.assertIsInstance(out[1], int)
		self.assertIsInstance(out[0], datetime.timedelta)

	def test_main(self):
		rsacracking.main(self.n, self.outpath)
		self.assertTrue(os.path.exists(self.outpath))

