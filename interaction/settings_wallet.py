#
# Wallet settings
#

import os

BASE_DIR_WALLET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_STORE_PATH = os.path.join(BASE_DIR_WALLET, 'interaction/keystore')
