import json
import os
import stat

from os.path import expanduser, join
from pathlib import Path
from typing import Dict, Optional

from {{ cookiecutter.project_slug }}.config.cli_config_models import CliConfig_, LogLevels


class CliConfig(CliConfig_):
    CONST_CONFIG_DIR_MODE = stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH
    CONST_CONFIG_FILE_MODE = stat.S_IRWXU
    KEY_CONFIG_FILE = 'config_file'
    DEFAULT_CONFIG_STORAGE_PATH = join(expanduser("~"), '.config')
    DEFAULT_CONFIG_FILE_PATH = join('python_boilerplate', 'config.json')

    @classmethod
    def get_default_config_path(cls) -> Path:
        return Path(cls.DEFAULT_CONFIG_STORAGE_PATH, cls.DEFAULT_CONFIG_FILE_PATH)

    config: Optional['CliConfig'] = None

    def __init__(self, config_file: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file: str = config_file

    def saveConfig(self):
        with open(self.config_file, 'w') as json_file:
            json.dump(self.as_dict(), json_file, indent=4)
        os.chmod(self.config_file, self.CONST_CONFIG_FILE_MODE)
        pass

    @classmethod
    def getConfig(cls, config_file: str = None) -> 'CliConfig':
        if config_file is None:
            config_file = str(cls.get_default_config_path())

        # if loaded config is from different file then reset it
        if cls.config is not None:
            if config_file != cls.config.config_file:
                cls.config = None

        if cls.config is None:
            cls.config = cls.loadConfig(config_file)

        return cls.config

    @classmethod
    def loadConfig(cls, config_file_: str) -> 'CliConfig':
        config_file = Path(config_file_)

        # create parent folder if not exists
        if not config_file.parent.exists():
            config_file.parent.mkdir(mode=CliConfig.CONST_CONFIG_DIR_MODE, parents=True)
            pass

        # config does not exists, sets the defaults and write
        if not config_file.exists():

            logFilePath = config_file.parent.joinpath('logs', 'python_boilerplate.log')
            # make sure logs folder exists
            if not logFilePath.parent.exists():
                logFilePath.parent.mkdir(mode=CliConfig.CONST_CONFIG_DIR_MODE, parents=True)

            config = CliConfig(
                config_file=str(config_file),
                log_level_console=LogLevels.INFO,
                log_level_file=LogLevels.DEBUG,
                log_file=str(logFilePath)
            )
            config.saveConfig()
        else:
            with open(config_file, 'r') as json_file:
                jdict: Dict = json.load(json_file)
                config = CliConfig.from_dict(jdict)
        return config

    def as_dict(self):
        d = super().as_dict()
        # config_file property is outside of json generated model
        d[CliConfig.KEY_CONFIG_FILE] = self.config_file
        return d

    @staticmethod
    def from_dict(d, type_map=None, model_type=None):
        if model_type is None:
            model_type = CliConfig
        config = CliConfig_.from_dict(d, type_map, model_type)

        # config_file property is outside of json generated model
        config.config_file = d.get(CliConfig.KEY_CONFIG_FILE, None)
        return config
