from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from {{ cookiecutter.project_slug }}.config.CliConfig import CliConfig
from {{ cookiecutter.project_slug }}.config.cli_config_models import LogLevels
from tests.LoggingTestCase import LoggingTestCase


class TestCliConfig(LoggingTestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.tempDir: Optional[TemporaryDirectory] = None
        self.tempDirPath: Optional[Path] = None
        self.testConfig: Optional[CliConfig] = None

    def setUp(self) -> None:
        super().setUp()
        self.tempDir = TemporaryDirectory()
        self.tempDirPath = Path(self.tempDir.name)
        # let's not pollute home dir with test configs
        CliConfig.DEFAULT_CONFIG_STORAGE_PATH = str(self.tempDirPath)

    def tearDown(self) -> None:
        super().tearDown()
        if self.tempDir:
            self.tempDir.cleanup()

    def test_getConfig(self):
        c = CliConfig.getConfig()
        self.assertIsNotNone(c)
        self.assertEqual(LogLevels.INFO, c.log_level_console)
        self.assertEqual(LogLevels.DEBUG, c.log_level_file)

    def test_update_config(self):
        c = CliConfig.getConfig()
        self.assertIsNotNone(c)
        self.assertEqual(LogLevels.INFO, c.log_level_console)
        self.assertEqual(LogLevels.DEBUG, c.log_level_file)
        c.log_level_console = LogLevels.DEBUG
        c.saveConfig()
        c = CliConfig.getConfig()
        self.assertIsNotNone(c)
        self.assertEqual(LogLevels.DEBUG, c.log_level_console)
        self.assertEqual(LogLevels.DEBUG, c.log_level_file)
