import os
import time
import threading
import logging
import json
import gps
from iotconnect.monitor import Monitor

gpsd = None  # setting the global variable


class GpsdThread(threading.Thread):
    """Thread that iterate the gpsd info to clear the buffer."""

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        global gpsd  # bring it in scope
        gpsd = gps.gps(mode=gps.WATCH_ENABLE)  # starting the stream of info

    def run(self):
        global gpsd
        while True:
            # this will continue to loop and grab EACH set of
            # gpsd info to clear the buffer
            next(gpsd)


class GpsMonitor(Monitor):
    """Class implementing Monitor that reads data from gpsd."""

    def __init__(self, config, callback):
        Monitor.__init__(self, config, callback)
        self._log = logging.getLogger('iotconnect.monitors.' + self.__class__.__name__)
        self._gpsd_thread = GpsdThread()
        self._gpsd_thread.start()
        self._min_accuracy = self._config['min_accuracy']
        self._retries_before_reboot = self._config['retries_before_reboot']
        self._previous_latitude = 0
        self._previous_longitude = 0
        self._retries = 0

    def monitor(self):
        """Monitor the gps."""
        fix = {}

        # It may take some poll calls to get good data
        if (gpsd.fix.mode == 1):
            self._handle_no_fix('Position not fixed')

        fix_accuracy = max(gpsd.fix.epy,
                           gpsd.fix.epx)
        self._log.info('Position fixed. Accuracy: +/- %s m',
                       fix_accuracy)
        self._log.debug('Latitude error (EPY): +/- %s m',
                        gpsd.fix.epy)
        self._log.debug('Longitude error (EPX): +/- %s m',
                        gpsd.fix.epx)
        if fix_accuracy < self._min_accuracy:
            self._retries = 0
            fix.update({
                'last_update': int(round(time.time())),
                'latitude': gpsd.fix.latitude,
                'longitude': gpsd.fix.longitude,
                'gps_accuracy': fix_accuracy,
                # Estimated Speed error
                'eps': gpsd.fix.eps,
                # Estimated longitude error
                'epx': gpsd.fix.epx,
                # Estimated latitude error
                'epy': gpsd.fix.epy,
                # Estimated altitude error
                'epv': gpsd.fix.epv,
                # Estimated time error
                'ept': gpsd.fix.ept,
                'speed': gpsd.fix.speed,  # m/s
                'climb': gpsd.fix.climb,
                'track': gpsd.fix.track,
                'mode': gpsd.fix.mode
            })
            if self._previous_latitude != 0 and self._previous_longitude != 0:
                # Previous latitude and longitude data is useful to
                # measure distance travelled between updates.
                fix.update({
                    # Latitude got from previous read
                    'platitude': self._previous_latitude,
                    # Longitude got from previous read
                    'plongitude': self._previous_longitude
                })
            self._previous_latitude = gpsd.fix.latitude
            self._previous_longitude = gpsd.fix.longitude
            self._log.info(json.dumps(fix))
            return {'location': fix}
        else:
            self._handle_no_fix('Low accuracy: it\'s +/- {} m but +/- {} m required'
                                .format(fix_accuracy, self._min_accuracy))

    def start(self):
        self._log.info('--- Starting %s ---', self.__class__.__name__)
        super().start()

    def stop(self):
        super().stop()
        self._log.info('--- %s stopped ---', self.__class__.__name__)

    def _handle_no_fix(self, message):
        self._retries += 1
        # self._log.warning(message)
        if self._retries_before_reboot > 0 and self._retries >= self._retries_before_reboot:  # noqa: E501
            self._log.critical('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            self._log.critical('! Too many times (%s) without fixing the position, REBOOTING in 5 seconds... !',
                               self._retries)
            self._log.critical('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            time.sleep(5)
            os.system('sudo reboot')
        else:
            if self._retries_before_reboot > 0:
                raise Exception('({}/{}) {}'.format(self._retries, self._retries_before_reboot, message))
            else:
                raise Exception('({}) {}'.format(self._retries, message))
