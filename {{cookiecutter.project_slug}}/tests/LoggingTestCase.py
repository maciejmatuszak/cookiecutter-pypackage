import logging
import sys
import unittest


class LoggingTestCase(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.logger: logging.Logger = logging.getLogger('test')

    def setUp(self) -> None:
        root = logging.getLogger()
        stream_handlers = [h for h in root.handlers if isinstance(h, logging.StreamHandler)]
        if stream_handlers:
            stream_handler = stream_handlers[0]
        else:
            stream_handler = logging.StreamHandler(sys.stdout)

        stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-5s %(name)-24s %(message)s'))
        root.addHandler(stream_handler)
        root.setLevel(logging.DEBUG)
        self.logger = logging.getLogger('test')

        # disable garbage from matplotlib
        logger = logging.getLogger('matplotlib.font_manager')
        logger.setLevel(logging.WARNING)

        super().setUp()

    def cleanUpSqlAlchemyLoggers(self):
        # sqlalchemy puts handler on child logger - clean it up!!!

        sqlalchemyLogger = logging.getLogger('sqlalchemy.engine.Engine')
        if sqlalchemyLogger.handlers:
            for handler in sqlalchemyLogger.handlers:
                sqlalchemyLogger.removeHandler(handler)
