import os
import time
import threading
import logging
import json
from gps3 import agps3
from iotconnect.monitor import Monitor

fix = None  # setting the global variable


class GpsdThread(threading.Thread):
    """Thread that iterate the gpsd info to clear the buffer."""

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        global fix  # bring it in scope
        gps_socket = agps3.GPSDSocket()
        data_stream = agps3.DataStream()
        gps_socket.connect()
        gps_socket.watch()
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                fix = data_stream


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
        global fix  # bring it in scope
        monitor_result = {}
        # It may take some poll calls to get good data
        if (fix.mode == 1 or fix.mode == 'na'):
            self._handle_no_fix('Position not fixed')

        latitude_error = 100000
        if fix.epx != 'na':
            latitude_error = fix.epx

        longitude_error = 1000
        if fix.epy != 'na':
            longitude_error = fix.epy

        fix_accuracy = max(latitude_error,
                           longitude_error)

        self._log.info('Position fixed. Accuracy: +/- %s m',
                       fix_accuracy)
        self._log.debug('Latitude error (EPY): +/- %s m',
                        fix.epy)
        self._log.debug('Longitude error (EPX): +/- %s m',
                        fix.epx)
        if fix_accuracy < self._min_accuracy:
            self._retries = 0
            monitor_result.update({
                'last_update': int(round(time.time())),
                'latitude': fix.lat,
                'longitude': fix.lon,
                'gps_accuracy': fix_accuracy,
                # Estimated Speed error
                'eps': fix.eps,
                # Estimated longitude error
                'epx': fix.epx,
                # Estimated latitude error
                'epy': fix.epy,
                # Estimated altitude error
                'epv': fix.epv,
                # Estimated time error
                'ept': fix.ept,
                'speed': fix.speed,  # m/s
                'climb': fix.climb,
                'track': fix.track,
                'mode': fix.mode
            })
            if self._previous_latitude != 0 and self._previous_longitude != 0:
                # Previous latitude and longitude data is useful to
                # measure distance travelled between updates.
                monitor_result.update({
                    # Latitude got from previous read
                    'platitude': self._previous_latitude,
                    # Longitude got from previous read
                    'plongitude': self._previous_longitude
                })
            self._previous_latitude = fix.lat
            self._previous_longitude = fix.lon
            self._log.info("type: gps fix, data: %s", json.dumps(monitor_result))
            return {'location': monitor_result}
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
