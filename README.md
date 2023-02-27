# SLICE-QTC

A package to communicate with a VESCENT Slice-QTC temperature controller.

This package wraps the serial API of the Vescent Slice temperature
controller [Vescent Slice temperature controller](https://vescent.com/de/slice-qtc-four-channel-temperature-controller.html)
to a python class for convenient communication.

All serial commands are implemented as class properties.


**Warning**: The software currently only works with firmware version 2.22. Earlier firmware versions are not supported!
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
This is NOT an official package provided by Vescent Photonics.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.