:orphan:

cif.yml manual page
===================

DESCRIPTION
-----------

*cif.yml* is the config file used to set defaults for the *cif* commands. 

OPTIONS
-------

client
    specify the client section of the config.

remote
    specify the API url

token
    specify a token for the API

no_verify_ssl
    turn off TLS verification


EXAMPLES
--------

.. code:: yaml

    ---
    client:
        remote: https://cif.test
        token: 12341234
        no_verify_ssl: true


SEE ALSO
--------

Extensive documentation is available in the documentation site: <py-cifsdk.rtfd.org>. 

