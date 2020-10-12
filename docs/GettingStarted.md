# Getting started

IOTConnect is an extensible framework written in Python that allows you to monitor anything and publishes the monitored conditions to different publishers.

Both Monitors and Publishers can be extended to fit your needs by implementing Monitor and Publisher classes respectively.

## Suggested hardware

We will need a few things to get started with installing IOTConnect. Raspberry Pi Zero W can be a good and cheap staring point.

-   Raspberry PI Zero W + Power supply.
-   MicroSD card. Ideally get one that is Application Class 2 as they handle small I/O much more consistently than cards not optimized to host applications. The size depends on the usage you may want to give to IOTConnect.
-  SD Card reader. This is already part of most laptops, but you can purchase a standalone USB adapter if you don’t have one. The brand doesn’t matter, just pick the cheapest.

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

Configuration is located under the ```iotconnect``` folder and it's a json file that must be named ```iotconnect.config.json```.

It consist in an array of publishers and an array of monitors. Monitored conditions from monitors are published to ALL configured publishers.

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
