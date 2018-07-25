# Tester la compilation d'un Smart contract
# Author: Chiheb Nexus - 2018
# License: GPLv3
#
"""Tester la compilation d'un Smart Contract"""

import json
from interact_contract import InteractWithContract

# inscrivez-vous au site de infura.io
# et avoir une clé
PROVIDER = 'https://ropsten.infura.io/YOUR_INFURA_KEY'
# adresse publique ethereum
PUB = 'YOUR_PUBLIC_ADDRESS'
# la clé privée de l'adresse publique
KEY = 'YOUR_PRIVATE_ADDRESS'
COMPILED_CONTRACT_SOURCE = 'compiled_contract'
INSTANCE = InteractWithContract(
    compiled_sol_path=COMPILED_CONTRACT_SOURCE,
    public_key=PUB,
    private_key=KEY,
    provider=PROVIDER
)

# ABI du contract compilé
with open(COMPILED_CONTRACT_SOURCE, 'r') as f_data:
    CONTRACT_NAME = '<stdin>:{0}'.format('Greeter')
    ABI = json.loads(f_data.read())['abi']

# adresse du contract après déploiement
CONTRACT_ADDRESS = '0x47C252818FA567d8AE9F06bDAfbfA5987072E64B'
INSTANCE.interact(
    contract_address=CONTRACT_ADDRESS,
    abi=ABI,
    new_msg='Chiheb Nexus'
)
