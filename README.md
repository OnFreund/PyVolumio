# PyVolumio

A python interface control [Volumio](https://volumio.org/).

## Installation

You can install pyvolumio from [PyPI](https://pypi.org/project/pyvolumio/):

    pip3 install pyvolumio

Python 3.7 and above are supported.


## How to use

```python
from pyvolumio import Volumio
v = Volumio("<host>", <port>)
# you can also pass in your own session
v = Volumio("<host>", <port>, <session>)

info = await v.get_system_info()
state = await v.get_state()

await v.play()
await v.pause()
await v.stop()
await v.volume_up()
...
```