import logging
from threading import Thread
import time


class MonitorError(Exception):
    pass


class Monitor:

    """Abstract class implementing monitor."""

    def __init__(self, config, publishers):
        self._log = logging.getLogger('iotconnect.monitors.' + self.__class__.__name__)
        self._log.info("--- Initializing %s ---", self.__class__.__name__)
        self._thread = None
        self._running = False
        self._config = config
        self._publishers = publishers
        self._interval = self._config['interval']

    def monitor(self):
        raise NotImplementedError()

    def run(self):
        while self._running:
            try:
                now = time.time()
                monitor_result = self.monitor()
                for publisher in self._publishers:
                    for context, data in monitor_result.items():
                        publisher.publish(context, data)
            except (Exception) as err:
                self._log.warning(err, exc_info=False)
            finally:
                interval = self._interval - (time.time() - now)
                time.sleep(max(0, interval))

    def start(self):
        """Start the monitor thread."""
        self._running = True
        self._thread = Thread(target=self.run, name=self.__class__.__name__)
        self._thread.start()
        self._log.info("--- %s started ---", self.__class__.__name__)

    def stop(self):
        """Stop the monitor thread."""
        self._log.info("--- Stopping %s ---", self.__class__.__name__)
        self._running = False
        if self._thread is not None:
            self._thread.join()

    def check_thread(self):
        """ Return running monitor state. """
        return self._thread is not None and self._thread.is_alive()
