# Déploiement et interaction avec un Smart contract
# Author: Chiheb Nexus - 2018
# License: GPLv3
#
"""Interaction avec un Smart Contract d'Ethereum"""

import json
import time
from web3 import Web3


class InteractWithContract:
    '''Interaction avec un Smart Contract'''
    def __init__(
            self,
            provider,
            compiled_sol_path=None,
            public_key=None,
            private_key=None):
        # Dans cet exemple on va utiliser infura.io comme provider
        # Et la communication avec infura peut se faire en utilisant
        # le protocole HTTP ou WS (Web Socket)
        self.w3_instance = Web3(Web3.HTTPProvider(provider))
        self.compiled = compiled_sol_path
        # ABI et le BIN du output compilé du Smart Contract
        self.contract_abi, self.contract_bin = '', ''
        # L'adresse publique et privée de celui qui va déployé et communiquer
        # avec le Smart Contract
        self.pub, self.priv = public_key, private_key

    def read(self, verbose=False):
        '''Lecture du ouput compilé et extraction de ABI et du BIN'''
        if verbose:
            print('-> Lecture du fichier: {0}'.format(self.compiled))
        with open(self.compiled, 'r') as f_data:
            # Conversion du JSON en Python dict
            data = json.loads(f_data.read())

        if verbose:
            print('-> Lecture terminée du fichier: {0}'.format(self.compiled))

        self.contract_abi = data.get('abi')
        self.contract_bin = data.get('bin')

        if verbose:
            print('-> Extraction du ABI et de BIN faite avec succès!')

    def deploy(self, verbose=False):
        '''Déploiement du Smart Contract'''
        self.read()
        if verbose:
            print('-> Déploiement du Smart Contract ...')

        instance = self.w3_instance.eth.contract(  # pylint: disable=E1101
            abi=self.contract_abi,
            bytecode=self.contract_bin
        )
        if verbose:
            print('-> Préparation de la transaction du déploiement ...')
        # Hacky ... mais fonctionnel :D
        tx_data = instance.constructor().__dict__.get('data_in_transaction')
        # pylint: disable=E1101
        transaction = {
            # Celui qui va envoyer la transaction
            'from': self.pub,
            # Combien d'ethers vont être envoyés durant la transaction
            'value': 0,
            # GAS ... J'essaie de le rendre dynamique ...
            'gas': 2000000,
            # GAS price dynamique
            'gasPrice': self.w3_instance.eth.gasPrice,
            # Le nonce de l'adresse
            'nonce': self.w3_instance.eth.getTransactionCount(self.pub),
            # Les données envoyées durant la transaction
            'data': tx_data
        }
        if verbose:
            print('-> Signer la transaction avec la clé privée...')

        signed = self.w3_instance.eth.account.signTransaction(transaction, self.priv)

        if verbose:
            msg = '-> Envoyer la transaction signée aux noeuds du provider ...'
            print(msg)

        tx_hash = self.w3_instance.eth.sendRawTransaction(signed.rawTransaction)

        if verbose:
            msg = '-> Transaction envoyée avec succès avec ce hash: {0}'
            print(msg.format(tx_hash.hex()))

        # Convertir le ByteArray en hexadécimal
        return tx_hash.hex()

    def wait_for_receipt(self, tx_hash, contract=False, verbose=False):
        '''Attendre au moins une confirmation de la transaction'''
        if verbose:
            msg = (
                '-> Attente de la première confirmation '
                'de la transaction: {0}'
            )
            print(msg.format(tx_hash))
            print('...')
        while True:
            # Avoir les informations de la transaction
            # Y compris l'adresse du Smart Contract
            # pylint: disable=E1101
            tx_receipt = self.w3_instance.eth.getTransactionReceipt(tx_hash)
            if tx_receipt:
                if verbose:
                    print('-> Transaction confirmée!')
                if contract:
                    # Avoir l'adresse du Smart Contract
                    contract_address = tx_receipt.get('contractAddress')
                    if verbose:
                        msg = (
                            "-> Écriture de l'adresse du contract '{0} dans"
                            "le fichier: {1}'"
                        )
                        print(msg.format(contract_address, 'contract_address'))

                    with open('contract_address.py', 'w+') as f_data:
                        f_data.write('"""Contract address"""\n\n')
                        f_data.write("CONTRACT_ADDRESS = '{}'\n".format(str(contract_address)))

                    if verbose:
                        print('-> Écriture terminée avec succès!')

                    return contract_address
                else:
                    return None
            # Attendre 1 seconde puis tester
            # si la transaction est confirmée ou non
            time.sleep(1)

    def interact(self, contract_address, abi, new_msg=''):
        '''Interaction avec le Smart Contract Greeter déployé'''
        # Création d'une instance du Smart Contract Greeter
        greeter = self.w3_instance.eth.contract(  # pylint: disable=E1101
            address=contract_address,
            abi=abi
        )
        # Appel de la fonction greet() dans le Smart Contract déployé Greeter
        msg = greeter.functions.greet().call()
        print('Actual message: ', msg)
        if new_msg:
            # Appel de la fonction setGreeting(string _greeting)
            # en ajoutant un argument
            # Cette fonction modifie l'état d'une variable
            # dans le Smart contract
            # => Faut payer des frais de transaction de cette modification
            # ==> Faut créer une transaction et la signer avec la clé privée
            # de celui qui va faire cette modification dans le Smart contract
            tx_data = greeter.functions.setGreeting(new_msg).buildTransaction({
                # GAS Price dynamique
                # pylint: disable=E1101
                'gasPrice': self.w3_instance.eth.gasPrice,
                # Le nonce de l'adresse
                'nonce': self.w3_instance.eth.getTransactionCount(self.pub),
            })
            # Signer la transaction avec l'adresse privée
            # pylint: disable=E1101
            signed_tx = self.w3_instance.eth.account.signTransaction(
                tx_data,
                self.priv
            )
            # Envoyer la transaction signée aux noeuds du provider
            tx_hash = self.w3_instance.eth.sendRawTransaction(
                signed_tx.rawTransaction
            )
            # Attendre au moins une confirmation
            self.wait_for_receipt(tx_hash.hex())
            # Appel de la fonction greet() dans le Smart Contract
            msg = greeter.functions.greet().call()
            print('New message: ', msg)
