

from cifsdk.format.cifjson import Json
from cifsdk.format.cifcsv import Csv
from cifsdk.format.table import Table
from cifsdk.format.bro import Bro

plugins = {
    'json': Json,
    'table': Table,
    'csv': Csv,
    'bro': Bro
}


# http://stackoverflow.com/a/456747
def factory(name):
    if name in plugins:
        return plugins[name]
    else:
        return None
