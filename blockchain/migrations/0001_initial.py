# Generated by Django 2.0.6 on 2018-06-27 19:48

import blockchain.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=250, verbose_name='Address')),
                ('balance', models.FloatField(default=0.0, verbose_name='Balance')),
            ],
        ),
        migrations.CreateModel(
            name='BlockStructureDB',
            fields=[
                ('height', models.AutoField(primary_key=True, serialize=False, verbose_name='Height')),
                ('timestamp', models.FloatField(unique=True, verbose_name='Timestamp')),
                ('data', models.TextField(default='0x0', verbose_name='Data')),
                ('block_hash', models.CharField(blank=True, max_length=250, null=True, verbose_name='Block Hash')),
                ('merkle', models.CharField(blank=True, max_length=250, null=True, verbose_name='Merkle Root')),
                ('previous_hash', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PreviousHash', to='blockchain.BlockStructureDB', verbose_name='Previous Hash')),
            ],
            options={
                'verbose_name_plural': 'Blocks Structure',
                'verbose_name': 'Block Structure',
            },
        ),
        migrations.CreateModel(
            name='ProofOfNexus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nexus_hash', models.CharField(blank=True, max_length=250, null=True, verbose_name='Nexus Hash')),
                ('timestamp', models.FloatField(blank=True, null=True, verbose_name='Timestamp')),
                ('nonce', models.IntegerField(blank=True, null=True, verbose_name='Nonce')),
                ('nonce_range', models.CharField(blank=True, max_length=250, null=True, verbose_name='Nonce range')),
                ('random_chr', models.CharField(blank=True, max_length=250, null=True, verbose_name='Random Character')),
                ('resolved', models.BooleanField(default=False, verbose_name='Resolved')),
            ],
            options={
                'verbose_name_plural': 'Proofs of Nexus',
                'verbose_name': 'Proof of Nexus',
            },
        ),
        migrations.CreateModel(
            name='TransactionDB',
            fields=[
                ('tx_hash', models.CharField(default=blockchain.models._create_hash, max_length=64, primary_key=True, serialize=False, verbose_name='Tx Hash')),
                ('amount', models.FloatField(default=0, verbose_name='Amount')),
                ('data', models.CharField(blank=True, max_length=250, null=True, verbose_name='Data')),
                ('timestamp', models.FloatField(verbose_name='Timestamp')),
                ('confirmation', models.IntegerField(default=0, verbose_name='Confirmation')),
                ('fees', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Fees')),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_block', to='blockchain.BlockStructureDB', verbose_name='Block')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='To', to='blockchain.Address', verbose_name='To')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Sender', to='blockchain.Address', verbose_name='From')),
            ],
            options={
                'ordering': ('-timestamp',),
                'verbose_name_plural': 'Transactions Structure',
                'verbose_name': 'Transaction',
            },
        ),
    ]
