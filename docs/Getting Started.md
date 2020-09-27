# Getting started

IOTConnect is an extensible framework written in Python that allows you to monitor anything and publishes the monitored conditions to different publishers.

Both Monitors and Publishers can be extended to fit your needs by implementing Monitor and Publisher classes respectively.

## Installation

Clone the Github repo:
```
sudo git clone https://github.com/hokus15/IOTConnect.git /opt/IOTConnect
```

Make pi user the owner of `/opt/IOTConnect` folder:
```
sudo chown -R pi /opt/IOTConnect
```

Install dependencies:
```
cd /opt/IOTConnect
pip3 install -r requirements.txt
```

### Run as a service

To run the `IOTConnect` as a service:

```
sudo systemctl link /opt/IOTConnect/iotconnect.service
sudo systemctl enable iotconnect.service
sudo systemctl daemon-reload
```

## Configuration

Configuration is located under the ```iotconnect``` folder and it's a json file that must be called ```iotconnect.config.json```.

It consist in an array of publishers and an array of monitors. All monitored conditions are published to ALL configured publishers.

Every publisher in the array MUST have at least a ```class``` property specifying a valid class name.

Every monitor in the array MUST have at least a ```class``` property specifying a valid class name and an ```interval``` property specifying the frequency (in seconds) that the monitor will be executed.

The service MUST have at least one publisher and on monitor to work.

Very simple dummy config file:

```
{
    "publishers":[
        {
            "class": "iotconnect.publishers.noop.NoopPublisher"
         }
    ],
    "monitors":[
        {
            "class": "iotconnect.monitors.noop.NoopMonitor",
            "interval": 10
        }
    ]
}
```

## Built-in publishers

Publishers are classes that publish the monitored conditions to any destination. i.e: MQTT broker, REST service, log file,...

IOTConnect comes with the following built-in publishers:

### NoopPublisher

This is the simplest of the publishers and it does nothing. It's simply there as a base demonstration to implement new publishers.

#### Configuration

```class```: Class name implementing the publisher.

```"class": "iotconnect.publishers.noop.NoopPublisher"```

Sample config:
```
{
    "class": "iotconnect.publishers.noop.NoopPublisher"
 }
```

### MQTTPublisher

It publishes the monitored data to an MQTT broker.

*Current implementation ONLY supports TLS connections, user name and password authentication, and MQTTv311 protocol*.

#### Configuration

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

## Built in monitors

TODO
