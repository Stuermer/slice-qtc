from __future__ import annotations

import logging

import serial
from serial import Serial

logger = logging.getLogger(__name__)


def send_command(ser: Serial | None, command: str, expected_result_type=None):
    logger.info(f"{' COMMAND START ' :*^40}")
    command = (command + "\r\n").encode("ascii")
    logger.info(f"write: {command}")
    if ser is None:
        reply = None
    else:
        ser.write(command)
        reply = ser.readline()
        logger.info(f"reply: {reply}")
        if expected_result_type is not None:
            try:
                reply = expected_result_type(reply)
            except TypeError:
                logger.info(f"Couldn't convert {reply} to {expected_result_type}")
    logger.info(f"{' COMMAND END ' :*^40}\n")
    return reply


class Channel:
    def __init__(self, number, ser=None):
        self.number = number
        self.ser = ser

    def _send_command(self, command, arg=None, expected_result_type=float):
        command = f"{command} {self.number} {'' if arg is None else arg}"
        return send_command(self.ser, command, expected_result_type)

    @property
    def TempSet(self) -> float:
        return self._send_command(f"TempSet?")

    @TempSet.setter
    def TempSet(self, value: float):
        self._send_command(f"TempSet", value)

    @property
    def Temp(self) -> float:
        return self._send_command(f"Temp?")

    @property
    def TError(self):
        return self._send_command(f"TError?")

    @property
    def TempMin(self) -> float:
        return self._send_command("TempMin?")

    @TempMin.setter
    def TempMin(self, value: float):
        self._send_command("TempMin", value)

    @property
    def TempMax(self) -> float:
        return self._send_command("TempMax?")

    @TempMax.setter
    def TempMax(self, value: float):
        self._send_command("TempMax", value)

    @property
    def Bipolar(self) -> int:
        return self._send_command("Bipolar?", expected_result_type=int)

    @Bipolar.setter
    def Bipolar(self, value: int):
        self._send_command("Bipolar", value, expected_result_type=int)

    @property
    def MaxCurr(self) -> float:
        return self._send_command("MaxCurr?")

    @MaxCurr.setter
    def MaxCurr(self, value: float):
        self._send_command("MaxCurr", value)

    @property
    def Current(self) -> float:
        return self._send_command("Current?")

    @Current.setter
    def Current(self, value: float):
        self._send_command("Currset", value)

    @property
    def MaxPwr(self) -> float:
        return self._send_command("MaxPwr?")

    @MaxPwr.setter
    def MaxPwr(self, value: float):
        self._send_command("MaxPwr", value)

    @property
    def Power(self) -> float:
        return self._send_command("Power?")

    @property
    def CVolt(self):
        return self._send_command("CVolt")

    @property
    def Beta(self) -> float:
        return self._send_command("Beta?")

    @Beta.setter
    def Beta(self, value: float):
        self._send_command("Beta", value)

    @property
    def RefTemp(self) -> float:
        return self._send_command("RefTemp?")

    @RefTemp.setter
    def RefTemp(self, value: float):
        self._send_command("RefTemp", value)

    @property
    def RefRes(self) -> float:
        return self._send_command("RefRes?")

    @RefRes.setter
    def RefRes(self, value: float):
        self._send_command("RefRes", value)

    @property
    def TCoefA(self) -> float:
        return self._send_command("TCoefA?")

    @TCoefA.setter
    def TCoefA(self, value: float):
        self._send_command("TCoefA", value)

    @property
    def TCoefB(self) -> float:
        return self._send_command("TCoefB?")

    @TCoefB.setter
    def TCoefB(self, value: float):
        self._send_command("TCoefB", value)

    @property
    def TCoefC(self) -> float:
        return self._send_command("TCoefC?")

    @TCoefC.setter
    def TCoefC(self, value: float):
        self._send_command("TCoefC", value)

    def TEMPLUT(self):
        self._send_command("TEMPLUT")

    @property
    def Control(self) -> int:
        return self._send_command("Control?", expected_result_type=int)

    @Control.setter
    def Control(self, value: int):
        self._send_command("Control", arg=value, expected_result_type=int)

    @property
    def PGain(self) -> float:
        return self._send_command("PGain?")

    @PGain.setter
    def PGain(self, value: float):
        self._send_command("PGain", value)

    @property
    def Integ(self) -> float:
        return self._send_command("Integ?")

    @Integ.setter
    def Integ(self, value: float):
        self._send_command("Integ", value)

    @property
    def Deriv(self) -> float:
        return self._send_command("Deriv?")

    @Deriv.setter
    def Deriv(self, value: float):
        self._send_command("Deriv", value)

    @property
    def Slew(self) -> float:
        return self._send_command("Slew?")

    @Slew.setter
    def Slew(self, value: float):
        self._send_command("Slew", value)

    @property
    def DerivEn(self) -> int:
        return self._send_command("DerivEn?", expected_result_type=int)

    @DerivEn.setter
    def DerivEn(self, value: int):
        self._send_command("DerivEn", value, expected_result_type=int)

    @property
    def PGainEn(self) -> int:
        return self._send_command("PGainEn?", expected_result_type=int)

    @PGainEn.setter
    def PGainEn(self, value: int):
        self._send_command("PGainEn", value, expected_result_type=int)

    @property
    def IntegEn(self) -> int:
        return self._send_command("IntegEn?", expected_result_type=int)

    @IntegEn.setter
    def IntegEn(self, value: int):
        self._send_command("IntegEn", value, expected_result_type=int)

    @property
    def SlewEn(self) -> int:
        return self._send_command("SlewEn?", expected_result_type=int)

    @SlewEn.setter
    def SlewEn(self, value: int):
        self._send_command("SlewEn", value, expected_result_type=int)


class Slice:
    def __init__(self, port='/dev/vescent', debug=False):
        self.debug = debug
        self.port = port

        self.ser = None
        self._connect()

        self.ch1 = Channel(1, self.ser)
        self.ch2 = Channel(2, self.ser)
        self.ch3 = Channel(3, self.ser)
        self.ch4 = Channel(4, self.ser)

    def _connect(self):
        if not self.debug:
            self.ser = serial.Serial(self.port)
        else:
            logger.info("DEBUG MODE  -  no commands send to device")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ser is not None:
            try:
                self.ser.close()
            except serial.SerialException:
                pass

    def __del__(self):
        if self.ser is not None:
            try:
                self.ser.close()
            except serial.SerialException:
                pass

    def _send_command(self, command, expected_result_type):
        return send_command(self.ser, command, expected_result_type)

    @property
    def version(self) -> float:
        return self._send_command("#VERSION", float)

    def save(self):
        return self._send_command("Save", str)

    @property
    def Output1(self) -> str:
        return self._send_command("Output1?", str)

    @Output1.setter
    def Output1(self, value: str):
        self._send_command(f"Output1 {value}", str)

    @property
    def Output2(self) -> str:
        return self._send_command("Output1?", str)

    @Output2.setter
    def Output2(self, value: str):
        self._send_command(f"Output2 {value}", str)

    @property
    def InputA(self) -> str:
        return self._send_command("InputA?", str)

    @InputA.setter
    def InputA(self, value: str):
        self._send_command(f"InputA {value}", str)

    @property
    def InputB(self) -> str:
        return self._send_command("InputB?", str)

    @InputB.setter
    def InputB(self, value: str):
        self._send_command(f"InputB {value}", str)


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    qtc = Slice('/dev/ttyACM0')
    for i in [1, 2, 3, 4]:
        channel = getattr(qtc, f"ch{i}")
        print(f"Channel {i} Temperature: {channel.Temp:.4f}")
