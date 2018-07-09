#
# Django Rest APIs
#
'''Explorer REST API'''

from datetime import datetime
from django.db.models import F
from rest_framework import viewsets, status
# If you want to render the response into a JSON format only
# from rest_framework import renderers
from rest_framework.response import Response
from web3.auto import w3
from eth_account.messages import defunct_hash_message
from blockchain import serializers, models
from blockchain.utils.block import BlockStructure


def _create_reward_tx(
        timestamp,
        data,
        reciever_addr,
        amount,
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
        raise Exception(
            'Must at least be one valid block'
            'which is Genesis Block!'
        )

    sender, _ = models.Address.objects.get_or_create(
        address=sender_addr.lower())
    reciever, _ = models.Address.objects.get_or_create(
        address=reciever_addr.lower())
    reciever.balance += amount
    reciever.save()
    _ = models.TransactionDB.objects.create(
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
    ).update(block=new_block, confirmation=F('confirmation') + 1)
    new_block.save()

    return new_block


class GenesisBlockAPI(viewsets.ViewSet):
    '''Get Genesis block is exists else create new one'''

    def list(self, *args, **kwargs):
        '''Get method returns Genesis block data'''

        genesis = models.BlockStructureDB.objects.first()
        if not genesis:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'data': []
            })
        serialized = serializers.GetBlockAPISerializer(genesis)
        return Response({
            'status': status.HTTP_200_OK,
            'data': serialized.data
        })

    def create(self, request, *args, **kwargs):
        '''Method POST gets Genesis's block data'''

        genesis = models.BlockStructureDB.objects.first()
        if not genesis:
            block = BlockStructure(0, '0x0')
            genesis = models.BlockStructureDB.objects.create(
                height=block.index,
                timestamp=float(block.timestamp),
                block_hash=block.hash,
                data='Genesis Block!'
            )

            new_block = _create_reward_tx(
                reciever_addr=request.data.get('address'),
                data=request.data.get('msg'),
                timestamp=datetime.now().timestamp(),
                amount=25
            )
            new_block.save()
            serialized = serializers.GetBlockAPISerializer(genesis)
            return Response(serialized.data)

        serialized = serializers.GetBlockAPISerializer(genesis)
        return Response(serialized.data)


class GetBlockAPI(viewsets.ViewSet):
    '''Get or create new block from mining process'''

    def list(self, request, *args, **kwargs):
        '''Get block by height or by block hash'''

        height = self.kwargs.get('height')
        query = None

        if height and all(k.isdigit() for k in height):
            block_height = int(height)
            query = models.BlockStructureDB.objects.filter(
                height=block_height
            ).first()
        elif height.isalnum():
            query = models.BlockStructureDB.objects.filter(
                block_hash=height
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
        return Response({
            'data': serialized.data,
            'status': status.HTTP_200_OK
        })


def check_signature(data, debug=False):
    '''Check address and signature'''

    _from = data.get('from')
    _to = data.get('to')
    # Check addresses if they are Eth compatible
    if not w3.isAddress(_from) or not w3.isAddress(_to):
        return False

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
        print('POST: {0} | Check: {1}'.format(
            data.get('from'),
            pub_key),
            pub_key == data.get('from')
        )

    if data.get('from') == pub_key:
        return True

    return False


def check_balance(data, sender):
    '''Check sender balance'''

    fees = data.get('fees')
    amount = data.get('amount')
    if not isinstance(
            fees, (int, float)) or not isinstance(
            amount, (int, float)):
        return False, 'Amount/fees must be integer or float'
    if not amount > 0 or not fees:
        return False, 'Amount/fees must be positive'
    if not sender.balance:
        return False, 'Low balance'

    if not sender.balance >= (amount + fees):
        return False, 'Amount to send is greater than actual balance'

    return True, False


class GetRawTransaction(viewsets.ViewSet):
    '''Get raw transaction using CRUD routes'''

    def create(self, request, *args, **kwargs):
        '''Create new transaction instance'''

        resp = {}
        if check_signature(request.data):
            resp['signature'] = True
            sender, _ = models.Address.objects.get_or_create(
                address=request.data.get('from').lower()
            )
            reciever, _ = models.Address.objects.get_or_create(
                address=request.data.get('to').lower()
            )

            resp_balance, err = check_balance(request.data, sender)
            if not resp_balance:
                resp['signature'] = False
                resp['tx_hash'] = None
                resp['status'] = status.HTTP_400_BAD_REQUEST
                resp['msg'] = err
                return Response(resp)

            amount = request.data.get('amount') + request.data.get('fees')
            sender.balance -= amount
            sender.save()
            reciever.balance += amount
            reciever.save()
            transaction = models.TransactionDB.objects.create(
                sender=sender,
                reciever=reciever,
                amount=amount,
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


class MemPool(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """Return all pending transactions"""

    serializer_class = serializers.TransactionAPISerializer
    queryset = models.TransactionDB.objects.filter(confirmation=0)
    http_method_names = ['get', 'head']
    # If you want to render the response only in JSON format
    # renderer_classes = [renderers.JSONRenderer]

    def list(self, request, *args, **kwargs):
        '''Get response of all pending transactions'''

        response = super(MemPool, self).list(request)
        return Response({
            'status': status.HTTP_200_OK,
            'data': response.data
        })


class ProofOfNexusAPI(viewsets.ViewSet):
    '''Get new job by applying Proof of Nexus'''

    serializer_class = serializers.ProofOfNexusSerializer

    def list(self, request, *args, **kwargs):
        '''GET the first non resolved job'''

        query = models.ProofOfNexus.objects.filter(resolved=False).first()
        if not query:
            query = models.ProofOfNexus.objects.create()

        serialized = self.serializer_class(query)
        return Response({
            'status': status.HTTP_200_OK,
            'data': serialized.data
        })

    def create(self, request, *args, **kwargs):
        '''Create reward and update pending transaction if job resolved'''

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
            return Response({
                'status': status.HTTP_200_OK,
                'data': new_block.block_hash
            })

        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'data': []
        })


class TransactionAPI(viewsets.ViewSet):
    '''Get transactions'''

    serializer_class = serializers.TransactionAPISerializer

    def list(self, request, _tx, *args, **kwargs):
        '''GET transactions'''

        query = models.TransactionDB.objects.filter(tx_hash=_tx).first()
        if not query:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'msg': 'Not found'
            })

        serialized = self.serializer_class(query)
        return Response({
            'status': status.HTTP_200_OK,
            'data': serialized.data
        })


class AddressAPI(viewsets.ViewSet):
    '''Address informations'''

    serializer_class = serializers.AddressInfoAPISerializer

    def list(self, request, address, *args, **kwargs):
        '''GET addresses informations'''

        if not w3.isAddress(address):
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'msg': 'Address not valid'
            })

        query = models.Address.objects.filter(address=address.lower()).first()
        if not query:
            return Response({
                'status': status.HTTP_200_OK,
                'data': {
                    'address': address.lower(),
                    'balance': 0,
                    'transactions': []
                }
            })

        serialized = self.serializer_class(query)
        return Response({
            'status': status.HTTP_200_OK,
            'data': serialized.data
        })


class LastFiveBlocks(viewsets.ViewSet):
    '''Return last 5 blocks'''

    serializer_class = serializers.GetLastBlocks

    def list(self, request, *args, **kwargs):
        '''GET returns last 5 blocks'''

        query = models.BlockStructureDB.objects.all().order_by(
            '-height')[:5].values(
            'height',
            'block_hash',
            'timestamp'
        )
        serialized = self.serializer_class(query, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'data': serialized.data
        })
