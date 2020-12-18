# IOTConnect
[![Build Status](https://img.shields.io/travis/hokus15/IOTConnect?logo=travis)](https://travis-ci.com/github/hokus15/IOTConnect) [![Code quality](https://app.codacy.com/project/badge/Grade/913d06cf965042e0808962a9ae238792)](https://www.codacy.com/manual/hokus15/IOTConnect/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hokus15/IOTConnect&amp;utm_campaign=Badge_Grade) ![License](https://img.shields.io/github/license/hokus15/IOTConnect) ![GitHub last commit](https://img.shields.io/github/last-commit/hokus15/IOTConnect?logo=github) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/hokus15/IOTConnect?logo=github)

Extensible Internet Of Things integration service written in Python that can be run in a Raspberry Pi Zero W.

It monitors the data from all configured monitors and publish the gathered data to all configured publishers.

This repo is an evolution and an extensible version of my other repo [Pioniq](https://github.com/hokus15/pioniq).

## Features
-   **Connectivity:** Connect anything that can be monitored using python with your IOT hub using built in MQTTPublisher.
-   **Customization:** More systems and information can be monitored and published developing additional Monitors and Publishers.
-   **Open-source:** You are welcome to improve the service by fixing bugs, adding functionality or developing your own Monitors and Publishers and make a pull request.

## Credits
All this work has been possible by putting together different pieces like:

-   How To Article from [sochack.eu](https://tutorial.sochack.eu/en/how-to-soc/)
-   [Ingesting GPS Data From Raspberry PI Zero Wireless With a USB GPS Device](https://dzone.com/articles/iot-ingesting-gps-data-from-raspberry-pi-zero-wire)
-   [python-OBD](https://github.com/brendan-w/python-OBD/tree/master/obd)
-   [EVNotiPi](https://github.com/EVNotify/EVNotiPi)
-   [OBD-PIDs-for-HKMC-EVs](https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs)
-   [SoulEVSpy](https://github.com/langemand/SoulEVSpy)
-   [Open Vehicles](https://github.com/openvehicles/)
-   and of course lot of patience and [Google](https://www.google.com/)

## Informal disclaimer
I'm a noob in python programming and I'm not a Linux expert so I'm pretty sure that the source code may be far from efficient, so don't be too hard with me if you find that I'm not following best practices neither doing things in the most optimal way. If you find that anything that can be improved (I'm sure it is), just raise a PR with your improvements or contact me.

## Disclaimer
IOTConnect (“THE SOFTWARE”) IS PROVIDED AS IS. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHOR MAKE NO WARRANTIES AS TO PERFORMANCE OR FITNESS FOR A PARTICULAR PURPOSE, OR ANY OTHER WARRANTIES WHETHER EXPRESSED OR IMPLIED. NO ORAL OR WRITTEN COMMUNICATION FROM OR INFORMATION PROVIDED BY THE AUTHORS SHALL CREATE A WARRANTY. UNDER NO CIRCUMSTANCES SHALL THE AUTHORS BE LIABLE FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES RESULTING FROM THE USE, MISUSE, OR INABILITY TO USE THE SOFTWARE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. THESE EXCLUSIONS AND LIMITATIONS MAY NOT APPLY IN ALL JURISDICTIONS. YOU MAY HAVE ADDITIONAL RIGHTS AND SOME OF THESE LIMITATIONS MAY NOT APPLY TO YOU. THIS SOFTWARE IS ONLY INTENDED FOR SCIENTIFIC USAGE.

## License
[Apache-2.0 license](https://github.com/hokus15/IOTConnect/blob/master/LICENSE)
