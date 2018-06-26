#
# Django Rest APIs
#

import json
from datetime import datetime
from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route
from web3.auto import w3
from eth_account.messages import defunct_hash_message
from blockchain import serializers
from blockchain import models
from blockchain.utils.block import BlockStructure
from django.db.models import F


def _create_reward_tx(timestamp, data, reciever_addr, amount,
                        sender_addr='0x0000000000000000000000000000000000000000'):
    last_block = models.BlockStructureDB.objects.last()
    if last_block:
        new_block = models.BlockStructureDB.objects.create(
                        previous_hash=last_block,
                        timestamp=timestamp,
                        data=data
        )
        new_block.save()
    else:
        raise Exception('Must at least be one valid block which is Genesis Block!')

    sender, created = models.Address.objects.get_or_create(
                address=sender_addr.lower()
    )
    reciever, created = models.Address.objects.get_or_create(
                address=reciever_addr.lower()
    )
    reciever.balance += amount
    reciever.save()
    reward = models.TransactionDB.objects.create(
                sender=sender,
                reciever=reciever,
                amount=amount,
                data='New mined coins',
                block=new_block,
                confirmation=0,
                timestamp=timestamp
    )
    models.TransactionDB.objects.filter(
                confirmation=0
    ).update(block=new_block, confirmation=F('confirmation')+1)
    new_block.save()

    return new_block

class GenesisBlockAPI(viewsets.ViewSet):

    def list(self, *args, **kwargs):
        genesis = models.BlockStructureDB.objects.first()
        if not genesis:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'data': []})
        serialized = serializers.GetBlockAPISerializer(genesis)
        return Response({'status': status.HTTP_200_OK, 'data': serialized.data})

    def create(self, request, *args, **kwargs):
        genesis = models.BlockStructureDB.objects.first()
        if not genesis:
            block = BlockStructure(0, '0x0')
            genesis = models.BlockStructureDB.objects.create(
                        height=block.index,
                        timestamp=float(block.timestamp),
                        block_hash=block.hash,
                        data='Genesis Block!')
            #genesis.save()

            new_block = _create_reward_tx(
                reciever_addr=request.data.get('address'),
                data=request.data.get('msg'),
                timestamp=datetime.now().timestamp(),
                amount=25
            )
            #if not new_block.merkle:
            new_block.save()
            serialized = serializers.GetBlockAPISerializer(genesis)
            return Response(serialized.data)

        serialized = serializers.GetBlockAPISerializer(genesis)
        return Response(serialized.data)
        
        

class GetBlockAPI(viewsets.ViewSet):
        
    def list(self, request, *args, **kwargs):
        height = self.kwargs.get('height')
        query = None

        if height and all(k.isdigit() == True for k in height):
            block_height = int(height)
            query = models.BlockStructureDB.objects.filter(
                height=block_height
            ).first()
        elif height.isalnum():
            query = models.BlockStructureDB.objects.filter(
                block_hash = height
            ).first()
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'msg': 'Invalid block number or hash'
            })
        if not query:
            return Response({
                'msg': 'Not found',
                'status': status.HTTP_404_NOT_FOUND
            })
        serialized = serializers.GetBlockAPISerializer(query)
        return Response({'data': serialized.data, 'status': status.HTTP_200_OK})


def check_signature(data, debug=False):
    msg = '{0}-{1}-{2}-{3}-{4}-{5}'.format(
        data.get('from'),
        data.get('to'),
        data.get('amount'),
        data.get('timestamp'),
        data.get('fees'),
        data.get('data')
    )
    msg_hash = defunct_hash_message(text=msg)
    pub_key = w3.eth.account.recoverHash(
        msg_hash, 
        signature=data.get('signature')
    )
    
    if debug:
        print('POST: {0} | Check: {1}'.format(data.get('from'), pub_key),
            pub_key == data.get('from') 
        )

    if data.get('from') == pub_key:
        return True 
    return False

def check_balance(data, sender):
    _from = data.get('from')
    amount = data.get('amount')
    if not amount > 0:
        return False, 'Amount must be positive'
    if not sender.balance:
        return False, 'Low balance'

    if not (sender.balance >= amount):
        return False, 'Amount to send is greater than actual balance'

    return True, False



class GetRawTransaction(viewsets.ViewSet):
    '''Using CRUD routes'''

    def create(self, request, *args, **kwargs):
        resp = {}            
        if check_signature(request.data):
            resp['signature'] = True
            sender, created = models.Address.objects.get_or_create(
                address=request.data.get('from').lower()
            )
            reciever, created = models.Address.objects.get_or_create(
                address=request.data.get('to').lower()
            )

            resp_balance, err = check_balance(request.data, sender)
            if not resp_balance:
                resp['signature'] = False
                resp['tx_hash'] = None
                resp['status'] = status.HTTP_400_BAD_REQUEST
                resp['msg'] = err
                return Response(resp)
                
            sender.balance -= request.data.get('amount')
            sender.save()
            reciever.balance += request.data.get('amount')
            reciever.save()
            transaction = models.TransactionDB.objects.create(
                sender=sender,
                reciever=reciever,
                amount=request.data.get('amount'),
                data=request.data.get('data'),
                timestamp=request.data.get('timestamp'),
                fees=request.data.get('fees')
            )

            resp['tx_hash'] = transaction.tx_hash
            resp['status'] = status.HTTP_200_OK
        else:
            resp['signature'] = False
            resp['tx_hash'] = None
            resp['status'] = status.HTTP_400_BAD_REQUEST
            resp['msg'] = 'Failed signature'

        return Response(resp)


class MemPool(viewsets.ModelViewSet):
    serializer_class = serializers.TransactionAPISerializer
    queryset =  models.TransactionDB.objects.filter(confirmation=0)
    http_method_names = ['get', 'head']

    def list(self, request, *args, **kwargs):
        response = super(MemPool, self).list(request)
        return Response({'status': status.HTTP_200_OK, 'data': response.data})



class ProofOfNexusAPI(viewsets.ViewSet):
    serializer_class = serializers.ProofOfNexusSerializer

    def list(self, request, *args, **kwargs):
        query = models.ProofOfNexus.objects.filter(resolved=False).first()
        if not query:
            query = models.ProofOfNexus.objects.create()

        serialized = self.serializer_class(query)
        return Response({'status': status.HTTP_200_OK, 'data': serialized.data})

    def create(self, request, *args, **kwargs):
        query = models.ProofOfNexus.objects.filter(resolved=False).first()
        if query.nonce == request.data.get('nonce'):
            new_block = _create_reward_tx(
                reciever_addr=request.data.get('address'),
                data=request.data.get('msg'),
                timestamp=datetime.now().timestamp(),
                amount=25
            )
            new_block.save()
            query.resolved = True 
            query.save()
            return Response({'status': status.HTTP_200_OK, 'data': new_block.block_hash})

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': []})
