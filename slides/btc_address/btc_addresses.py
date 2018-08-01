# Générer des clés privées et publiques de Bitcoin
# Author: Chiheb Nexus - 2018
# License: GPLv3
#
# Livre:
# http://chimera.labs.oreilly.com/books/1234000001802/ch04.html#_implementing_keys_and_addresses_in_python
# Liste des prefix de Bitcoin:
# https://en.bitcoin.it/wiki/List_of_address_prefixes
# Exemple: Private key => WIF:
# https://en.bitcoin.it/wiki/Wallet_import_format
# Exemple: WIF => Adresse publique:
# https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
#
"""Generate Bitcoin addresses"""

import os
import hashlib
import binascii
import ecdsa
from base58 import Base58


class BTCAddress:
    '''Generate Bitcoin addresses'''

    def __init__(self):
        self.base58 = Base58()
        # 2 ^ 256 + 1
        # pylint: disable=C0103
        self.N = (1 << 256) + 1

    def generate_privkey(self, bits=32):
        '''Générer un random 32 bit seed'''
        while True:
            # Générer une séqunce de bits aléatoires
            # https://docs.python.org/3/library/os.html#os.urandom
            priv_hex = binascii.hexlify(os.urandom(bits)).decode('utf8')
            priv_int = int(priv_hex, 16)
            # une clé privée de bitcoin est de l'ordre 2^256 bit = 32 bytes
            if 0 < priv_int < self.N:
                return priv_hex

    # pylint: disable=C0103
    def priv_toWIF(self, key='', prefix='80'):
        '''Générer un WIF depuis un seed'''
        # remplacer le premier byte par le prefix
        # enlever le char "L" et ajouter des 0 à gauche pour assurer la longueur
        # https://www.tutorialspoint.com/python/string_zfill.htm
        step1 = prefix + hex(int(key, 16))[2:].strip('L').zfill(64)
        # double hash sha256
        step2 = hashlib.sha256(binascii.unhexlify(step1)).hexdigest()
        step3 = hashlib.sha256(binascii.unhexlify(step2)).hexdigest()
        # step1 + 8 bits de step3 => convertir en entier
        step4 = int(step1 + step3[:8], 16)
        # convertir l'entier de ste4 en base58
        return self.base58.encode(step4)

    def check_wif(self, wif='', privkey=''):
        '''Valider un WIF généré'''
        # décoder le WIF et le convertir en hexadécimal
        b58 = self.base58.decode(wif).hex()
        # enlever les 2 premiers bits et les 8 derniers bits
        # et comparer avec la clé privée
        assert b58[2:-8].upper() == privkey.upper()

    def wif_to_priv(self, wif=''):
        '''Avoir un seed depuis le WIF'''
        # décoder le WIF et le convertir en hexadécimal
        # enlever les 2 premiers bits et les 8 derniers bits
        return self.base58.decode(wif).hex()[2:-8]

    # pylint: disable=R0201
    def priv_to_public(self, privkey='', compressed=False):
        '''Avoir une clé publique depuis un seed'''
        # voir ce lien: https://en.bitcoin.it/wiki/Protocol_documentation#Addresses
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privkey), curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        # Les prefixes: https://en.bitcoin.it/wiki/List_of_address_prefixes
        prefix = '04' if not compressed else ('03' if vk.pubkey.point.y() % 2 == 1 else '02')
        return prefix + binascii.hexlify(vk.to_string()).decode()

    def ripemd160(self, var):
        '''Fonction de hash ripemd160'''
        rmd = hashlib.new('ripemd160')
        rmd.update(var)
        return rmd

    def make_pub_address(self, pubkey, prefix='00'):
        '''Créer une addresse bitcoin depuis une clé publique'''
        # appliquer ripemd160 sur la hash sha256 du byte array du clé publique
        hash160 = self.ripemd160(hashlib.sha256(binascii.unhexlify(pubkey)).digest()).digest()
        # ajouter le prefix en byte au byte du hash160
        post_pub_addr = binascii.unhexlify(bytes(prefix.encode())) + hash160
        # double hash sha256 et extraire les 4 derniers bits => checksum
        checksum = hashlib.sha256(hashlib.sha256(post_pub_addr).digest()).digest()[:4]
        # encoder en base58
        return self.base58.encode(post_pub_addr + checksum)
