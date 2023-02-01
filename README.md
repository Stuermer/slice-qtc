# SLICE-QTC

A package to communicate with a VESCENT Slice-QTC temperature controller.

This package wraps the serial API of the Vescent Slice temperature
controller [Vescent Slice temperature controller](https://vescent.com/de/slice-qtc-four-channel-temperature-controller.html)
to a python class for convenient communication.

All serial commands are implemented as class properties.

## Usage

```python
import slice

qtc = slice.Slice()

# read current temperature of channel 1
print(qtc.ch1.Temp)

# change set point of channel 2 
qtc.ch2.SetTemp = 19.040
```

## Installation

The package can be installed via pip:

```bash
pip install slice-qtc 
```

## Disclaimer
