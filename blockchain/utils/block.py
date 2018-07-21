#
# Block structure
#
"""Block Structrue for random block"""

import hashlib
from datetime import datetime


class BlockStructure:
    '''Struct for a random block'''
    def __init__(self, index, previous_hash, timestamp=None, data=None,):
        self.index = index
        if not timestamp:
            self.timestamp = datetime.now().timestamp()
        else:
            self.timestamp = timestamp
        if not data:
            self.data = 0x0
        else:
            self.data = data
        self.previous_hash = previous_hash
        self.hash = self.block_hash()

    def block_hash(self):
        '''Returns block hash'''
        sha256 = hashlib.sha256()
        sha256.update(
            str(self.index).encode('utf8') +
            str(self.timestamp).encode('utf8') +
            str(self.data).encode('utf8') +
            str(self.previous_hash).encode('utf8')
        )
        return sha256.hexdigest()

    def __str__(self):
        return self.hash

    def __dict__(self):
        import json
        return json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous hash': self.previous_hash,
            'hash': self.hash
        })

    def __iter__(self):
        iterable = [('index', self.index), ('timestamp', self.timestamp),
                    ('data', self.data), ('previous hash', self.previous_hash),
                    ('hash', self.hash)]
        for elm in iterable:
            yield elm

# Test:
if __name__ == '__main__':
    APP = BlockStructure(1, 0xefffff)
    print(APP)
    print(dict(APP))
