#
# Main views
#

import re
from web3.auto import w3
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.http import Http404
from blockchain.utils.block import BlockStructure
from blockchain import models


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

class Search(View):
    error_404 = '404_view.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.error_404)
        

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search-input')
        if not search:
            raise Http404('Invalid search argument')

        if w3.isAddress(search):
            return redirect(reverse('address_info', args=[search]))

        if all(k.isdigit() == True for k in search):
            return redirect(reverse('block_info', args=[search]))

        if search.isalnum():
            if models.BlockStructureDB.objects.filter(
                    block_hash=search
                ).exists():
                return redirect(reverse('block_info', args=[search]))
            elif models.TransactionDB.objects.filter(
                    tx_hash=search
                ).exists():
                return redirect(reverse('transaction_info', args=[search]))
            else:
                raise Http404('Invalid search argument')


class Index(View):
    template = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'base_url': reverse('api:last_blocks')})

    


