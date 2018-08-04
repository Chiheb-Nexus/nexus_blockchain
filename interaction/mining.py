#
#
#
#

import os
import hashlib
import time
import re 
import requests
import json
import settings_wallet
from utils.fmt_debug import fmt_debug

class Mining:
    def __init__(self):
        self.genesis_url = 'http://127.0.0.1:8000/api/genesis'
        self.get_job_url = 'http://127.0.0.1:8000/api/proof-of-nexus/'
        self.headers = {'content-type': 'application/json'}
        self.miner_name = 'Nexus'
        path = os.path.join(settings_wallet.KEY_STORE_PATH, 'keys')
        with open(path, 'r') as f:
            self.miner_address = json.loads(f.read())['address']
        self.check_genesis()

    def check_genesis(self):
        _data = {
            'address': self.miner_address,
            'msg': 'Block mined by {0}'.format(self.miner_name),
            'miner': self.miner_name
        }
        resp = requests.post(
            self.genesis_url,
            headers=self.headers,
            data=json.dumps(_data)
        )
        if resp.status_code == 200:
            print(resp.text)
        else:
            fmt_debug(WARNING='Cannot create Genesis Block!')
            raise Exception('Initialization of blockchain failed!')
        

    def get_job(self):
        response = requests.get(self.get_job_url, headers=self.headers)
        if response.status_code == 200:
            fmt_debug(INFO='Trying to find new work ...')
            data = json.loads(response.text).get('data')
            if data:
                return data 
            else:
                fmt_debug(WARNING='No work found ...')
                fmt_debug(WARNING='Sleeping 5s ...')
                time.sleep(5)
                return None
                
        else:
            fmt_debug(WARNING="Cannot access: {0}".format(self.get_job_url))
            return None

    def proof_of_nexus(self, data):
        _hash = data.get('nexus_hash')
        timestamp = data.get('timestamp')
        random_chr = data.get('random_chr')
        nonce_range = None
        nonce_range_regex = re.match(
            r'range\((\d+),\s+(\d+)\)', 
            data.get('nonce_range')
        )
        if nonce_range_regex:
            nonce_range = [int(k) for k in nonce_range_regex.groups()]
        else:
            return None, "cannot find nonce_range"

        for k in range(nonce_range[0], nonce_range[1]+1):
            sha256 = hashlib.sha256()
            _data = '{0}{1}{2}'.format(
                random_chr,
                timestamp,
                k
            )
            sha256.update(_data.encode())
            actual_hash = sha256.hexdigest()
            if actual_hash == _hash:
                return k, None

        return None, "cannot validate Proof of Nexus!"
        

    def resolve_work(self):
        data = self.get_job()
        if data:
            fmt_debug(INFO='Trying to find Nonce ...')
            nonce, err = self.proof_of_nexus(data)
            if err:
                fmt_debug(WARNING=err)
                fmt_debug(INFO='Retargeting new work ...')
                time.sleep(5)
                return None 

            fmt_debug(INFO='Working ...')
            time.sleep(5)
            fmt_debug(INFO='Nonce found! : {0}'.format(nonce))
            return nonce

        else:
            fmt_debug(WARNING='Setting new target ... ')
            return None

    def mine(self):
        while True:
            try:
                nonce = self.resolve_work()
                if nonce:
                    _data = {
                        'nonce': nonce,
                        'miner': self.miner_name,
                        'msg': 'Block mined by {0}'.format(self.miner_name),
                        'address': self.miner_address
                    }
                    resp = requests.post(
                        self.get_job_url,
                        headers=self.headers,
                        data=json.dumps(_data))
                    print(resp.text)
            except KeyboardInterrupt:
                user_input = input('\nQuit [q/Q] else Continue: ')
                if user_input in ['q', 'Q']:
                    break


# test
if __name__ == '__main__':
    app = Mining()
    app.mine()
        
