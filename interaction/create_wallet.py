#
# Create Private & public keys using Ethereum's web3 module
#
#

import os
import json
from utils.fmt_debug import fmt_debug
import settings_wallet
from web3.auto import w3

class CreateAccount:
    def __init__(self, debug=False):
        self.debug = debug
        self.path = os.path.join(settings_wallet.KEY_STORE_PATH, 'keys')
        self.account = w3.eth.account.create(self.get_seed())
        self.write()

    def write(self):
        with open(self.path, 'w+') as f:
            f.write(json.dumps({
                'address': self.account.address,
                'privkey': w3.toHex(self.account.privateKey)
            }, indent=4))

        if self.debug:
            fmt_debug(INFO='Wallet created', PATH=self.path)
    
    def get_seed(seed=64):
        return os.urandom(64)
        

if __name__ == '__main__':
    a = CreateAccount(debug=True)
