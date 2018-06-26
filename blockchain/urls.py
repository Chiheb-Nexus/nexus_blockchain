#
# routes/urls
#
#

from django.urls import path, include, re_path
from blockchain import views, api_views, api_urls

#app_name = 'blockchain'
urlpatterns = [
    path('api/', include('blockchain.api_urls', namespace='api')),
    re_path(r'block-info/(?P<height>[0-9a-f-A-F]{,64})', views.GenesisBlock.as_view(), name='block_info')
]