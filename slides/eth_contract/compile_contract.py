# Compile contract
# Author: Chiheb Nexus - 2018
# License: GPLv3
#
"""Compilation d'un Smart Contract d'Ethereum"""


import json
from solc import compile_source


class CompileContract:
    '''Compilation d'un Smart contract'''
    def __init__(self, path_file, contract_name):
        self.path_file = path_file
        self.contract_name = contract_name

    def read(self, verbose=False):
        '''Lecture du fichier contenant le code source du Smart Contract'''
        if verbose:
            print('-> Lecture du fichier: {0}'.format(self.path_file))
        with open(self.path_file, 'r') as f_data:
            data = f_data.read()

        print('-> Lecture terminée! du fichier: {0}'.format(self.path_file))
        return data

    def write(self, file_name, data, verbose=False):
        '''Écriture du output de la compilation du Smart contract'''
        if verbose:
            msg = '-> Écriture du contract compilé dans le fichier: {0}'
            print(msg.format(file_name))

        with open(file_name, 'w') as f_data:
            f_data.write(
                json.dumps(
                    data['<stdin>:{0}'.format(self.contract_name)]
                )
            )

        if verbose:
            msg = '-> Écriture terminée avec succès! dans le fichier: {0}'
            print(msg.format(file_name))

    def compile(self, verbose=False):
        '''Compiler le code du Smart Contract'''
        if verbose:
            print('-> Compilation en cours ...')

        compiled_sol = compile_source(self.read(verbose=True))
        self.write('compiled_contract', compiled_sol, verbose=True)

        if verbose:
            print('-> Compilation terminée avec succès!')
