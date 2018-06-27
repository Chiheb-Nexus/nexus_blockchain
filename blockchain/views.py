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


class BlockInfo(View):
    template = 'blocks.html'

    def get(self, request, height, *args, **kwargs):
        
        return render(request, self.template, {'base_url': reverse('api:block', args=[height],)})

class TransactionInfo(View):
    template = 'transaction.html'

    def get(self, request, tx, *args, **kwargs):
        return render(request, self.template, {'base_url': reverse('api:transaction', args=[tx],)})

class AddressInfo(View):
    template = 'address.html'

    def get(self, request, address, *args, **kwargs):
        return render(request, self.template, {'base_url': reverse('api:address', args=[address.lower()],)})


