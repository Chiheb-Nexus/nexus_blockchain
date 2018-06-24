#
# routes/urls
#
#

from django.urls import path, include
from blockchain import views, api_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'block[/]?([0-9]+)?', api_views.GetBlockAPI, base_name='block')
router.register(r'genesis', api_views.GenesisBlockAPI, base_name='genesis')
router.register(r'get-raw-transaction', api_views.GetRawTransaction, base_name='raw_tx')
router.register(r'mempool', api_views.MemPool, base_name='mempool')
router.register(r'proof-of-nexus', api_views.ProofOfNexusAPI, base_name='proof_of_nexus')

urlpatterns = [
    path('api/', include(router.urls)),
    path('genesis-block', views.GenesisBlock.as_view(), name='genesis_block')
]