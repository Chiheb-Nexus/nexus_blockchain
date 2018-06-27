#
# Create Transaction
#
#

import requests
from datetime import datetime
import json
from utils.fmt_debug import fmt_debug
from web3.auto import w3
from eth_account.messages import defunct_hash_message

class CreateTransaction:
    def __init__(self, _from, _from_priv, _to, amount, 
                    timestamp, fees=0, data='0x', debug=False):
        if not _from or not isinstance(_from, str):
            raise Exception('Address "from" is not valid')

        if not _from_priv or not isinstance(_from_priv, str):
            raise Exception('Need a valid private key to sign transaction')

        if not _to or not isinstance(_to, str):
            raise Exception('Address "to" is not valid')

        if not isinstance(amount, (int, float)) or amount < 0 :
            raise Exception('Amount is not valid')

        if not isinstance(timestamp, (int, float)):
            raise Exception('Timestamp is not valid')

        if not isinstance(fees, (int, float)) or fees < 0:
            raise Exception('Fees are not valid')
            
        if not isinstance(data, str):
            raise Exception('Data are not valid')

        self.debug = debug
        self._from = _from 
        self._from_priv = _from_priv
        self._to = _to 
        self.amount = amount 
        self.timestamp = timestamp 
        self.fees = fees 
        self.data = data 
        self.headers = {'content-type': 'application/json'}


    def create_signature(self):
        msg = '{0}-{1}-{2}-{3}-{4}-{5}'.format(
            self._from,
            self._to,
            self.amount,
            self.timestamp,
            self.fees,
            self.data
        )
        msg_hash = defunct_hash_message(text=msg)
        signed_msg = w3.eth.account.signHash(msg_hash, private_key=self._from_priv)
        return signed_msg.signature.hex()


    def send_raw_transaction(self):
        tx = json.dumps({
            'from': self._from,
            'to': self._to,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'fees': self.fees,
            'data': self.data,
            'signature': self.create_signature()
        })

        if self.debug:
            fmt_debug(INFO='Sending Transaction:\n{0}'.format(tx))
        
        req = requests.post(
            'http://127.0.0.1:8000/api/get-raw-transaction/', 
            data=tx,
            headers=self.headers
        )

        if req.status_code == 200:
            fmt_debug(INFO='Server response: {0}'.format(
                req.text
            ))
        else:
            fmt_debug(WARNING='Error while sending data to server. Error: {0}'.format(
                req.status_code
            ))

# Test
if __name__ == '__main__':
    
    import os 

    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(DIR_PATH, 'keystore/keys')
    account = ''
    with open(path, 'r') as f:
        account = json.loads(f.read())

    
    a = CreateTransaction(
        _from=account.get('address'), 
        _to='0x0000000000000000000000000000000000000000', 
        debug=True,
        _from_priv=account.get('privkey'), 
        amount=5, 
        timestamp=datetime.now().timestamp(),
        fees=0.0001
    )
    a.send_raw_transaction()

