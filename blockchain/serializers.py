from rest_framework import serializers
from blockchain import models

class AddressAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address 
        fields = ('address', 'balance')

class TransactionAPISerializer(serializers.ModelSerializer):
    sender = AddressAPISerializer(many=False)
    reciever = AddressAPISerializer(many=False)
    
    class Meta:
        model = models.TransactionDB
        fields = '__all__'

class GetBlockAPISerializer(serializers.ModelSerializer):
    transactions = TransactionAPISerializer(many=True, source='get_block')

    class Meta:
        model = models.BlockStructureDB
        fields = '__all__'

class ProofOfNexusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProofOfNexus
        fields = ('nexus_hash', 'timestamp', 'nonce_range', 'random_chr', 'resolved')