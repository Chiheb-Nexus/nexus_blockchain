# Tester la compilation d'un Smart contract
# Author: Chiheb Nexus - 2018
# License: GPLv3
#
"""Tester la compilation d'un Smart Contract"""

import json
from keystore import ADDRESS, PRIVATE_KEY, PROVIDER
from contract_address import CONTRACT_ADDRESS
from interact_contract import InteractWithContract

COMPILED_CONTRACT_SOURCE = 'compiled_contract'
INSTANCE = InteractWithContract(
    compiled_sol_path=COMPILED_CONTRACT_SOURCE,
    public_key=ADDRESS,
    private_key=PRIVATE_KEY,
    provider=PROVIDER
)

# ABI du contract compilé
with open(COMPILED_CONTRACT_SOURCE, 'r') as f_data:
    CONTRACT_NAME = '<stdin>:{0}'.format('Greeter')
    ABI = json.loads(f_data.read())['abi']

INSTANCE.interact(
    contract_address=CONTRACT_ADDRESS,
    abi=ABI,
    new_msg='Chiheb Nexus'
)
