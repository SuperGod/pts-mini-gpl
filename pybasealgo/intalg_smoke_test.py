#! /usr/bin/python2.6

"""Fast unit tests for the intalg module."""

__author__ = 'pts@fazekas.hu (Peter Szabo)'

import math
import unittest

import intalg


class IntalgSmokeTest(unittest.TestCase):
  def testBitCount(self):
    self.assertEquals(1, intalg.bit_count(0))
    self.assertEquals(1, intalg.bit_count(1))
    self.assertEquals(2, intalg.bit_count(2))
    self.assertEquals(2, intalg.bit_count(3))
    self.assertEquals(6, intalg.bit_count(63))
    self.assertEquals(7, intalg.bit_count(64))
    self.assertEquals(7, intalg.bit_count(75))
    self.assertEquals(11, intalg.bit_count(2047))
    self.assertEquals(12, intalg.bit_count(2048))
    self.assertEquals(12, intalg.bit_count(-4007))
    self.assertEquals(12, intalg.bit_count(4095))
    self.assertEquals(13, intalg.bit_count(4096))
    self.assertEquals(1204, intalg.bit_count(1 << 1203))
    self.assertEquals(1204, intalg.bit_count(-(1 << 1203)))
    self.assertEquals(1205, intalg.bit_count(1 << 1204))
    self.assertEquals(1206, intalg.bit_count(1 << 1205))
    self.assertEquals(1207, intalg.bit_count(1 << 1206))

  def testLog256Table(self):
    self.assertEquals(257, len(intalg.LOG2_256_TABLE))
    self.assertEquals(1762, intalg.LOG2_256_TABLE[0x76])

  def testLog256More(self):
    self.assertEquals(1762, intalg.log2_256_more(0x76))
    self.assertEquals(6882, intalg.log2_256_more(123456789))
    self.assertEquals(2048, intalg.log2_256_more(256))
    self.assertEquals(2051, intalg.log2_256_more(257))  # 2050 would have been enough.
    self.assertEquals(2051, intalg.log2_256_more(258))
    self.assertEquals(2054, intalg.log2_256_more(259))
    self.assertEquals(123 << 8, intalg.log2_256_more(1 << 123))
    self.assertEquals(1203 << 8, intalg.log2_256_more(1 << 1203))
    self.assertEquals(1204 << 8, intalg.log2_256_more(1 << 1204))
    self.assertEquals(1205 << 8, intalg.log2_256_more(1 << 1205))
    self.assertEquals(1206 << 8, intalg.log2_256_more(1 << 1206))

  def testLogMore(self):
    b_coeff = 123457 * math.log(3)
    for i in xrange(100):
      a = intalg.log_more(123457, 3 ** i)
      b = b_coeff * i
      assert b <= a, (i, a, b)
      assert b + b / 256 >= a, (i, a, b)

  def testSqrtFloor(self):
    assert intalg.sqrt_floor(41 ** 6) == 41 ** 3
    assert intalg.sqrt_floor((41 ** 3 + 1) ** 2 - 1) == 41 ** 3
    assert intalg.sqrt_floor(10 ** 5000) == 10 ** 2500  # 10e5000 is float overflow.

    for n in xrange(100):
      r = intalg.sqrt_floor(n)
      rk = r * r
      assert rk <= n < (r + 1) ** 2, (n, r)

    for ni in xrange(100):
      n = int(37 + 100 * 1.5 ** ni)
      r = intalg.sqrt_floor(n)
      rk = r * r
      assert rk <= n < (r + 1) ** 2, (n, r)

  def testRootFloor(self):
    self.assertEquals((41 ** 3, True), intalg.root_floor(41 ** 6, 2))
    self.assertEquals((41 ** 2, True), intalg.root_floor(41 ** 6, 3))
    self.assertEquals((41, False), intalg.root_floor(42 ** 6 - 30 ** 6, 6))
    self.assertEquals((42 ** 2 - 1, False), intalg.root_floor(42 ** 6 - 13 ** 6, 3))
    self.assertEquals((10 ** 2500, True), intalg.root_floor(10 ** 5000, 2))  # 10e5000 > max_float.
    self.assertEquals((2, True), intalg.root_floor(2 ** 1000, 1000))
    self.assertEquals((3, True), intalg.root_floor(3 ** 1000, 1000))
    self.assertEquals((42 ** 3, True), intalg.root_floor(42 ** 9000, 3000))

    for k in (2, 3, 4, 5, 6, 7):
      for n in xrange(100):
        r, is_exact = intalg.root_floor(n, k)
        rk = r ** k
        assert rk <= n < (r + 1) ** k
        assert (rk == n) == is_exact, (n, k, r, is_exact, rk)

    for k in (2, 3, 4, 5, 6, 7):
      for ni in xrange(20):
        n = int(37 + 100000 * 3 ** ni)
        r, is_exact = intalg.root_floor(n, k)
        rk = r ** k
        assert rk <= n < (r + 1) ** k
        assert (rk == n) == is_exact, (n, k, r, is_exact, rk)

  def testFractionToFloat(self):
    self.assertEquals(32.5, intalg.fraction_to_float(2 ** 10005 + 2 ** 9999, 2 ** 10000))
    self.assertEquals(32.5, intalg.fraction_to_float(2 ** 10005 + 2 ** 9999 + 1, 2 ** 10000))

  def testYieldSlowFactorize(self):
    self.assertEquals(list(intalg.yield_slow_factorize(1)), [])
    self.assertEquals(list(intalg.yield_slow_factorize(36)), [2, 2, 3, 3])
    self.assertEquals(list(intalg.yield_slow_factorize(180)), [2, 2, 3, 3, 5])
    self.assertEquals(list(intalg.yield_slow_factorize(3 ** 1000 * 29 ** 57)), [3] * 1000 + [29] * 57)
    self.assertEquals(list(intalg.yield_slow_factorize(2 * 3 * 5 * 7 * 7 * 11 * 13 * 17 * 19)), [2, 3, 5, 7, 7, 11, 13, 17, 19])

  def testFactorizeMedium(self):
    n = intalg.next_prime(intalg._SMALL_PRIME_LIMIT) ** 2 - 10
    limit = n + 100
    while n < limit:  # xrange can't take a long (n).
      a = list(intalg.yield_slow_factorize(n))
      b = intalg.finder_slow_factorize(n)
      c = intalg.factorize(n)
      d = intalg.factorize(n, divisor_finder=intalg.brent)
      e = intalg.factorize(n, divisor_finder=intalg.pollard)
      assert a == b == c == d == e, (n, a, b, c, d, e)
      n += 1

  def testFactorizeSmall(self):
    for n in xrange(1, 100):
      a = list(intalg.yield_slow_factorize(n))
      b = intalg.finder_slow_factorize(n)
      c = intalg.factorize(n, divisor_finder=intalg.brent)
      d = intalg.factorize(n, divisor_finder=intalg.pollard)
      assert a == b == c == d, (n, a, b, c, d)

  def testBrentPrime(self):
    random_obj = intalg.MiniIntRandom(42)
    for n in intalg.primes_upto(100):
      b = intalg.brent(n, random_obj)
      self.assertEquals(b, n)

  def testPollardPrime(self):
    random_obj = intalg.MiniIntRandom(42)
    for n in intalg.primes_upto(100):
      b = intalg.pollard(n, random_obj)
      self.assertEquals(b, n)

  def testBrentComposite(self):
    random_obj = intalg.MiniIntRandom(42)
    for n in intalg.yield_composites():
      if n > 100:
        break
      b = intalg.brent(n, random_obj)
      assert b > 1
      assert b <= n
      self.assertEquals(0, n % b, (b, n))

  def testPollardComposite(self):
    random_obj = intalg.MiniIntRandom(42)
    for n in intalg.yield_composites():
      if n > 100:
        break
      b = intalg.pollard(n, random_obj)
      assert b > 1
      assert b <= n
      self.assertEquals(0, n % b, (b, n))

  def testTotient(self):
    expected = [0, 1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4, 12, 6, 8, 8, 16, 6,
                18, 8, 12, 10, 22]
    self.assertEquals([0], intalg.totients_upto(0))
    self.assertEquals([0], intalg.totients_upto(0, force_recursive=1))
    self.assertEquals([0, 1], intalg.totients_upto(1, force_recursive=1))
    self.assertEquals([0, 1], intalg._totients_upto_iter(1))
    self.assertEquals([0, 1, 1], intalg.totients_upto(2, force_recursive=1))
    self.assertEquals([0, 1, 1], intalg._totients_upto_iter(2))
    self.assertEquals(expected, intalg.totients_upto(23))
    self.assertEquals(expected, intalg.totients_upto(23, force_recursive=1))
    self.assertEquals(expected, intalg._totients_upto_iter(23))
    self.assertEquals(expected, map(intalg.totient, xrange(24)))
    limit = 500
    expected2 = map(intalg.totient, xrange(limit + 1))
    self.assertEquals(expected2, intalg.totients_upto(limit))
    self.assertEquals(expected2, intalg.totients_upto(limit, force_recursive=1))
    self.assertEquals(expected2, intalg._totients_upto_iter(limit))


if __name__ == '__main__':
  unittest.main()
