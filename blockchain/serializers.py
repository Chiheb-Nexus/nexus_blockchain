from rest_framework import serializers
from blockchain import models


class AddressAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ('address', )


class SubAddressAPISerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.address

    class Meta:
        model = models.Address
        fields = ('address', )


class SubGetBlockAPISerializer(serializers.ModelSerializer):
    '''Recursive serializer used to get previous_hash'''

    def to_representation(self, value):
        # value is BlockStructureDB
        # return only it's block_hash
        return value.block_hash

    class Meta:
        model = models.BlockStructureDB
        fields = ('block_hash',)


class TransactionAPISerializer(serializers.ModelSerializer):
    sender = SubAddressAPISerializer(many=False)
    reciever = SubAddressAPISerializer(many=False)
    block = SubGetBlockAPISerializer(many=False)

    class Meta:
        model = models.TransactionDB
        fields = '__all__'


class GetBlockAPISerializer(serializers.ModelSerializer):
    transactions = TransactionAPISerializer(many=True, source='get_block')
    previous_hash = SubGetBlockAPISerializer(many=False)

    # Debug
    # def get_fields(self):
    #     fields = super(GetBlockAPISerializer, self).get_fields()
    #     print(dir(fields['previous_hash']))
    #     print(fields['previous_hash'].__dict__)
    #     return fields

    class Meta:
        model = models.BlockStructureDB
        fields = '__all__'


class ProofOfNexusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProofOfNexus
        fields = (
            'nexus_hash',
            'timestamp',
            'nonce_range',
            'random_chr',
            'resolved'
        )


class TransactionsAPI(serializers.ModelSerializer):
    class Meta:
        model = models.TransactionDB
        fields = '__all__'


class AddressInfoAPISerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = models.Address
        fields = ('address', 'balance', 'transactions')

    def get_transactions(self, obj):
        _sent = obj.Sender.all()
        _recieved = obj.To.all()
        # join two querysets using | operator then order by timestamp
        return TransactionAPISerializer(
            (_sent | _recieved).order_by('-timestamp'),
            many=True).data


class GetLastBlocks(serializers.Serializer):
    '''Custom serializer for a list of values'''
    height = serializers.IntegerField()
    block_hash = serializers.CharField(max_length=64)
    timestamp = serializers.FloatField()
