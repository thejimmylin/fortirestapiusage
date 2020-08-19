import requests
from urllib.parse import urlencode, quote


class FortiAPIClient():

    def __init__(self, host, session=None, is_https=True, timeout=30):
        self._host = host
        self._session = session or requests.session()
        self._is_https = is_https
        self.timeout = timeout

    @property
    def host(self):
        return self._host

    @property
    def session(self):
        return self._session

    @property
    def is_https(self):
        return self._is_https

    @property
    def url_root(self):
        url_root = f'https://{self._host}' if self._is_https else f'http://{self._host}'
        return url_root

    def login(self, username, password, path='/logincheck'):
        url = self.url_root + path
        data = {
            'username': username,
            'secretkey': password,
        }
        encoded_data = urlencode(data)
        response = self._session.post(url=url, data=encoded_data)
        return response

    def logout(self, path='/logout'):
        url = self.url_root + path
        response = self._session.post(url=url)
        return response

    def get(self, path, params={}):
        url = self.url_root + path
        response = self._session.get(
            url=url,
            params=params,
            timeout=self.timeout,
        )
        return response

    def post(self, path, data={}, json=''):
        url = self.url_root + path
        headers = {
            'X-CSRFTOKEN': self._session.cookies['ccsrftoken'][1:-1],
        }
        response = self._session.post(
            url=url,
            headers=headers,
            data=data,
            json=json,
            timeout=self.timeout,
        )
        return response

    def put(self, path, data={}, json=''):
        url = self.url_root + path
        headers = {
            'X-CSRFTOKEN': self._session.cookies['ccsrftoken'][1:-1],
        }
        response = self._session.put(
            url=url,
            headers=headers,
            data=data,
            json=json,
            timeout=self.timeout,
        )
        return response

    def delete(self, path):
        url = self.url_root + path
        headers = {
            'X-CSRFTOKEN': self._session.cookies['ccsrftoken'][1:-1],
        }
        response = self._session.delete(
            url=url,
            headers=headers,
            timeout=self.timeout,
        )
        return response


# Usage
# Login
client = FortiAPIClient('150.117.123.248', is_https=False, timeout=30)
client.login(username='admin', password='4fcb3244-e5d2-449c-a49d-7b6fa32bfa7f')


# Get
response = client.get(
    path='/api/v2/cmdb/firewall/address',
    params={'format': 'name|subnet'}
)
print(response.text)


# Read & write
response.json()


# Post
response = client.post(
    path='/api/v2/cmdb/firewall/address',
    json={
        'name': 'address 10.210.201.168/32',
        'type': 'ipmask',
        'subnet': '10.210.201.168 255.255.255.255',
    }
)
print(response.text)


# Put
response = client.put(
    path='/api/v2/cmdb/firewall/address' + '/' + quote('address 10.210.201.168/32', safe=''),
    json={
        'name': 'address__10.210.201.168/32',
    }
)
print(response.json())


# Delete
response = client.delete(
    path='/api/v2/cmdb/firewall/address' + '/' + quote('address__10.210.201.168/32', safe=''),
)
print(response.text)
