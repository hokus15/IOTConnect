import logging


class PublisherError(Exception):
    pass


class Publisher:

    """
        Abstract class implementing publisher.
        Subclasses need to implement publish and close methods.
    """

    def __init__(self, config):
        """Creates the publisher instance and assign the proper attributes."""
        self._log = logging.getLogger('iotconnect.publishers.' + self.__class__.__name__)
        self._config = config
        self._initialized = False

    def initialize(self):
        """Initializes the publisher in order to be used."""
        raise NotImplementedError()

    def publish(self, context, data):
        """Publish the data to the corresponding destination."""
        raise NotImplementedError()

    def close(self):
        """Close the connetions or terminate all streams gracefully."""
        raise NotImplementedError()

    def is_initialized(self):
        """Returns wether the publisher has been initialized successfully (True) or not (False)."""
        return self._initialized
