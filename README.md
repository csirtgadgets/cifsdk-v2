# CIF Software Development Kit for Python
The CIF  Software Development Kit (SDK) for Python contains library code and examples designed to enable developers to build applications using CIF.

[![Build Status](https://travis-ci.org/csirtgadgets/py-cifsdk.png?branch=master)](https://travis-ci.org/csirtgadgets/py-cifsdk)

# WARNING
**Before you begin, be careful when installing this on a CIF Server Instance. This WILL OVERWRITE the p5-cif-sdk 
bin/cif command on the server. This SDK is meant to be used as a client interacting with a REMOTE CIF Instance.**

# Installation

## Ubuntu
  ```bash
  $ sudo apt-get install -y python-dev python-pip git
  $ pip install cifsdk
  ```
## CentOS v 7
  ```bash
  $ yum -y update
  $ sudo rpm -iUvh http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
  $ sudo yum install -y gcc python-pip python-devel git libffi-devel openssl-devel python-virtualenvwrapper python-virtualenv
  $ pip install cifsdk
  ```
# Examples
## Client
### Config
  ```yaml
  # ~/.cif.yml
  client:
    remote: https://localhost
    token: 1234
  ```
### Running out of the box
These plugins are minimal and run out of the box

  ```bash
  $ cif --token 1234 --remote 'https://localhost' -q example.com
  $ cif --token 1234 --remote 'https://localhost' -q example.com --format csv
  $ cif --token 1234 --remote 'https://localhost' -q example.com --format table
  $ cif --token 1234 --remote 'https://localhost' -q example.com --format json
  ```

### Running with 3rd party plugins
These plugins typically require extra [bloated] code, not installed by default

#### STIX
   ```bash
   $ pip install stix  # requires many other 3rd party xml bloat
   $ cif --token 1234 --remote 'https://localhost' -q example.com --format stix
   ```
   
## API
### Search
  ```python
  import logging
  from cifsdk.client import Client
  from cifsdk.format import Table

  LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'
  loglevel = logging.INFO
  console = logging.StreamHandler()
  logging.getLogger('').setLevel(loglevel)
  console.setFormatter(logging.Formatter(LOG_FORMAT))
  logging.getLogger('').addHandler(console)

  cli = Client(token='1234',
               remote='https://localhost',
               verify_ssl=False)


  ret = cli.search('example.com')
  print Table(ret)

  filters = {
    "observable": "example.com",
    "confidence": 35,
  }

  ret = cli.search(filters=filters)
  print(Table(ret))
  ```

### Submit
   ```python
   import logging
   from cifsdk.client import Client

   LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'
   loglevel = logging.INFO
   console = logging.StreamHandler()
   logging.getLogger('').setLevel(loglevel)
   console.setFormatter(logging.Formatter(LOG_FORMAT))
   logging.getLogger('').addHandler(console)

   data = '{"observable":"example4.com","tlp":"amber","confidence":"85","tags":"malware","provider":"example.com","group":"everyone"}'

   cli = Client(token='1234',
               remote='https://localhost',
               verify_ssl=False)

   ret = cli.submit(data)
   print("submission id: {0}".format(ret))
   ```

### Ping
  ```python
  from cifsdk.client import Client
  ...

  ret = cli.ping()
  print("roundtrip: %s ms" % ret)
  ```

# Support and Documentation

You can also look for information at the [GitHub repo](https://github.com/csirtgadgets/py-cifsdk).

# License and Copyright

Copyright (C) 2015 [the CSIRT Gadgets Foundation](http://csirtgadgets.org)

Free use of this software is granted under the terms of the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html) (LGPL v3.0). For details see the file ``LICENSE`` included with the distribution.
