import logging
from iotconnect.monitor import Monitor


class NoopMonitor(Monitor):
    """Class implementing no operation Monitor."""

    def __init__(self, config, callback):
        Monitor.__init__(self, config, callback)
        self._log = logging.getLogger('iotconnect.monitors.' + self.__class__.__name__)

    def monitor(self):
        return {}

    def start(self):
        self._log.info("--- Starting %s ---", self.__class__.__name__)
        super().start()

    def stop(self):
        super().stop()
        self._log.info("--- %s stopped ---", self.__class__.__name__)
