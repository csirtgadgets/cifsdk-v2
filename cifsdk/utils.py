import pkgutil
import logging
import yaml
import os
from cifsdk.constants import LOG_FORMAT


def read_config(args):
    options = {}
    if os.path.isfile(args.config):
        f = file(args.config)
        config = yaml.load(f)
        config = config['client']
        f.close()
        if not config:
            print("Unable to read {} config file".format(args.config))
            raise SystemExit
        for k in config:
            if not options.get(k):
                options[k] = config[k]
    else:
        print("Unable to read {} config file".format(args.config))
        raise SystemExit

    return options


def load_plugin(path, plugin):
    p = None
    for loader, modname, is_pkg in pkgutil.iter_modules([path]):
        if modname == plugin:
            p = loader.find_module(modname).load_module(modname)
            p = p.Plugin

    return p


def setup_logging(args):
    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)
