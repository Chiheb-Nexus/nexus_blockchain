#
# routes/urls
#
#

from django.urls import path, include, re_path
from blockchain import views, api_views, api_urls

# app_name = 'blockchain'
urlpatterns = [
    path('api/', include('blockchain.api_urls', namespace='api')),
    re_path(
        r'block-info/(?P<height>[0-9a-fA-F]{,64})',
        views.BlockInfo.as_view(),
        name='block_info'),
    re_path(
        r'transaction-info/(?P<tx>[0-9a-fA-F]{,64})',
        views.TransactionInfo.as_view(),
        name='transaction_info'),
    re_path(
        r'address-info/(?P<address>0x[0-9a-fA-F]{,64})',
        views.AddressInfo.as_view(),
        name='address_info'),
    path('search', views.Search.as_view(), name='search'),
    path('', views.Index.as_view(), name='index'),
    path('mempool', views.Mempool.as_view(), name='mempool_view')
]
