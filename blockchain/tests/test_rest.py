#
# Test blockchain API
#
#

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestGenesisBlockAPI(APITestCase):
    def test_genesis_block(self):
        url = reverse('api:genesis')
        # Get before creating a genesis block
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], [])
        self.assertEqual(
            response.data['status'],
            status.HTTP_404_NOT_FOUND
        )
        # Create a genesis block then get results
        data = {
            'address': '0x4c6AfD202389c720e9C2550B6022dF26321A94FC',
            'msg': 'Block Test'
        }
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_200_OK)
        self.assertEqual(response_post.data['height'], 0)
        self.assertEqual(response_post.data['data'], 'Genesis Block!')
        self.assertEqual(response_post.data['previous_hash'], None)
        self.assertEqual(response_post.data['transactions'], [])