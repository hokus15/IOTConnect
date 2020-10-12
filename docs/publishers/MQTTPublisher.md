# MQTTPublisher

It publishes the monitored data to an MQTT broker.

*Current implementation ONLY supports TLS connections, user name and password authentication, and MQTTv311 protocol*.

## Configuration

```class```: Class name implementing the publisher.

```"class": "iotconnect.publishers.mqtt.MQTTPublisher"```

```broker```: MQTT broker address.

```"broker": "test.mosquitto.org"```

```port```: MQTT broker port.

```"port": 8883```

```user```: MQTT user name.

```"user": "my-user"```

```password```: MQTT password.

```"password": "super-secret-password"```

```topic_prefix```: Topic prefix that will be used to publish information.

```qos```: QOS to be used when publishing to MQTT. Default 0.

```retain```: Retain flag to be used when publishing to MQTT. Default True.

Note that ```context``` provided to the publish method will be appended to this topic. So if the ```topic_prefix``` is ```car/sensor/my-car/``` and the context is ```state``` the topic where the data will be published will be: ```car/sensor/my-car/state```.

*Note that topic_prefix should end with forward slash ```/```.

```"topic_prefix": "car/sensor/my-car/"```

```connection_retries```: Number of times the publisher will try to connect before giving up. Keep in mind that if the publisher is not initialized in the beginning, initialization will be retried every time a monitor tries to publish.

```"connection_retries": 3```

Sample config:
```
{
    "class": "iotconnect.publishers.mqtt.MQTTPublisher",
    "broker": "test.mosquitto.org",
    "port": 8883,
    "user": "my-user",
    "password": "super-secret-password",
    "topic_prefix": "car/sensor/my-car/",
    "connection_retries": 3
 }
```
