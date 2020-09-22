import logging


class Publisher:
    """ Abstract class implementing publisher.
        Subclasses need to implement publish and close methods. """

    def __init__(self, config):
        self._log = logging.getLogger('iotconnect.publishers.' + self.__class__.__name__)
        self._log.info("--- Initializing %s ... ---", self.__class__.__name__)
        self._config = config

    def publish(self, context, data):
        """ Publish the data to the corresponding destination """
        raise NotImplementedError()

    def close(self):
        """ Close the connetions or terminate all streams gracefully """
        raise NotImplementedError()
