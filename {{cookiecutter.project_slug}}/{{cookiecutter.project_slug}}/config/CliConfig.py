import json
from os import makedirs
from os.path import expanduser, join, dirname, exists
from typing import List, Dict

from {{ cookiecutter.project_slug }}.config.cli_config_models import CliConfig_, LogLevels, System


class CliConfig(CliConfig_):
    KEY_CONFIG_FILE = 'config_file'
    HOME_PATH = expanduser("~")
    CONST_CONFIG_FILE = join(HOME_PATH, '.config', '{{ cookiecutter.project_slug }}', 'config.json')

    config: 'CliConfig' = None

    def __init__(self, config_file: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file: str = config_file

    def saveConfig(self):
        with open(self.config_file, 'w') as json_file:
            json.dump(self.as_dict(), json_file, indent=4)
        pass

    @classmethod
    def getConfig(cls, config_file: str = CONST_CONFIG_FILE):
        if cls.config is None or cls.config.config_file != config_file:
            cls.config = cls.loadConfig(config_file)

        return cls.config

    @classmethod
    def loadConfig(cls, config_file: str) -> 'CliConfig':
        config_path = dirname(config_file)
        if not exists(config_path):
            makedirs(config_path, mode=0o744)

        # config does not exists, sets the defaults and write
        if not exists(config_file):

            config = CliConfig(
                config_file=config_file,
                log_level_console=LogLevels.INFO,
                log_level_file=LogLevels.DEBUG,
            )
            config.saveConfig()
        else:
            with open(config_file, 'r') as json_file:
                jdict: Dict = json.load(json_file)
                config: CliConfig = CliConfig.from_dict(jdict)
        return config

    def as_dict(self):
        d = super().as_dict()
        d[CliConfig.KEY_CONFIG_FILE] = self.config_file
        return d

    @staticmethod
    def from_dict(d, type_map=None, model_type=None):
        if model_type is None:
            model_type = CliConfig
        config = CliConfig_.from_dict(d, type_map, model_type)
        config.config_file = d.get(CliConfig.KEY_CONFIG_FILE, None)
        return config
