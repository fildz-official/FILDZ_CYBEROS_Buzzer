# FILDZ CYBEROS Buzzer Library

Fully asynchronous buzzer library for CYBEROS.

## Features

* Completely asynchronous.
* Supports RTTTL (Ring Tone Text Transfer Language).
* Adjustable volume.

## Setup

1. Download and extract .zip file contents to "fildz_buzzer" folder.
2. Upload "fildz_buzzer" folder to your MicroPython powered device.

## Usage

```Python
from machine import Pin, PWM
import uasyncio as asyncio
import fildz_cyberos as cyberos
from fildz_buzzer import Buzzer


async def main():
    await cyberos.init()
    bzr = Buzzer(PWM(Pin(12), freq=100, duty=0))
    await bzr.play(index=0)  # Will play "on" from "TONES" list in "tones.py".
    await bzr.play(name='off')
    await cyberos.run_forever()

asyncio.run(main())
```

## Documentation

The documentation for this library is currently a work in progress. It will be available soon to provide detailed explanations of the library's API, usage examples, and best practices.

## Contributing

FILDZ CYBEROS is an open-source project that thrives on community contributions. We welcome developers to contribute to the project by following the MIT license guidelines. Feel free to submit pull requests, report issues, or suggest enhancements to help us improve the project further.

## Acknowledgment 

We are immensely thankful to the [MicroPython](https://github.com/micropython/micropython) community for developing and maintaining this incredible open-source project. Their dedication and hard work have provided us with a powerful and versatile platform to build upon.
