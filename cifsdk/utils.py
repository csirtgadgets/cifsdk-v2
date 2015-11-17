import pkgutil
import logging
import yaml
import os
from cifsdk.constants import LOG_FORMAT
from argparse import ArgumentParser

from cifsdk.constants import REMOTE_ADDR


def read_config(args):
    options = {}
    if os.path.isfile(args.config):
        f = file(args.config)
        config = yaml.load(f)
        f.close()
        if not config:
            raise Exception("Unable to read {} config file".format(args.config))
        for k in config:
            if not options.get(k):
                options[k] = config[k]

        if config.get('remote') and (options['remote'] == REMOTE_ADDR):
            options['remote'] = config['remote']
    else:
        raise Exception("Unable to read {} config file".format(args.config))

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
