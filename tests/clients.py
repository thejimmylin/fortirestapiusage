import os
import unittest
import json
from urllib.parse import quote
from fortirestapiusage.clients import FortiAPIClient


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'secrets.json'), 'r', encoding='utf-8') as f:
    secrets = json.loads(f.read())


HOST = secrets['CREDENTIALS']['host']
USERNAME = secrets['CREDENTIALS']['users']['api_admin']['username']
PASSWORD = secrets['CREDENTIALS']['users']['api_admin']['password']


class FortiAPIClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = FortiAPIClient(HOST)
        r = self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )
        status_code = r.text[:1]
        descriptions = {
            '0': 'Log in failure. Most likely an incorrect username/password combo.',
            '1': 'Successful log in',
            '2': 'Admin is now locked out',
            '3': 'Two-factor Authentication is needed',
        }
        msg = descriptions.get(status_code, 'Unknown error. Can you log in manually?')
        is_logged_in = (status_code == '1')
        if not is_logged_in:
            raise ValueError(msg)

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
        for n in range(10):
            self.client.login(
                username=USERNAME,
                password=PASSWORD,
            )
            self.client.logout()
        r = self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )
        self.assertIsNotNone(r.cookies.get('ccsrftoken'))

    def test_post_delete_heavily(self):
        for n in range(10):
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

    def test_post_system_interface_with_json_comment_and_check_consistency_and_delete(self):
        name = '_vlan__1688'
        vdom = 'root'
        type_ = 'vlan'
        ip = '10.65.61.253 255.255.255.0'
        # both int and str are ok
        vlanid = 1688
        interface = 'port3'
        created_by = 'jimmy_lin'
        remark = 'This is a remark field.'
        self.client.post(
            path='/api/v2/cmdb/system/interface',
            json={
                'name': name,
                'vdom': vdom,
                'type': type_,
                'ip': ip,
                'vlanid': vlanid,
                'interface': interface,
                'description': json.dumps({
                    'created_by': created_by,
                    'remark': remark,
                }),
            }
        )
        r = self.client.get(
            path='/api/v2/cmdb/system/interface' + '/' + quote(name, safe=''),
        )
        self.assertEqual(r.json()['status'], 'success')
        self.assertEqual(len(r.json()['results']), 1)
        self.assertEqual(r.json()['results'][0]['name'], name)
        self.assertEqual(r.json()['results'][0]['vdom'], vdom)
        self.assertEqual(r.json()['results'][0]['type'], type_)
        self.assertEqual(r.json()['results'][0]['ip'], ip)
        self.assertEqual(r.json()['results'][0]['vlanid'], vlanid)
        self.assertEqual(r.json()['results'][0]['interface'], interface)
        self.assertEqual(json.loads(r.json()['results'][0]['description'])['created_by'], created_by)
        self.assertEqual(json.loads(r.json()['results'][0]['description'])['remark'], remark)
        self.client.delete(
            path='/api/v2/cmdb/system/interface' + '/' + quote(name, safe=''),
        )

    def test_post_firewall_address_with_json_comment_and_check_consistency_and_delete(self):
        name = '_address__10.65.61.168/32'
        type_ = 'ipmask'
        subnet = '10.65.61.168 255.255.255.255'
        created_by = 'jimmy_lin'
        remark = 'This is a remark field.'
        self.client.post(
            path='/api/v2/cmdb/firewall/address',
            json={
                'name': name,
                'type': type_,
                'subnet': subnet,
                'comment': json.dumps({
                    'created_by': created_by,
                    'remark': remark,
                }),
            }
        )
        r = self.client.get(
            path='/api/v2/cmdb/firewall/address' + '/' + quote(name, safe=''),
        )
        self.assertEqual(r.json()['status'], 'success')
        self.assertEqual(len(r.json()['results']), 1)
        self.assertEqual(r.json()['results'][0]['name'], name)
        self.assertEqual(r.json()['results'][0]['type'], type_)
        self.assertEqual(r.json()['results'][0]['subnet'], subnet)
        self.assertEqual(json.loads(r.json()['results'][0]['comment'])['created_by'], created_by)
        self.assertEqual(json.loads(r.json()['results'][0]['comment'])['remark'], remark)
        self.client.delete(
            path='/api/v2/cmdb/firewall/address' + '/' + quote('_address__10.65.61.168/32', safe=''),
        )

    def test_post_firewall_service_with_json_comment_and_check_consistency_and_delete(self):
        name = '_service__tcp_portrange__50001__59999__udp_portrange__50001__59999'
        tcp_portrange = '50001 59999'
        udp_portrange = '50001 59999'
        created_by = 'jimmy_lin'
        remark = 'This is a remark field.'
        self.client.post(
            path='/api/v2/cmdb/firewall.service/custom',
            json={
                'name': name,
                'tcp-portrange': tcp_portrange,
                'udp-portrange': udp_portrange,
                'comment': json.dumps({
                    'created_by': created_by,
                    'remark': remark,
                }),
            }
        )
        r = self.client.get(
            path='/api/v2/cmdb/firewall.service/custom' + '/' + quote(name, safe=''),
        )
        self.assertEqual(r.json()['status'], 'success')
        self.assertEqual(len(r.json()['results']), 1)
        self.assertEqual(r.json()['results'][0]['name'], name)
        self.assertEqual(r.json()['results'][0]['tcp-portrange'], tcp_portrange)
        self.assertEqual(r.json()['results'][0]['udp-portrange'], udp_portrange)
        self.assertEqual(json.loads(r.json()['results'][0]['comment'])['created_by'], created_by)
        self.assertEqual(json.loads(r.json()['results'][0]['comment'])['remark'], remark)
        self.client.delete(
            path='/api/v2/cmdb/firewall.service/custom' + '/' + quote(name, safe=''),
        )

    def test_post_firewall_ippool_with_json_comment_and_check_consistency_and_delete(self):
        name = '_ippool__168.65.61.168'
        type_ = 'overload'
        startip = '168.65.61.168'
        endip = '168.65.61.168'
        created_by = 'jimmy_lin'
        remark = 'This is a remark field.'
        self.client.post(
            path='/api/v2/cmdb/firewall/ippool',
            json={
                'name': name,
                'type': type_,
                'startip': startip,
                'endip': endip,
                'comments': json.dumps({
                    'created_by': created_by,
                    'remark': remark,
                }),
            }
        )
        r = self.client.get(
            path='/api/v2/cmdb/firewall/ippool' + '/' + quote(name, safe=''),
        )
        self.assertEqual(r.json()['status'], 'success')
        self.assertEqual(len(r.json()['results']), 1)
        self.assertEqual(r.json()['results'][0]['name'], name)
        self.assertEqual(r.json()['results'][0]['type'], type_)
        self.assertEqual(r.json()['results'][0]['startip'], startip)
        self.assertEqual(r.json()['results'][0]['endip'], endip)
        self.assertEqual(json.loads(r.json()['results'][0]['comments'])['created_by'], created_by)
        self.assertEqual(json.loads(r.json()['results'][0]['comments'])['remark'], remark)
        self.client.delete(
            path='/api/v2/cmdb/firewall/ippool' + '/' + quote(name, safe=''),
        )

    def test_post_firewall_vip_with_json_comment_and_check_consistency_and_delete(self):
        name = '_vip__100.65.61.168__10.65.61.168'
        type_ = 'static-nat'
        extintf = 'port1'
        extip = '100.65.61.168'
        mappedip = '10.65.61.168'
        created_by = 'jimmy_lin'
        remark = 'This is a remark field.'
        r = self.client.post(
            path='/api/v2/cmdb/firewall/vip',
            json={
                'name': name,
                'type': type_,
                'extintf': extintf,
                'extip': extip,
                'mappedip': [{'range': mappedip}],
                'comment': json.dumps({
                    'created_by': created_by,
                    'remark': remark,
                }),
            }
        )
        r = self.client.get(
            path='/api/v2/cmdb/firewall/vip' + '/' + quote(name, safe=''),
        )
        self.assertEqual(r.json()['status'], 'success')
        self.assertEqual(len(r.json()['results']), 1)
        self.assertEqual(r.json()['results'][0]['name'], name)
        self.assertEqual(r.json()['results'][0]['extip'], extip)
        self.assertEqual(r.json()['results'][0]['mappedip'][0]['range'], mappedip)
        self.assertEqual(json.loads(r.json()['results'][0]['comment'])['created_by'], created_by)
        self.assertEqual(json.loads(r.json()['results'][0]['comment'])['remark'], remark)
        self.client.delete(
            path='/api/v2/cmdb/firewall/vip' + '/' + quote(name, safe=''),
        )

    def test_post_firewall_policy_with_json_comment_and_check_consistency_and_delete(self):
        name = '_address__10.65.61.168/32'
        type_ = 'ipmask'
        subnet = '10.65.61.168 255.255.255.255'
        created_by = 'jimmy_lin'
        remark = 'This is a remark field.'
        self.client.post(
            path='/api/v2/cmdb/firewall/address',
            json={
                'name': name,
                'type': type_,
                'subnet': subnet,
                'comment': json.dumps({
                    'created_by': created_by,
                    'remark': remark,
                }),
            }
        )
        r = self.client.post(
            path='/api/v2/cmdb/firewall/policy',
            json={
                'srcintf': [{"name": "port1"}],
                'dstintf': [{"name": "port3"}],
                'srcaddr': [{"name": "all"}],
                'dstaddr': [{"name": "all"}],
                'schedule': "always",
                'service': [{"name": "HTTP"}, {"name": "HTTPS"}],
                'action': "accept",
                'comments': json.dumps({
                    'created_by': created_by,
                    'remark': remark,
                }),
            }
        )
        mkey = str(r.json()['mkey'])
        r = self.client.get(
            path='/api/v2/cmdb/firewall/policy' + '/' + quote(mkey, safe=''),
        )
        self.assertEqual(json.loads(r.json()['results'][0]['comments'])['created_by'], created_by)
        self.assertEqual(json.loads(r.json()['results'][0]['comments'])['remark'], remark)
        self.client.delete(
            path='/api/v2/cmdb/firewall/policy' + '/' + quote(mkey, safe=''),
        )
        r = self.client.post(
            path='/api/v2/cmdb/firewall/policy',
            json={
                'srcintf': [{"name": "port1"}],
                'dstintf': [{"name": "port3"}],
                'srcaddr': [{"name": "_address__10.65.61.168__255.255.255.255"}],
                'dstaddr': [{"name": "all"}],
                'schedule': "always",
                'service': [{"name": "HTTP"}, {"name": "HTTPS"}],
                'action': "accept",
                "nat": "enable",
                "ippool": "enable",
                "poolname": [{"name": "ippool__150.117.123.177__150.117.123.177"}],
                'comments': json.dumps({
                    'created_by': created_by,
                    'remark': remark,
                }),
            }
        )
        mkey = str(r.json()['mkey'])
        r = self.client.get(
            path='/api/v2/cmdb/firewall/policy' + '/' + quote(mkey, safe=''),
        )
        self.assertEqual(json.loads(r.json()['results'][0]['comments'])['created_by'], created_by)
        self.assertEqual(json.loads(r.json()['results'][0]['comments'])['remark'], remark)
        self.client.delete(
            path='/api/v2/cmdb/firewall/policy' + '/' + quote(mkey, safe=''),
        )

    def tearDown(self):
        self.client.close()


if __name__ == '__main__':
    unittest.main()
