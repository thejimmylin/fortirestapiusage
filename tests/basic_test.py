import unittest
from urllib.parse import quote
from base import FortiAPIClient


"""
This basic assumes that there is no objects built in /api/v2/cmdb/firewall/address.
"""

CREDENTIALS = {
    'host': '150.117.123.248',
    'users': {
        'admin': {
            'username': 'admin',
            'password': '4fcb3244-e5d2-449c-a49d-7b6fa32bfa7f'
        },
        'readonlyadmin': {
            'username': 'readonlyadmin',
            'password': 'readonlyadmin'
        }
    }
}


class TestFortiAPIClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = FortiAPIClient(CREDENTIALS['host'])
        cls.client.login(
            username=CREDENTIALS['users']['admin']['username'],
            password=CREDENTIALS['users']['admin']['password']
        )

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    def test_get(self):
        r = self.client.get(
            path='/api/v2/cmdb/firewall/address',
            params={'format': 'name|subnet'}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['status'], 'success')

    def test_post(self):
        r = self.client.post(
            path='/api/v2/cmdb/firewall/address',
            json={
                'name': 'address 10.210.201.168/32',
                'type': 'ipmask',
                'subnet': '10.210.201.168 255.255.255.255',
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['status'], 'success')

    def test_put(self):
        r = self.client.put(
            path='/api/v2/cmdb/firewall/address' + '/' + quote('address 10.210.201.168/32', safe=''),
            json={
                'name': 'address__10.210.201.168/32',
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['status'], 'success')

    def test_data_consistency(self):
        r = self.client.get(
            path='/api/v2/cmdb/firewall/address' + '/' + quote('address__10.210.201.168/32', safe=''),
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['status'], 'success')
        self.assertEqual(r.json()['results'][0]['name'], 'address__10.210.201.168/32')
        self.assertEqual(r.json()['results'][0]['type'], 'ipmask')
        self.assertEqual(r.json()['results'][0]['subnet'], '10.210.201.168 255.255.255.255')

    def test_delete(self):
        r = self.client.delete(
            path='/api/v2/cmdb/firewall/address' + '/' + quote('address__10.210.201.168/32', safe=''),
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['status'], 'success')

    @classmethod
    def tearDownClass(cls):
        cls.client.close()


if __name__ == '__main__':
    unittest.main()
