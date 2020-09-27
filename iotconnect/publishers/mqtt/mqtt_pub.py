import time
import uuid
import json
import logging
import paho.mqtt.client as mqtt
from iotconnect.publisher import Publisher


class MQTTPublisher(Publisher):
    """Class implementing a MQTT publisher."""

    def __init__(self, config):
        Publisher.__init__(self, config)
        self._log = logging.getLogger('iotconnect.publishers.' + self.__class__.__name__)
        self._broker = self._config['broker']
        self._port = self._config['port']
        self._user = self._config['user']
        self._password = self._config['password']
        self._topic_prefix = self._config['topic_prefix']
        self._max_connection_retries = self._config['connection_retries']
        self._connection_retries = 0

    def initialize(self):
        if not self._initialized:
            self._log.info("--- Initializing %s ... ---", self.__class__.__name__)
            mqtt.Client.connected_flag = False

            # Create MQTT client
            self._mqtt_client = mqtt.Client(client_id="IOTConnect-" + str(uuid.uuid4()),
                                            protocol=mqtt.MQTTv311,
                                            transport="tcp")

            # Assign callback functions
            self._mqtt_client.on_publish = self._on_publish
            self._mqtt_client.on_connect = self._on_connect

            # Set tls
            self._mqtt_client.tls_set()
            # Set user and password
            self._mqtt_client.username_pw_set(self._user, self._password)
            # Enable MQTT logger
            self._mqtt_client.enable_logger(self._log)
            # Start loop to process callbacks
            self._mqtt_client.loop_start()
            # Conect to MQTT server
            while not self._mqtt_client.connected_flag and self._connection_retries < self._max_connection_retries:
                self._log.debug("Trying to connect to MQTT server (%s)...", self._connection_retries + 1)
                self._mqtt_client.connect(self._broker, self._port)
                self._connection_retries += 1
                time.sleep(5)

            if self._connection_retries >= self._max_connection_retries:
                self._log.error("Could not connect to MQTT. Max attempts (%s) exceeded.", self._max_connection_retries)
                self._log.info("--- %s could not be initialized ---", self.__class__.__name__)
                raise Exception("Could not connect to MQTT. Max attempts ({}) exceeded."
                                .format(self._max_connection_retries))
            else:
                self._connection_retries = 0
                self._initialized = True
                self._log.info("--- %s initialized ---", self.__class__.__name__)

    def _on_publish(self, client, userdata, mid):
        """MQTT function for on_publish callback."""
        self._log.debug("Publish message id: {}".format(mid))

    def _on_connect(self, client, userdata, flags, rc):
        """MQTT function for on_connect callback."""
        if rc == 0:
            client.connected_flag = True  # set flag
            self._log.info("Successfully connected to MQTT broker")
        else:
            self._log.debug("Could not connect to MQTT broker. Return code: %s", rc)

    def publish(self, context, data):
        self._log.info("context: '%s', payload: '%s'",
                       self._topic_prefix + context,
                       json.dumps(data))
        result = self._mqtt_client.publish(topic=self._topic_prefix + context,
                                           payload=json.dumps(data),
                                           qos=0,
                                           retain=True)
        result.wait_for_publish()
        if (result.rc == 0):
            self._log.debug("Message successfully published: %s", str(result))
        else:
            self._log.error("Error publishing message: %s", str(result))

    def close(self):
        self._log.info("--- Closing %s ---", self.__class__.__name__)
        self._log.info("Disconnecting from MQTT broker")
        self._mqtt_client.loop_stop()
        self._mqtt_client.disconnect()
        self._log.info("--- %s closed ---", self.__class__.__name__)
