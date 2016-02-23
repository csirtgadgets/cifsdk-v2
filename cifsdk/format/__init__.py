from cifsdk.format.cifjson import Json
from cifsdk.format.cifcsv import Csv
from cifsdk.format.table import Table
from cifsdk.format.bro import Bro
from cifsdk.format.cifsnort import Snort
from cifsdk.format.cifbind import Bind

plugins = {
    'json': Json,
    'table': Table,
    'csv': Csv,
    'bro': Bro,
    'snort': Snort,
    'bind': Bind,
}

try:
    from cifsdk.format.cif_stix import Stix
    plugins['stix'] = Stix
except:
    pass


# http://stackoverflow.com/a/456747
def factory(name):
    if name in plugins:
        return plugins[name]
    else:
        return None
