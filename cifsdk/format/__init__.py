

from cifsdk.format.cifjson import Json
from cifsdk.format.cifcsv import Csv
from cifsdk.format.table import Table

plugins = {
    'json': Json,
    'table': Table,
    'csv': Csv
}


# http://stackoverflow.com/a/456747
def factory(name):
    if name in plugins:
        return plugins[name]
    else:
        return None