# CIF Software Development Kit for Python
The CIF  Software Development Kit (SDK) for Python contains library code and examples designed to enable developers to build applications using CIF.

[![Build Status](https://travis-ci.org/csirtgadgets/cif-sdk-python.png?branch=master)](https://travis-ci.org/csirtgadgets/cif-sdk-python)

# Installation
 * get the [latest release](https://github.com/csirtgadgets/cif-sdk-python/releases)
 * install the SDK  

  ```bash
  $ tar -zxvf cif-sdk-x.x.x.tar.gz
  $ cd cif-sdk
  $ python setup.py build
  $ python setup.py test
  $ python -m unittest discover
  $ sudo python setup.py install
  ```
  
# Examples
## Client
  ```bash
  $ cifpy -T 1234 -R 'https://localhost/api' -q example.com
  ```
  
## API
### Search
  ```python
  from cif.sdk.client import Client
  
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

# License and Copyright
Free use of this software is granted under the terms of the GNU Lesser General Public License (LGPLv3). For details see the files `COPYING` included with the distribution.
