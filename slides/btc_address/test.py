# Tester l'implémentation de génération des addresses de bitcoin
# Author: Chiheb Nexus - 2018
# License: GPLv3
# l'exemple introduit par:
# https://en.bitcoin.it/wiki/Wallet_import_format
#   et
# https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
# Aussi penser à valider les résultats avec le site: https://www.bitaddress.org
#
"""Testing the implementation"""

import unittest
from btc_addresses import BTCAddress


class TestBTCAddress(unittest.TestCase):
    '''Test Generated Bitcoin addresses within a predefined addresses'''

    btc_addresses = BTCAddress()
    privkey = '0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D'
    wif_example = "5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"
    addr_example = "1GAehh7TsJAHuUAeKZcXf5CnwuGuGgyX2S"

    def test_wif(self):
        '''Tester le WIF généré avec le WIF de l'exemple'''
        priv = self.btc_addresses.priv_toWIF(self.privkey)
        self.assertEqual(priv, self.wif_example)

    def test_addr(self):
        '''Tester l'adresse générée avec l'adresse de l'exemple'''
        pub = self.btc_addresses.priv_to_public(self.privkey)
        addr = self.btc_addresses.make_pub_address(pub)
        self.assertEqual(addr, self.addr_example)

# Test
if __name__ == '__main__':
    unittest.main()
