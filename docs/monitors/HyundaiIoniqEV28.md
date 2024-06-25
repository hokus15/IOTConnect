# Hyundai Ioniq EV (28Kwh)

Reads data from the OBDII Bluetooth Dongle.

## Configuration

`class`: Class name implementing the monitor.

`"class": "iotconnect.monitors.ioniqev.IoniqEVMonitor"`

`port`: The UNIX device file of the adapter.

`"port": "/dev/rfcomm0"`

`baudrate`: The baudrate to use for the connection e.g. 9600, 19200, 38400, ...

`"baudrate": 9600`

`fast`: Set to "True" to optimize the commands sent to the adapter.

`"fast": "False"`

`timeout`: The connection timeout in seconds.

`"timeout": 30`

`interval`: The interval in seconds to read new data.

`"interval": 30`

Sample config:

```
{
  "class": "iotconnect.monitors.ioniqev.IoniqEVMonitor",
  "port": "/dev/rfcomm0",
  "baudrate": 9600,
  "fast": "False",
  "timeout": 30,
  "interval": 10
 }
```
