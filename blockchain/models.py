#
# models
#
#
"""Blockchain APP models"""

import hashlib
import struct
import random
from binascii import hexlify
from os import urandom
from functools import reduce
from datetime import datetime
from web3.auto import w3
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from blockchain.utils.block import BlockStructure


class BlockStructureDB(models.Model):
    '''BlockStructrueDB model'''
    height = models.AutoField(
        primary_key=True,
        verbose_name='Height',
        blank=False, null=False
    )
    timestamp = models.FloatField(
        unique=True,
        verbose_name='Timestamp',
        blank=False, null=False
    )
    data = models.TextField(
        verbose_name='Data',
        default='0x0'
    )
    previous_hash = models.ForeignKey(
        'self',
        to_field='height',
        verbose_name='Previous Hash',
        related_name='PreviousHash',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    block_hash = models.CharField(
        max_length=250,
        verbose_name='Block Hash',
        blank=True, null=True
    )
    merkle = models.CharField(
        max_length=250,
        verbose_name='Merkle Root',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.block_hash

    class Meta:
        verbose_name = 'Block Structure'
        verbose_name_plural = 'Blocks Structure'


def _merkle_root(iterable):
    '''Basic implementation of merkle root'''

    merkle = ''
    sha256 = hashlib.sha256()
    if iterable.count() >= 2:
        merkle = reduce(lambda x, y: hashlib.sha256(
            (x if isinstance(x, str) else x.tx_hash + y.tx_hash).encode())
            .hexdigest(),  # pylint: disable=C0330
            iterable  # pylint: disable=C0330
        )   # pylint: disable=C0330
    elif iterable.count() == 1:
        sha256.update(iterable[0].tx_hash.encode())
        merkle = sha256.hexdigest()
    # We should never go to this section !
    # There will be always at least one transaction
    # In every block !!!
    # Hope so ^_(o_0)_^ !!
    # else:
    #    sha256.update(''.encode())
    #    merkle = sha256.hexdigest()
    return merkle


@receiver(pre_save, sender=BlockStructureDB)
def add_hash(sender, instance, *args, **kwargs):  # pylint: disable=W0613
    '''Add hash after saving bloc'''
    if not instance.block_hash:
        block = BlockStructure(
            index=instance.height,
            previous_hash=instance.previous_hash,
            data=instance.data,
            timestamp=instance.timestamp
        )
        instance.block_hash = block.hash


@receiver(post_save, sender=BlockStructureDB)
def add_merkle_root(
        sender,
        instance,
        *args,
        **kwargs):  # pylint: disable=W0613
    '''Add merkle root to a block'''
    block_tx = BlockStructureDB.objects.filter(pk=instance.pk).first()
    if not instance.merkle and block_tx:
        if block_tx:
            transactions = block_tx.get_block.all()
            _merkle = _merkle_root(transactions)
            if _merkle:
                instance.merkle = _merkle
        else:
            print('Problem!', instance, instance.pk, block_tx)

    if instance.height == 0 and not instance.merkle:
        instance.merkle = hashlib.sha256(''.encode()).hexdigest()
        instance.save()


def validate_address(addr):
    '''Validate Ethereum address'''
    if not w3.isAddress(addr):
        raise ValidationError(
            '{} is not a valid Ethereum address'.format(addr)
        )


class Address(models.Model):
    '''Address model'''
    address = models.CharField(
        max_length=250,
        verbose_name='Address',
        validators=[validate_address]
    )
    balance = models.FloatField(
        verbose_name='Balance',
        default=0.0,
    )

    def clean_address(self):
        '''Validate an address before saving'''
        if not w3.isAddress(self.address):
            raise ValidationError(
                '{} is not a valid Ethereum address'.format(self.address)
            )

    def __str__(self):
        return self.address


def _create_hash(seed_length=64):
    sha256 = hashlib.sha256()
    seed = hexlify(
        urandom(seed_length) + struct.pack('f', datetime.now().timestamp())
    )
    sha256.update(seed)
    return sha256.hexdigest()


class TransactionDB(models.Model):
    '''TransactionDB model'''
    tx_hash = models.CharField(
        max_length=64,
        verbose_name='Tx Hash',
        primary_key=True,
        default=_create_hash,
        blank=False,
        null=False
    )
    sender = models.ForeignKey(
        Address,
        verbose_name='From',
        related_name='Sender',
        on_delete=models.DO_NOTHING
    )
    reciever = models.ForeignKey(
        Address,
        verbose_name='To',
        related_name='To',
        on_delete=models.DO_NOTHING
    )
    amount = models.FloatField(
        verbose_name='Amount',
        default=0
    )
    data = models.CharField(
        max_length=250,
        verbose_name='Data',
        null=True,
        blank=True
    )
    timestamp = models.FloatField(
        verbose_name='Timestamp',
        null=False,
        blank=False
    )
    block = models.ForeignKey(
        BlockStructureDB,
        verbose_name='Block',
        null=True,
        blank=True,
        related_name='get_block',
        on_delete=models.CASCADE
    )
    confirmation = models.IntegerField(
        verbose_name='Confirmation',
        default=0
    )
    fees = models.FloatField(
        verbose_name='Fees',
        default=0,
        validators=[MinValueValidator(0.0)]
    )

    def __str__(self):
        return self.tx_hash

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions Structure'
        ordering = ('-timestamp',)


class ProofOfNexus(models.Model):
    '''ProofOfNexus model'''
    nexus_hash = models.CharField(
        max_length=250,
        verbose_name='Nexus Hash',
        blank=True,
        null=True
    )
    timestamp = models.FloatField(
        verbose_name='Timestamp',
        blank=True,
        null=True
    )
    nonce = models.IntegerField(
        verbose_name='Nonce',
        blank=True,
        null=True
    )
    nonce_range = models.CharField(
        max_length=250,
        verbose_name='Nonce range',
        blank=True,
        null=True
    )
    random_chr = models.CharField(
        max_length=250,
        verbose_name='Random Character',
        blank=True, null=True
    )
    resolved = models.BooleanField(
        verbose_name='Resolved',
        default=False
    )

    def __str__(self):
        return self.nexus_hash

    class Meta:
        verbose_name = 'Proof of Nexus'
        verbose_name_plural = 'Proofs of Nexus'


def get_random_range():
    '''Get random ranges'''
    index, last = random.sample(range(1, 100), 2)
    if index > last:
        index, last = last, index

    return index, last, 'range({0}, {1})'.format(index, last)


@receiver(post_save, sender=ProofOfNexus)
def get_work(
        sender,
        instance,
        created,
        *args,
        **kwargs):   # pylint: disable=W0613
    '''Get work from valid ranges'''
    if created and not instance.nexus_hash:
        index, last, range_str = get_random_range()
        nonce = random.randint(index, last)
        timestamp = datetime.now().timestamp()
        random_chr = chr(random.randint(97, 122))

        sha256 = hashlib.sha256()
        data = '{0}{1}{2}'.format(random_chr, timestamp, nonce)
        sha256.update(data.encode())
        _hash = sha256.hexdigest()

        instance.nexus_hash = _hash
        instance.timestamp = timestamp
        instance.nonce = nonce
        instance.nonce_range = range_str
        instance.random_chr = random_chr
        instance.save()
