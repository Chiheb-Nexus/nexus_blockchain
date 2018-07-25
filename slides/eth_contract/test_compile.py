# Tester la compilation d'un Smart contract
# Author: Chiheb Nexus - 2018
# License: GPLv3
#
"""Tester la compilation du Smart Contract"""

from compile_contract import CompileContract

PATH_FILE = 'contract.sol'  # Le nom du fichier
CONTRACT_NAME = 'Greeter'  # Le nom du contract
CONTRACT = CompileContract(path_file=PATH_FILE, contract_name=CONTRACT_NAME)
CONTRACT.compile(verbose=True)
