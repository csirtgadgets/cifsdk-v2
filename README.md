# CIF Software Development Kit for Python
The CIF  Software Development Kit (SDK) for Python contains library code and examples designed to enable developers to build applications using CIF.

[![Build Status](https://travis-ci.org/csirtgadgets/py-cif-sdk.png?branch=master)](https://travis-ci.org/csirtgadgets/py-cif-sdk)

# Installation
## Ubuntu
  ```bash
  sudo apt-get install -y python-dev python-pip git
  git clone https://github.com/csirtgadgets/py-cif-sdk.git -b master
  cd py-cif-sdk
  pip install -r requirements.txt
  python setup.py build
  python setup.py test
  python setup.py install
  ```
  
# Examples
## Client
  ```bash
  $ cif --token 1234 --remote 'https://localhost' -q example.com
  ```
  
## API
### Search
  ```python
  from cif.sdk.client import Client
  from prettytable import PrettyTable
  
  def make_table(r):
    cols = ['id','provider','tlp','group','observable','confidence',
            'firsttime','lasttime','reporttime','altid','altid_tlp',
            'tags']
    
    t = PrettyTable(cols)
    t.align['provider'] = 'l'
    if type(r) is not list:
        r = [r]
    
    for obs in r:
        r = []
        for c in cols:
            y = obs.get(c)
            if type(y) is list:
                y = ','.join(y)
            r.append(y)
        t.add_row(r)
    print t
  
  cli = Client(token=1234,
               remote='https://localhost2:8443',
               noverifyssl=1)
  
  ret = cli.search(query='example.com')
  make_table(ret)
  ```
### Ping
  ```python
  from cif.sdk.client import Client
  ...
  
  ret = cli.ping()
  print "roundtrip: %s ms" % ret
  ```

# Support and Documentation

You can also look for information at the [GitHub repo](https://github.com/csirtgadgets/py-cif-sdk).

# License and Copyright

Copyright (C) 2014 [the CSIRT Gadgets Foundation](http://csirtgadgets.org)

Free use of this software is granted under the terms of the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html) (LGPL v3.0). For details see the file ``LICENSE`` included with the distribution.
