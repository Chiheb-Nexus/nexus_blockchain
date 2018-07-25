# Tester la compilation d'un Smart contract
# Author: Chiheb Nexus - 2018
# License: GPLv3
#
"""Tester le démploiement du Smart Contract"""

from interact_contract import InteractWithContract

# inscrivez-vous au site de infura.io
# et avoir une clé
PROVIDER = 'https://ropsten.infura.io/YOUR_INFURA_KEY'
# adresse publique ethereum
PUB = 'YOUR_PUBLIC_ADDRESS'
# la clé privée de l'adresse publique
KEY = 'YOUR_PRIVATE_ADDRESS'
# fichier contenant l'ouput de la compilation du Smart contract
COMPILED_CONTRACT_SOURCE = 'compiled_contract'
INSTANCE = InteractWithContract(
    compiled_sol_path=COMPILED_CONTRACT_SOURCE,
    public_key=PUB,
    private_key=KEY,
    provider=PROVIDER
)
# déploiement du Smart Contract
TX_HASH = INSTANCE.deploy(verbose=True)
# Attendre au moins une confirmation pour avoir l'adresse du Smart contract
CONTRACT_INSTANCE = INSTANCE.wait_for_receipt(
    TX_HASH,
    contract=True,
    verbose=True
)
