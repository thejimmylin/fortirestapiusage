import requests
from urllib.parse import urlencode


class FortiAPIClient():

    def __init__(self, host, session=None, protocol='http', timeout=12):
        self._host = host
        self._session = session or requests.session()
        self._protocol = protocol
        self._timeout = timeout

    def __repr__(self):
        return f'{self.__class__.__name__}({self._host.__repr__()})'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def host(self):
        return self._host

    @property
    def session(self):
        return self._session

    @property
    def protocol(self):
        return self._protocol

    @property
    def timeout(self):
        return self._timeout

    @property
    def url_root(self):
        url_root = f'{self._protocol}://{self._host}'
        return url_root

    def login(self, username, password, path='/logincheck'):
        url = self.url_root + path
        data = {
            'username': username,
            'secretkey': password,
        }
        encoded_data = urlencode(data)
        response = self._session.post(
            url=url,
            data=encoded_data,
            timeout=self._timeout
        )
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

    def logout(self, path='/logout'):
        url = self.url_root + path
        response = self._session.post(
            url=url,
            timeout=self._timeout
        )
        return response

    def close(self):
        self.logout()
        self._session.close()
