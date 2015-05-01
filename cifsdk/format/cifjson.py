from cifsdk.format.plugin import Plugin
import json


class Json(Plugin):

    def __init__(self, *args, **kwargs):
        super(Json, self).__init__(*args, **kwargs)

    def __repr__(self):
        return json.dumps(self.data)