# Tester la compilation d'un Smart contract
# Author: Chiheb Nexus - 2018
# License: GPLv3
#
"""Tester le démploiement du Smart Contract"""

from keystore import ADDRESS, PRIVATE_KEY, PROVIDER
from interact_contract import InteractWithContract


COMPILED_CONTRACT_SOURCE = 'compiled_contract'
INSTANCE = InteractWithContract(
    compiled_sol_path=COMPILED_CONTRACT_SOURCE,
    public_key=ADDRESS,
    private_key=PRIVATE_KEY,
    provider=PROVIDER
)
# déploiement du Smart Contract
TX_HASH = INSTANCE.deploy(verbose=True)
# Attendre au moins une confirmation pour avoir l'adresse du Smart contract
CONTRACT_ADDRESS = INSTANCE.wait_for_receipt(
    TX_HASH,
    contract=True,
    verbose=True
)
