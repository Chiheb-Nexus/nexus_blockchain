from django.contrib import admin
from blockchain import models

def formatter(instance):
    if instance:
        return '{0}...{1}'.format(
            str(instance)[:8],
            str(instance)[len(str(instance))-8:]
        )
    else:
        return '-'

@admin.register(models.BlockStructureDB)
class BlocksAdmin(admin.ModelAdmin):
    list_display = ('height', 'timestamp', 'get_previous_hash',
                    'get_block_hash', 'data')

    def get_block_hash(self, instance):
        return formatter(instance.block_hash)
    
    def get_previous_hash(self, instance):
        return formatter(instance.previous_hash)

@admin.register(models.TransactionDB)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_hash', 'to_address', 'from_address', 'amount', 'block_hash',
                    'timestamp', 'confirmation', 'data', 'fees')

    def transaction_hash(self, instance):
        return formatter(instance.tx_hash)

    def block_hash(self, instance):
        return formatter(instance.block)

    def to_address(self, instance):
        return formatter(instance.reciever)

    def from_address(self, instance):
        return formatter(instance.sender)

@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'balance')

@admin.register(models.ProofOfNexus)
class ProofOfNexusAdmin(admin.ModelAdmin):
    list_display = ('hash_target', 'timestamp', 'nonce', 'nonce_range', 'random_chr', 'resolved')

    def hash_target(self, instance):
        return formatter(instance.nexus_hash)

        
                    
