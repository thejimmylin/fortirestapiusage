import unittest
from urllib.parse import quote
from fortirestapiusage.clients import FortiAPIClient


CREDENTIALS = {
    'host': '150.117.123.248',
    'users': {
        'admin': {
            'username': 'admin',
            'password': '4fcb3244-e5d2-449c-a49d-7b6fa32bfa7f'
        },
        'readonlyadmin': {
            'username': 'readonlyadmin',
            'password': 'cb204a81-0a16-46e9-aaca-2a8cc070593b'
        }
    }
}


class FortiAPIClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = FortiAPIClient(CREDENTIALS['host'])
        self.client.login(
            username=CREDENTIALS['users']['admin']['username'],
            password=CREDENTIALS['users']['admin']['password']
        )

    def test_get(self):
        r = self.client.get(
            path='/api/v2/cmdb/firewall/address',
            params={'format': 'name|subnet'}
        )
        self.assertEqual(r.json()['status'], 'success')

    def test_post_delete(self):
        r = self.client.post(
            path='/api/v2/cmdb/firewall/address',
            json={
                'name': 'address__admin__10.65.61.168/32',
                'type': 'ipmask',
                'subnet': '10.65.61.168 255.255.255.255',
            }
        )
        self.assertEqual(r.json()['status'], 'success')
        r = self.client.delete(
            path='/api/v2/cmdb/firewall/address' + '/' + quote('address__admin__10.65.61.168/32', safe=''),
        )
        self.assertEqual(r.json()['status'], 'success')

    def test_post_put_delete(self):
        r = self.client.post(
            path='/api/v2/cmdb/firewall/address',
            json={
                'name': 'address__admin__10.65.61.168/32',
                'type': 'ipmask',
                'subnet': '10.65.61.168 255.255.255.255',
            }
        )
        self.assertEqual(r.json()['status'], 'success')
        r = self.client.put(
            path='/api/v2/cmdb/firewall/address' + '/' + quote('address__admin__10.65.61.168/32', safe=''),
            json={
                'name': 'address__admin__10.65.61.168/32',
            }
        )
        self.assertEqual(r.json()['status'], 'success')
        r = self.client.delete(
            path='/api/v2/cmdb/firewall/address' + '/' + quote('address__admin__10.65.61.168/32', safe=''),
        )
        self.assertEqual(r.json()['status'], 'success')

    def test_login_logout_heavily(self):
        for n in range(49):
            self.client.login(
                username=CREDENTIALS['users']['admin']['username'],
                password=CREDENTIALS['users']['admin']['password']
            )
            self.client.logout()
        r = self.client.login(
            username=CREDENTIALS['users']['admin']['username'],
            password=CREDENTIALS['users']['admin']['password']
        )
        self.assertIsNotNone(r.cookies.get('ccsrftoken'))

    def tearDown(self):
        self.client.close()


if __name__ == '__main__':
    unittest.main()
