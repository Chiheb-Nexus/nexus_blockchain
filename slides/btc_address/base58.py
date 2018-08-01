# Base58 implementation using Python3
# Author: Chiheb Nexus - 2018
# License: GPLv3
#
"""BASE58 implementation using Python3"""

import binascii


class Base58:
    '''Base58 implementation'''

    def __init__(self):
        # pylint: disable=C0103
        self.B58_DIGITS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    # pylint: disable=C0103
    def encode(self, var, n=0):
        '''Encode Bytes/int/string to padded base58 encoded string'''

        res, czero, pad = [], 0, 0

        if isinstance(var, bytes):
            # Convert bytes into hex then into an integer
            n = int('0x0' + binascii.hexlify(var).decode('utf8'), 16)
        elif isinstance(var, int):
            # Convert integer into a bytes
            n, var = var, bytes(str(var), 'utf8')
        elif isinstance(var, str):
            # convert string into an integer
            n = int(''.join(map(str, (ord(k) for k in var))))
        else:
            raise Exception('Byte not valid: {0}'.format(n))

        while n > 0:
            n, r = divmod(n, 58)
            res.append(self.B58_DIGITS[r])

        res_final = ''.join(res[::-1])

        for c in var:
            if c == czero:
                pad += 1
            else:
                break

        return self.B58_DIGITS[0] * pad + res_final

    def decode(self, s):
        '''Decode padded base58 encoded string into bytes'''

        if not s:
            return b''

        n = 0
        for c in s:
            n *= 58
            if c not in self.B58_DIGITS:
                raise Exception('Not valid base58: {0}'.format(c))

            digit = self.B58_DIGITS.index(c)
            n += digit

        # Convert n into hex
        h = '{:x}'.format(n)
        if len(h) % 2:
            h = '0' + h

        res = binascii.unhexlify(h.encode('utf8'))

        pad = 0
        for c in s[:-1]:
            if c == self.B58_DIGITS[0]:
                pad += 1
            else:
                break

        return b'\x00' * pad + res
