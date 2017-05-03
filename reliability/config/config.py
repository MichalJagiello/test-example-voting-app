import os

import yaml


class Config(object):

    CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               'config.yml')

    def __init__(self, config_file=None):
        if config_file:
            self._config_file = config_file
        else:
            self._config_file = self.CONFIG_FILE
        self._config = self._load_config_file()

    def __getitem__(self, key):
        return self._config[key]

    def _load_config_file(self):
        with open(self._config_file) as config_file:
            config = yaml.load(config_file.read())
        return config
