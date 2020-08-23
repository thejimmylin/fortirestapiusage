from base import FortiAPIClient
from urllib.parse import quote


# Usage
# Login - Admin
client = FortiAPIClient('150.117.123.248')
client.login(username='admin', password='4fcb3244-e5d2-449c-a49d-7b6fa32bfa7f')


# # Login - Readonly admin
# client = FortiAPIClient('150.117.123.248')
# client.login(username='readonlyadmin', password='readonlyadmin')


# Get
response = client.get(
    path='/api/v2/cmdb/firewall/address',
    params={'format': 'name|subnet'}
)
print(response.text)


# Read & write
data = response.json()
# Do something with data
# ....
# ....


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
