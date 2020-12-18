# NoopMonitor

This is the simplest of the monitors and it monitors nothing.

## Configuration

```class```: Class name implementing the monitor.

```"class": "iotconnect.monitors.noop.NoopMonitor"```

```interval```: Interval in seconds to execute the monitorization.

```"interval": 10```

Sample config:
```
{
    "class": "iotconnect.monitors.noop.NoopMonitor",
    "interval": 10
}
```
