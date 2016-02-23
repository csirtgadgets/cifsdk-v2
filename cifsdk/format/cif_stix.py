import arrow
from cifsdk.format.plugin import Plugin
from stix.indicator import Indicator
from stix.core import STIXPackage, STIXHeader
from cybox.common import Hash
from cybox.objects.file_object import File
from cybox.objects.address_object import Address
import re


class Stix(Plugin):

    def __init__(self, *args, **kwargs):
        super(Stix, self).__init__(*args, **kwargs)

    def _create_indicator(self, d):
        def _md5(keypair):
            shv = Hash()
            shv.simple_hash_value = keypair.get('observable')

            f = File()
            h = Hash(shv, Hash.TYPE_MD5)
            f.add_hash(h)
            return f

        def _sha1(keypair):
            shv = Hash()
            shv.simple_hash_value = keypair.get('observable')

            f = File()
            h = Hash(shv, Hash.TYPE_SHA1)
            f.add_hash(h)
            return f

        def _sha256(keypair):
            shv = Hash()
            shv.simple_hash_value = keypair.get('observable')

            f = File()
            h = Hash(shv, Hash.TYPE_SHA256)
            f.add_hash(h)
            return f

        def _address_ipv4(address):
            if re.search('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}', address):
                return 1

        def _address_fqdn(address):
            if re.search('^[a-zA-Z0-9.\-_]+\.[a-z]{2,6}$', address):
                return 1

        def _address_url(address):
            if re.search('^(ftp|https?):\/\/', address):
                return 1

        def _address(keypair):
            address = keypair.get('observable')
            if _address_fqdn(address):
                return Address(address, 'fqdn')
            elif _address_ipv4(address):
                return Address(address, 'ipv4-addr')
            elif _address_url(address):
                return Address(address, 'url')

        indicator = Indicator(timestamp=arrow.get(d.get('reporttime')).datetime)
        indicator.set_producer_identity(d.get('provider'))

        indicator.set_produced_time(arrow.utcnow().datetime)

        indicator.description = ','.join(d.get('tags'))

        otype = d.get('otype')

        if otype == 'md5':
            f = _md5(d)
        elif otype == 'sha1':
            f = _sha1(d)
        elif otype == 'sha256':
            f = _sha256(d)
        else:
            f = _address(d)

        indicator.add_object(f)
        return indicator

    def __repr__(self):
        stix_package = STIXPackage()
        stix_header = STIXHeader()
        stix_package.stix_header = stix_header

        for d in self.data:
            i = self._create_indicator(d)
            stix_package.add_indicator(i)
        return stix_package.to_xml()

