#
# https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
# https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d
#

from django.shortcuts import render
from blockchain.utils.block import BlockStructure
from blockchain import models
from django.views import View


class GenesisBlock(View):
    template = 'genesis_block.html'

    def get(self, request, *args, **kwargs):
        genesis = models.BlockStructureDB.objects.first()
        if not genesis:
            block = BlockStructure(0, '0x0')
            print('block: ', block)
            genesis = models.BlockStructureDB(
                        height=block.index,
                        timestamp=float(block.timestamp),
                        block_hash=block.hash,
                        data='Genesis Block!')
            genesis.save()
        return render(request, self.template, {'block': genesis.block_hash})


