# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2012-11-11'

import random
import string
import base64
import hmac
import hashlib
import uuid
import math
from struct import Struct
from operator import xor
from itertools import izip, starmap
from os import urandom

from utils.date import current_server_time

SIMPLE_ENCRYPT_KEY = 'UoNsfkFxEc9ayMlpv62Kg0dh5Oe3WItGmRZ4jCbwDQrAqSPJH7VY8z1uiBLTnX'
BASE_SYMBOLS = string.ascii_lowercase + string.ascii_uppercase + string.digits

PBKDF2_HASH_SALT_LENGTH = 12
PBKDF2_HASH_KEY_LENGTH = 24
PBKDF2_HASH_FUNCTION = 'sha256'
PBKDF2_HASH_COST_FACTOR = 10000

_pack_int = Struct('>I').pack

'''
a = set(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
ENCRYPT_KEY = ''.join(random.sample(a, len(a)))
'''


def simple_encrypt(data, base=BASE_SYMBOLS, crypt_key=SIMPLE_ENCRYPT_KEY):
    return (base64.urlsafe_b64encode('%s%s' % (current_server_time(), str(data))).translate(string.maketrans(base, crypt_key))).rstrip('=')


def simple_decrypt(data, base=BASE_SYMBOLS, crypt_key=SIMPLE_ENCRYPT_KEY):
    try:
        return base64.urlsafe_b64decode(str(data).translate(string.maketrans(crypt_key, base)) + '===')[10:]
    except TypeError:
        return False


def generate_random_string(n=16):
    return (u''.join(random.choice(BASE_SYMBOLS) for _ in xrange(n))).lower()


def generate_random_uuid4_string(n=8):
    return str(uuid.uuid4()).replace('-', '')[:n]


def generate_random_uuid4_int(n=6):
    return int(str(int(uuid.uuid4()))[:n])


def pbkdf2_hex(data, salt, iterations=1000, keylen=24, hashfunc=None):
    return pbkdf2_bin(data, salt, iterations, keylen, hashfunc).encode('hex')


def pbkdf2_bin(data, salt, iterations=1000, keylen=24, hashfunc=None):
    hashfunc = hashfunc or hashlib.sha1
    mac = hmac.new(data, None, hashfunc)
    def _pseudorandom(x, mac=mac):
        h = mac.copy()
        h.update(x)
        return map(ord, h.digest())
    buf = []
    for block in xrange(1, -(-keylen // mac.digest_size) + 1):
        rv = u = _pseudorandom(salt + _pack_int(block))
        for i in xrange(iterations - 1):
            u = _pseudorandom(''.join(map(chr, u)))
            rv = starmap(xor, izip(rv, u))
        buf.extend(rv)
    return ''.join(map(chr, buf))[:keylen]


def generate_pbkdf2_hash(password):
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    salt = base64.b64encode(urandom(PBKDF2_HASH_SALT_LENGTH))
    return 'PBKDF2${}${}${}${}'.format(
        PBKDF2_HASH_FUNCTION,
        PBKDF2_HASH_COST_FACTOR,
        salt,
        base64.b64encode(
            pbkdf2_bin(password, salt, PBKDF2_HASH_COST_FACTOR,
                       PBKDF2_HASH_KEY_LENGTH, getattr(hashlib, PBKDF2_HASH_FUNCTION))))


def verify_pbkdf2_hash(password, hash_):
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    algorithm, hash_function, cost_factor, salt, hash_a = hash_.split('$')
    assert algorithm == 'PBKDF2'
    hash_a = base64.b64decode(hash_a)
    hash_b = pbkdf2_bin(password, salt, int(cost_factor), len(hash_a),
                        getattr(hashlib, hash_function))
    assert len(hash_a) == len(hash_b)
    diff = 0
    for char_a, char_b in izip(hash_a, hash_b):
        diff |= ord(char_a) ^ ord(char_b)
    return diff == 0


def alpha_id(idnum, to_num=False, pad_up=False, passkey=None, base=BASE_SYMBOLS):
    """
    alpha_id(123456789, passkey='secret') >> 'qrJFR'
    alpha_id('qrJFR', to_num=True, passkey='secret') >> 123456789
    """

    if passkey:
      i = list(base)
      passhash = hashlib.sha256(passkey).hexdigest()
      passhash = hashlib.sha512(passkey).hexdigest() if len(passhash) < len(base) else passhash
      p = list(passhash)[0:len(base)]
      base = ''.join(zip(*sorted(zip(p,i)))[1])

    len_base = len(base)

    if to_num:
      idnum = idnum[::-1]
      out = 0
      length = len(idnum) -1
      t = 0

      while True:
        bcpow = int(pow(len_base, length - t))
        out += base.index(idnum[t:t+1]) * bcpow
        t += 1
        if t > length:
            break

      if pad_up:
        pad_up -= 1
        if pad_up > 0:
          out -= int(pow(len_base, pad_up))

    else:
      if pad_up:
        pad_up -= 1
        if pad_up > 0:
          idnum += int(pow(len_base, pad_up))

      out = []
      t = int(math.log(idnum, len_base))

      while True:
        bcp = int(pow(len_base, t))
        a = int(idnum / bcp) % len_base
        out.append(base[a:a+1])
        idnum -= a * bcp
        t -= 1
        if t < 0:
            break

      out = ''.join(out[::-1])

    return out


def base36encode(number):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet = string.digits + string.ascii_lowercase

    base36 = ''
    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


def base36decode(number):
    return int(number, 36)