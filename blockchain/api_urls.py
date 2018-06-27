#
#
#

from django.urls import path, include, re_path
from rest_framework import routers
from blockchain import api_views

router = routers.DefaultRouter()
#router.register(r'block/(?P<height>[0-9a-f-A-F]{,64})', api_views.GetBlockAPI, base_name='block')
router.register(r'genesis', api_views.GenesisBlockAPI, base_name='genesis')
router.register(r'get-raw-transaction', api_views.GetRawTransaction, base_name='raw_tx')
router.register(r'mempool', api_views.MemPool, base_name='mempool')
router.register(r'proof-of-nexus', api_views.ProofOfNexusAPI, base_name='proof_of_nexus')

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    #path('block/<int:height>/', api_views.GetBlockAPI.as_view({
    #    'get': 'list'
    #}), name='blocks'),
    re_path(r'block/(?P<height>[0-9a-fA-F]{,64})', api_views.GetBlockAPI.as_view({
        'get': 'list'
    }), name='block'),
    re_path(r'transaction/(?P<tx>[0-9a-fA-F]{,64})', api_views.TransactionAPI.as_view({
        'get': 'list'
    }), name='transaction'),
    re_path(r'address/(?P<address>0x[0-9a-fA-F]{,64})', api_views.AddressAPI.as_view({
        'get': 'list'
    }), name='address')
]