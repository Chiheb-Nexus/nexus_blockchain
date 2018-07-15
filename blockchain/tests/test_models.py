#
# Test blockchain models
#
#

import os
from datetime import datetime
from web3.auto import w3
from django.test import TestCase
from django.core.exceptions import ValidationError
from blockchain.models import (
    BlockStructureDB,
    TransactionDB,
    Address
)


class TestBlockStructureDB(TestCase):
    def setUp(self):
        block = BlockStructureDB.objects.create(
            height=0,
            timestamp=datetime.now().timestamp(),
            data='Genesis Block!',
            block_hash='0x00000000FF',
            merkle='0x0000FF'
        )
        first = BlockStructureDB.objects.create(
            timestamp=datetime.now().timestamp(),
            data='0x0',
            block_hash='0x00FF',
            merkle='0x0FFF',
            previous_hash=block
        )
        second = BlockStructureDB.objects.create(
            timestamp=datetime.now().timestamp(),
            previous_hash=first
        )

    def test_genesis(self):
        '''Test only Genesis Block'''
        block = BlockStructureDB.objects.first()
        self.assertEqual(block.height, 0)
        self.assertEqual(block.data, 'Genesis Block!')
        self.assertEqual(block.block_hash, '0x00000000FF')
        self.assertEqual(block.merkle, '0x0000FF')
        self.assertIsNotNone(block.timestamp)
        self.assertIsNone(block.previous_hash)

    def test_first_block(self):
        '''Test the first block after genesis'''
        block = BlockStructureDB.objects.get(block_hash='0x00FF')
        genesis = BlockStructureDB.objects.first()
        self.assertEqual(block.height, 1)
        self.assertEqual(block.data, '0x0')
        self.assertEqual(block.block_hash, '0x00FF')
        self.assertEqual(block.previous_hash.block_hash, genesis.block_hash)
        self.assertEqual(block.merkle, '0x0FFF')
        self.assertIsNotNone(block.timestamp)

    def test_next_block(self):
        '''Test a random block'''
        block = BlockStructureDB.objects.last()
        self.assertEqual(block.data, '0x0')
        self.assertEqual(block.height, 2)
        self.assertIsNotNone(block.block_hash)
        self.assertIsNone(block.merkle)


class TestAddress(TestCase):
    def setUp(self):
        self.address1 = '0x4c6AfD202389c720e9C2550B6022dF26321A94FC'
        self.address2 = self.address1.lower()
        self.address3 = '0x4c6AfD202389c720e9C2550B6022dF26321A94F'

    def test_address(self):
        '''Test if the given address is a valid Ethereum address'''
        # Pass
        try:
            addr1 = Address()
            addr1.address = self.address1
            addr1.balance = 10
            addr1.full_clean()
            addr1.save()
        except ValidationError as e:
            # We'll not go to this section
            self.assertIsNone(e)

        # Pass
        try:
            addr2 = Address()
            addr2.address = self.address2
            addr2.balance = 10
            addr2.full_clean()
            addr2.save()
        except ValidationError as e:
            # We'll not go to this section
            self.assertIsNone(e)

        # Fail
        try:
            addr3 = Address()
            addr3.address = self.address3
            addr3.balance = 10
            addr3.full_clean()
            addr3.save()
        except ValidationError as e:
            # Silence the error
            self.assertIsNotNone(e)


class TestTransactionDB(TestCase):
    def generate_account(self):
        '''Generate random private & public addresses'''
        account = w3.eth.account.create(os.urandom(64))
        return account.address, account.privateKey

    def setUp(self):
        self.address1, self.priv1 = self.generate_account()
        self.address2, self.priv2 = self.generate_account()
        sender = Address.objects.create(address=self.address1, balance=20)
        reciever = Address.objects.create(address=self.address2)
        # first tx
        tx = TransactionDB.objects.create(
            sender=sender,
            reciever=reciever,
            amount=10,
            timestamp=datetime.now().timestamp(),
            data="tx sent!"
        )
        # more tx with a valid block
        block = BlockStructureDB.objects.create(
            height=1,
            timestamp=datetime.now().timestamp(),
            data='Block 1',
            block_hash='0x00000000FF',
        )
        tx2 = TransactionDB.objects.create(
            sender=sender,
            reciever=reciever,
            amount=3,
            timestamp=datetime.now().timestamp(),
            data="tx sent!",
            block=block
        )
        tx3 = TransactionDB.objects.create(
            sender=sender,
            reciever=reciever,
            amount=1,
            timestamp=datetime.now().timestamp(),
            data="tx sent!",
            block=block
        )

    def test_valid_tx(self):
        '''Check if Transaction is well created'''
        tx = TransactionDB.objects.first()
        self.assertEqual(tx.sender.address, self.address1)
        self.assertEqual(tx.reciever.address, self.address2)
        self.assertIsNotNone(tx.timestamp)
        self.assertEqual(tx.data, 'tx sent!')
        self.assertIsNotNone(tx.block)
        self.assertEqual(tx.confirmation, 0)
        self.assertEqual(tx.fees, 0)

    def test_valid_tx_block(self):
        '''Check if a transaction can be added with a valid block'''
        tx = TransactionDB.objects.first()
        # Save the block to generate a merkle root
        tx.block.save()
        self.assertEqual(tx.sender.address, self.address1)
        self.assertIsNotNone(tx.block.merkle)
