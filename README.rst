=================
Nexus Blockchain
=================

Nexus Blockchain is a tiny implementation of the blockchain technology built using
Python, Django, VueJS and an RDBMS database.

Detailed documentation is in the "slides" directory.

Quick start
-----------

1. Add "nexus_blockchain" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'nexus_blockchain',
    ]

2. Include the nexus_blockchain URLconf in your project urls.py like this::

    path('blockchain/', include('nexus_blockchain.urls')),

3. Run `python manage.py migrate` to create models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/blockchain/
