# fortirestapiusage
Python module about wrapped FortiOS REST API usages.

> For FortiOS, FortiGate firewall.

## Installation

OS X & Linux:

```
python3 -m venv /Users/jimmy_lin/envs/fortirestapiusage
source /Users/jimmy_lin/envs/fortirestapiusage/bin/activate
git clone https://github.com/j3ygithub/fortirestapiusage /Users/jimmy_lin/repos/fortirestapiusage
pip install -r /Users/jimmy_lin/repos/fortirestapiusage/requirements.txt
```

Windows:

```
python -m venv C:\Users\jimmy_lin\envs\fortirestapiusage
C:\Users\jimmy_lin\envs\fortirestapiusage\Scripts\activate
git clone https://github.com/j3ygithub/fortirestapiusage C:\Users\jimmy_lin\repos\fortirestapiusage
pip install -r C:\Users\jimmy_lin\repos\fortirestapiusage\requirements.txt
```

## Run tests

```
>>> pwd
/Users/jimac/repos/fortirestapiusage
>>> python -m tests.clients
...........
----------------------------------------------------------------------
Ran 11 tests in 6.203s

OK
```

## Usages

```
>>> from fortirestapiusage.clients import FortiAPIClient
>>> client = FortiAPIClient(host='150.117.123.248')
>>> cleint.login(username='your_username', password='your_password')
>>> r = client.get(path='/api/v2/cmdb/system/interface', params={'format': 'name|type', 'count': 3})
>>> print(r.text)
{
  "http_method":"GET",
  "revision":"71f322b1061f9acd6171c941a7e5dcf4",
  "results":[
    {
      "name":"fortilink",
      "q_origin_key":"fortilink",
      "type":"aggregate"
    },
    {
      "name":"port1",
      "q_origin_key":"port1",
      "type":"physical"
    },
    {
      "name":"port2",
      "q_origin_key":"port2",
      "type":"physical"
    }
  ],
  "vdom":"root",
  "path":"system",
  "name":"interface",
  "status":"success",
  "http_status":200,
  "serial":"FGVMEV_B6WKV3L0D",
  "version":"v6.4.2",
  "build":1723
}
```

## Meta

Jimmy Lin <b00502013@gmail.com>

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/j3ygithub/](https://github.com/j3ygithub/)

## Contributing

1. Fork it (<https://github.com/j3ygithub/fortirestapiusage/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
