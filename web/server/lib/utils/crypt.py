# -*- coding: utf-8 -*-

import logging
import random
import string
import base64
import hmac
import hashlib
import uuid
import math
import binascii
import zlib

from struct import Struct
from operator import xor
from itertools import izip, starmap
from os import urandom
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

from lib.utils.date import current_server_time

SIMPLE_ENCRYPT_KEY = 'UoNsfkFxEc9ayMlpv62Kg0dh5Oe3WItGmRZ4jCbwDQrAqSPJH7VY8z1uiBLTnX'
BASE_SYMBOLS = string.ascii_lowercase + string.ascii_uppercase + string.digits

PBKDF2_HASH_SALT_LENGTH = 12
PBKDF2_HASH_KEY_LENGTH = 24
PBKDF2_HASH_FUNCTION = 'sha256'
PBKDF2_HASH_COST_FACTOR = 10000

_pack_int = Struct('>I').pack

logger = logging.getLogger('default')


def generate_simple_encrypt_key(base_symbols=BASE_SYMBOLS):
    """
    sample output 'hjF1rkVnm3DUs4ACBoISiL6a7lxyZb5eHJKTWXGpPQ08EqczRv2NO9YgdwfMtu'
    """
    return ''.join(random.sample(set(list(base_symbols)), len(base_symbols)))


def simple_encrypt(data, base_symbols=BASE_SYMBOLS, encrypt_key=SIMPLE_ENCRYPT_KEY):
    """
    simple_encrypt('Ab1-+')
    'TVhkTWDlqVGJIQRATjaB'
    """
    return (base64.urlsafe_b64encode('%s%s' % (current_server_time(), str(data))).translate(
        string.maketrans(base_symbols, encrypt_key))).rstrip('=')


def simple_decrypt(data, base_symbols=BASE_SYMBOLS, encrypt_key=SIMPLE_ENCRYPT_KEY):
    """
    simple_decrypt('TVhkTWDlqVGJIQRATjaB')
    'Ab1-+'
    """
    try:
        return base64.urlsafe_b64decode(str(data).translate(string.maketrans(encrypt_key, base_symbols)) + '===')[10:]
    except TypeError:
        return False


def zlib_compress(data):
    """"
    binascii.hexlify(zlib.compress('Ab1-+'))
    '789c734c32d4d5060003ea012d'
    """
    return binascii.hexlify(zlib.compress(data))


def zlib_decompress(compressed):
    """
    zlib.decompress(binascii.unhexlify('789c734c32d4d5060003ea012d'))
    'Ab1-+'
    """
    return zlib.decompress(binascii.unhexlify(compressed))


def generate_random_string(n=16, make_lower=False):
    """
    Example output, 'nGZGLK1eBJQ8vT6Z'
    """
    result = unicode(''.join(random.choice(BASE_SYMBOLS) for _ in xrange(n)))
    if make_lower:
        result = result.lower()
    return result


def generate_random_uuid4_string(n=8):
    """
    Example output, 'efbd528d'
    """
    return unicode(uuid.uuid4()).replace('-', '')[:n]


def generate_random_uuid4_int(n=12):
    """
    Example output, 184377630539
    """
    result = None
    found = False

    for _ in xrange(0, 11):
        result = int(str(int(uuid.uuid4()))[:n])
        if len(str(result)) == n:
            found = True
            break

    if not found:
        logger.error('cant generate random uuid4 int with length: <%s>' % n)
        result = None

    return result


def pbkdf2_hex(data, salt, iterations=1000, keylen=24, hashfunc=None):
    """
    >> pbkdf2_hex('123456', 'salty')
    '9ff40a4b1e93582e5fe5dc75e23f088c9fe353d70e6e4c8d'
    """
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
    """
    >>> generate_pbkdf2_hash('123456')
    'PBKDF2$sha256$10000$TP1a32/LgM53hsDB$VOX1FcsHLcbtcDPBf6+uALtlOCaUkDNC'
    """
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
        length = len(idnum) - 1
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
    """
    base36encode(10) >> 'a'
    base36encode(72) >> '20'
    base36encode(82) >> '2a'
    """
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


def base36decode(value):
    """
    base36decode('2a') >> 82
    """
    return int(value, 36)


def generate_hash_from_dict(input_dict):
    """
    generate_hash_from_dict({'a':7, 'b': 'foo', 'c': [4,7,9]})
    >> 'bSrdDIV8bSthDJ2l41tMCWeujqdFjWsE45dF41Y0o5NpCWel41bMCW3owWdFw5dFDJ8p7r'
    simple_decrypt('bSrdDIV8bSthDJ2l41tMCWeujqdFjWsE45dF41Y0o5NpCWel41bMCW3owWdFw5dFDJ8p7r')
    >> "[('a', 7), ('b', 'foo'), ('c', [4, 7, 9])]"
    """
    return simple_encrypt('{}'.format(sorted(input_dict.items())))


def generate_rsa_keys(passphrase, bits=4096):
    """
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: passphrase String password
    param: bits The key length in bits
    Return private key and public key
    Usage example:
        import os
        from lib.utils.crypt import *
        from lib.utils.file import *
        from settings import BANK_CARD_CERT_PATH, BANK_CARD_RSA_PASSPHRASE
        priv, pub = generate_rsa_keys(BANK_CARD_RSA_PASSPHRASE)
        output_file('id_rsa.pub', pub, BANK_CARD_CERT_PATH)
        output_file('id_rsa', priv, BANK_CARD_CERT_PATH)
        public_key_loc = os.path.join(BANK_CARD_CERT_PATH, 'id_rsa.pub')
        private_key_loc = os.path.join(BANK_CARD_CERT_PATH, 'id_rsa')
        message = 'My Data should be --> safe!'
        encrypted = encrypt_rsa(public_key_loc, message)
        try:
            decrypted = decrypt_rsa(private_key_loc, encrypted, BANK_CARD_RSA_PASSPHRASE)
        except ValueError:
            decrypted = None
    """
    random_generator = Random.new().read
    new_key = RSA.generate(bits, random_generator, e=65537)
    public_key = new_key.publickey().exportKey('PEM')
    private_key = new_key.exportKey('PEM', passphrase, pkcs=1)
    return private_key, public_key


def encrypt_rsa(public_key_loc, message):
    """
    param: public_key_loc Path to public key
    param: message String to be encrypted
    return base64 encoded encrypted string
    """
    key = open(public_key_loc, 'r').read()
    rsakey = RSA.importKey(key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted = rsakey.encrypt(message)
    return encrypted.encode('base64')


def decrypt_rsa(private_key_loc, encrypted, passphrase=''):
    """
    param: public_key_loc Path to your private key
    param: package String to be decrypted
    param: passphrase String password
    return decrypted string
    """
    key = open(private_key_loc, 'r').read()
    rsakey = RSA.importKey(key, passphrase=passphrase)
    rsakey = PKCS1_OAEP.new(rsakey)
    decrypted = rsakey.decrypt(base64.b64decode(encrypted))
    return decrypted


def sign_data_with_rsa(private_key_loc, data, passphrase):
    """
    param: private_key_loc Path to your private key
    param: package Data to be signed
    param: passphrase String password
    return: base64 encoded signature
    """
    key = open(private_key_loc, 'r').read()
    rsakey = RSA.importKey(key, passphrase=passphrase)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    # It's being assumed the data is base64 encoded, so it's decoded before updating the digest
    digest.update(base64.b64decode(data))
    sign = signer.sign(digest)
    return base64.b64encode(sign)


def verify_rsa_sign(public_key_loc, signature, data):
    """
    Verifies with a public key from whom the data came that it was indeed
    signed by their private key
    param: public_key_loc Path to public key
    param: signature String signature to be verified
    return: Boolean. True if the signature is valid; False otherwise.
    """
    pub_key = open(public_key_loc, 'r').read()
    rsakey = RSA.importKey(pub_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    # Assumes the data is base64 encoded to begin with
    digest.update(base64.b64decode(data))
    if signer.verify(digest, base64.b64decode(signature)):
        return True
    return False