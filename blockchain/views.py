#
# https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
# https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d
#

import re
from django.shortcuts import render
from django.urls import reverse
from blockchain.utils.block import BlockStructure
from blockchain import models
from django.views import View


class GenesisBlock(View):
    template = 'blocks.html'

    def get(self, request, height, *args, **kwargs):
        
        return render(request, self.template, {'block_var': reverse('api:block', args=[height],)})


