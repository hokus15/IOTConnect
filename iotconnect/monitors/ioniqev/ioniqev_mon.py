import time
import json
import logging
import obd
from obd import OBDStatus
from .commands import ext_commands
from iotconnect.monitor import Monitor


class OBDIIConnectionError(Exception):
    pass


class CanError(Exception):
    pass


class IoniqEVMonitor(Monitor):

    """
    Class implementing Monitor that reads data from Hyundai Ioniq EV
    using OBDII.
    """

    def __init__(self, config, callback):
        """Inits the monitor."""
        Monitor.__init__(self, config, callback)
        self._log = logging.getLogger('iotconnect.monitors.' + self.__class__.__name__)
        self._port = config['port']
        self._baudrate = int(config['baudrate'])
        self._fast = False
        self._timeout = 30
        self._max_attempts = 3
        self._battery_capacity = 28
        self._connection = None

    def _obd_connect(self):
        connection_count = 0
        obd_connection = None
        while ((obd_connection is None or obd_connection.status() != OBDStatus.CAR_CONNECTED)
               and connection_count < self._max_attempts):
            connection_count += 1
            # Establish connection with OBDII dongle
            obd_connection = obd.OBD(portstr=self._port,
                                     baudrate=self._baudrate,
                                     fast=self._fast,
                                     timeout=self._timeout)
            if ((obd_connection is None or obd_connection.status() != OBDStatus.CAR_CONNECTED)
                    and connection_count < self._max_attempts):
                self._log.warning("%s. Retrying in %s second(s)...",
                                  obd_connection.status(),
                                  connection_count)
                time.sleep(connection_count)

        if obd_connection.status() != OBDStatus.CAR_CONNECTED:
            raise OBDIIConnectionError(obd_connection.status())
        else:
            return obd_connection

    def _query_command(self, command, max_attempts=3):
        command_count = 0
        cmd_response = None
        exception = False
        valid_response = False
        while not valid_response and command_count < max_attempts:
            command_count += 1
            try:
                cmd_response = self._connection.query(command, force=True)
            except Exception:
                exception = True
            valid_response = (not(cmd_response is None
                                  or cmd_response.is_null()
                                  or cmd_response.value is None
                                  or cmd_response.value == "?"
                                  or cmd_response.value == ""
                                  or exception))
            if not valid_response and command_count < max_attempts:
                self._log.warning("No valid response for %s. Retrying in %s second(s)...",
                                  command,
                                  command_count)
                time.sleep(command_count)

        if not valid_response:
            raise ValueError("No valid response for {}. Max attempts ({}) exceeded."
                             .format(command, max_attempts))
        else:
            self._log.info("Got response from command: %s ", command)
            return cmd_response

    def _query_battery_info(self):
        self._log.info("**** Querying battery information ****")
        battery_info = {}
        # Set header to 7E4
        self._query_command(ext_commands["CAN_HEADER_7E4"])
        # Set the CAN receive address to 7EC
        self._query_command(ext_commands["CAN_RECEIVE_ADDRESS_7EC"])

        # 2101 - 2105 codes to get battery status information
        bms_2101_resp = self._query_command(ext_commands["BMS_2101"])
        bms_2102_resp = self._query_command(ext_commands["BMS_2102"])
        bms_2103_resp = self._query_command(ext_commands["BMS_2103"])
        bms_2104_resp = self._query_command(ext_commands["BMS_2104"])
        bms_2105_resp = self._query_command(ext_commands["BMS_2105"])

        # Extract status of health value from corresponding response
        soh = bms_2105_resp.value["soh"]

        # Only create battery status data if got a consistent
        # Status Of Health (sometimes it's not consistent)
        if soh <= 100:
            charging = bms_2101_resp.value["charging"]

            battery_current = bms_2101_resp.value["dcBatteryCurrent"]
            battery_voltage = bms_2101_resp.value["dcBatteryVoltage"]

            battery_cell_max_deterioration = bms_2105_resp.value["dcBatteryCellMaxDeterioration"]
            battery_cell_min_deterioration = bms_2105_resp.value["dcBatteryCellMinDeterioration"]
            soc_display = bms_2105_resp.value["socDisplay"]

            mins_to_complete = 0

            # Calculate time to fully charge (only when charging)
            if charging == 1:
                average_deterioration = (battery_cell_max_deterioration + battery_cell_min_deterioration) / 2.0
                lost_soh = 100 - average_deterioration
                lost_wh = ((self._battery_capacity * 1000) * lost_soh) / 100
                remaining_pct = 100 - soc_display
                remaining_wh = (((self._battery_capacity * 1000) - lost_wh) * remaining_pct) / 100
                charge_power = abs((battery_current * battery_voltage))
                mins_to_complete = int((remaining_wh / charge_power) * 60)

            battery_info.update({'timestamp': int(round(bms_2105_resp.time))})
            battery_info.update({'minsToCompleteCharge': mins_to_complete})
            battery_info.update(bms_2101_resp.value)
            battery_info.update(bms_2105_resp.value)

            # Battery average temperature
            module_temps = []
            for i in range(1, 12):
                module_temps.append(battery_info["dcBatteryModuleTemp{:02d}".format(i)])
            battery_info.update({'dcBatteryAvgTemperature': round(sum(module_temps) / len(module_temps), 1)})

            # Cell voltages
            cell_voltages = (bms_2102_resp.value
                             + bms_2103_resp.value
                             + bms_2104_resp.value)
            for i, cvolt in enumerate(cell_voltages):
                key = "dcBatteryCellVoltage{:02d}".format(i + 1)
                battery_info[key] = float(cvolt)

            self._log.info("**** Got battery information ****")
        else:
            raise ValueError("Got inconsistent data for battery Status Of Health: %s%",
                             soh)

        # Return exception when empty dict
        if not bool(battery_info):
            raise ValueError("Could not get battery information")
        else:
            return battery_info

    def _query_odometer_info(self):
        self._log.info("**** Querying odometer ****")
        odometer_info = {}
        # Set header to 7C6
        self._query_command(ext_commands["CAN_HEADER_7C6"])
        # Set the CAN receive address to 7EC
        self._query_command(ext_commands["CAN_RECEIVE_ADDRESS_7EC"])
        # Sets the ID filter to 7CE
        self._query_command(ext_commands["CAN_FILTER_7CE"])
        # Query odometer
        odometer_resp = self._query_command(ext_commands["ODOMETER_22B002"])

        # Only set odometer data if present.
        # Not available when car engine is off
        odometer_info.update({'timestamp': int(round(odometer_resp.time))})
        odometer_info.update(odometer_resp.value)

        # Return exception when empty dict
        if not bool(odometer_info):
            raise ValueError("Could not get odometer information")
        else:
            return odometer_info

    def _query_vmcu_info(self):
        self._log.info("**** Querying VMCU ****")
        vmcu_info = {}
        # Set header to 7E2
        self._query_command(ext_commands["CAN_HEADER_7E2"])
        # Set the CAN receive address to 7EA
        self._query_command(ext_commands["CAN_RECEIVE_ADDRESS_7EA"])

        # VIN
        vin_resp = self._query_command(ext_commands["VIN_1A80"])
        # Add vin to vmcu info
        vmcu_info.update(vin_resp.value)

        # VMCU
        vmcu_2101_resp = self._query_command(ext_commands["VMCU_2101"])
        vmcu_info.update({'timestamp': int(round(vmcu_2101_resp.time))})
        vmcu_info.update(vmcu_2101_resp.value)

        # Return exception when empty dict
        if not bool(vmcu_info):
            raise ValueError("Could not get VMCU information")
        else:
            return vmcu_info

    def _query_tpms_info(self):
        self._log.info("**** Querying for TPMS information ****")
        tpms_info = {}
        # Set header to 7A0
        self._query_command(ext_commands["CAN_HEADER_7A0"])
        # Set the CAN receive address to 7A8
        self._query_command(ext_commands["CAN_RECEIVE_ADDRESS_7A8"])
        # Query TPMS
        tpms_22c00b_resp = self._query_command(ext_commands["TPMS_22C00B"])

        tpms_info.update({'timestamp': int(round(tpms_22c00b_resp.time))})
        tpms_info.update(tpms_22c00b_resp.value)

        # Return exception when empty dict
        if not bool(tpms_info):
            raise ValueError("Could not get TPMS information")
        else:
            return tpms_info

    def _query_external_temperature_info(self):
        self._log.info("**** Querying for external temperature ****")
        external_temperature_info = {}
        # Set header to 7E6
        self._query_command(ext_commands["CAN_HEADER_7E6"])
        # Set the CAN receive address to 7EC
        self._query_command(ext_commands["CAN_RECEIVE_ADDRESS_7EE"])
        # Query external temeprature
        ext_temp_resp = self._query_command(ext_commands["EXT_TEMP_2180"])

        # Only set temperature data if present.
        external_temperature_info.update({'timestamp': int(round(ext_temp_resp.time))})
        external_temperature_info.update(ext_temp_resp.value)  # C

        # Return exception when empty dict
        if not bool(external_temperature_info):
            raise ValueError("Could not get external temperature information")
        else:
            return external_temperature_info

    def monitor(self):
        monitor_result = {}
        self._log.info("*********** Monitoring data from IoniqEV ***********")
        try:
            # Add battery information to poll result
            battery_info = self._query_battery_info()
            monitor_result.update({"battery": battery_info})
            self._log.info("type: battery, data: %s", json.dumps(battery_info))
        except (ValueError, CanError) as err:
            self._log.warning("**** Error querying battery information: {} ****"
                              .format(err), exc_info=False)

        try:
            # Add VMCU information to poll result
            vmcu_info = self._query_vmcu_info()
            monitor_result.update({"vmcu": vmcu_info})
            self._log.info("type: vmcu, data: %s", json.dumps(vmcu_info))
        except (ValueError, CanError) as err:
            self._log.warning("**** Error querying vmcu information: {} ****"
                              .format(err), exc_info=False)

        try:
            # Add Odometer to poll result
            odometer_info = self._query_odometer_info()
            monitor_result.update({"odometer": odometer_info})
            self._log.info("type: odometer, data: %s",
                           json.dumps(odometer_info))
        except (ValueError, CanError) as err:
            self._log.warning("**** Error querying odometer: {} ****"
                              .format(err),
                              exc_info=False)

        try:
            # Add TPMS information to poll result
            tpms_info = self._query_tpms_info()
            monitor_result.update({"tpms": tpms_info})
            self._log.info("type: tpms, data: %s", json.dumps(tpms_info))
        except (ValueError, CanError) as err:
            self._log.warning("**** Error querying tpms information: {} ****"
                              .format(err),
                              exc_info=False)

        try:
            # Add external temperture information to poll result
            external_temperature_info = self._query_external_temperature_info()
            monitor_result.update({"ext_temp": external_temperature_info})
            self._log.info("type: ext_temp, data: %s",
                           json.dumps(external_temperature_info))
        except (ValueError, CanError) as err:
            self._log.warning("**** Error querying external temperature information: {} ****"
                              .format(err),
                              exc_info=False)

        self._log.info("************ %s out of 5 data line(s) generated ************",
                       len(monitor_result))
        return monitor_result

    def start(self):
        """Start the IoniqEV monitor thread."""
        self._log.info("--- Starting %s ---", self.__class__.__name__)
        self._connection = self._obd_connect()
        self._log.debug(self._connection.print_commands())
        super().start()

    def stop(self):
        super().stop()
        if self._connection is not None:
            self._connection.close()
        self._log.info("--- %s stopped ---", self.__class__.__name__)

    def check_thread(self):
        return (self._connection is not None
                and self._connection.status() == OBDStatus.CAR_CONNECTED
                and super().check_thread())
