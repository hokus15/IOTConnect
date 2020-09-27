import logging
from iotconnect.publisher import Publisher


class NoopPublisher(Publisher):
    """ Class implementing a no operation publisher."""

    def __init__(self, config):
        Publisher.__init__(self, config)
        self._log = logging.getLogger('iotconnect.publishers.' + self.__class__.__name__)

    def initialize(self):
        self._log.info("--- Initializing %s ... ---", self.__class__.__name__)
        self._initialized = True
        self._log.info("--- %s initialized ---", self.__class__.__name__)

    def publish(self, context, data):
        pass

    def close(self):
        self._log.info("--- Closing %s ---", self.__class__.__name__)
        self._log.info("--- %s closed ---", self.__class__.__name__)
