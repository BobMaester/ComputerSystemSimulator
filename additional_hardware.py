from component import Component
from general import int_to_bool, BinaryElectric as BinElec

class PowerSupply(Component):
    def __init__(self, hasPower: bool or int = True, pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        self._power = False
        super().__init__(
            ("Power", "Ground"),
            pinValues, connections
        )
        self._power = int_to_bool(hasPower)

    @property
    def power(self) -> bool:
        return self._power

    @power.setter
    def power(self, hasPower: bool or int):
        self._power = int_to_bool(hasPower)

    def togglePower(self):
        self._power = not self._power

    def turnOn(self):
        self._power = True

    def turnOff(self):
        self._power = False

    @property
    def state(self) -> {str: any}:
        state = Component.state.__get__(self)
        state["power"] = self._power
        return state

    @state.setter
    def state(self, state: {str: any}):
        prevState = self.state
        Component.state.__set__(self, state)
        try:
            powerState = state["power"]
        except KeyError:
            raise Component.StateError("power", state)
        try:
            self.power = powerState
        except Exception as error:
            self.state = prevState
            raise error

    @state.deleter
    def state(self):
        Component.state.__delete__(self)
        self.makePinsActive((1, 2))
        self._power = False

    def response(self):
        self.setPinsStates((1, 2), ((self._power, True), (False, True)))

class Button(Component):
    def __init__(self, isPressed: bool or int = False, pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        self._pressed = False
        super().__init__(4, pinValues, connections)
        self._pressed = int_to_bool(isPressed)

    @property
    def pressed(self) -> bool:
        return self._pressed

    @pressed.setter
    def pressed(self, isPressed: bool or int):
        self._pressed = int_to_bool(isPressed)

    def togglePress(self):
        self._pressed = not self._pressed

    def press(self):
        self._pressed = True

    def unpress(self):
        self._pressed = False

    @property
    def state(self) -> {str: any}:
        state = Component.state.__get__(self)
        state["pressed"] = self._pressed
        return state

    @state.setter
    def state(self, state: {str: any}):
        prevState = self.state
        Component.state.__set__(self, state)
        try:
            pressedState = state["pressed"]
        except KeyError:
            raise Component.StateError("pressed", state)
        try:
            self.pressed = pressedState
        except Exception as error:
            self.state = prevState
            raise error

    @state.deleter
    def state(self):
        Component.state.__delete__(self)
        self._pressed = False

    def response(self):
        pin1, pin2, pin3, pin4 = self.getPinsStates(slice(None))
        side1 = BinElec.combine(pin1, pin2)
        side2 = BinElec.combine(pin3, pin4)
        if self._pressed:
            side1 = side2 = BinElec.combine(side1, side2)
        self.setPinsStates((1, 2), side1)
        self.setPinsStates((3, 4), side2)

class Clock(Component):
    def __init__(self, output: bool or int = False, pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        self._output = False
        super().__init__(
            ("N/C", "GND", "VCC", "Output"),
            pinValues, connections
        )
        self._output = int_to_bool(output)

    @property
    def output(self) -> bool:
        return self._output

    @output.setter
    def output(self, output: bool):
        self._output = int_to_bool(output)

    def step(self):
        self._output = not self._output

    @property
    def state(self) -> {str: any}:
        state = Component.state.__get__(self)
        state["output"] = self._output
        return state

    @state.setter
    def state(self, state: {str: any}):
        prevState = self.state
        Component.state.__set__(self, state)
        try:
            outputState = state["output"]
        except KeyError:
            raise Component.StateError("output", state)
        try:
            self.output = outputState
        except Exception as error:
            self.state = prevState
            raise error

    @state.deleter
    def state(self):
        Component.state.__delete__(self)
        self._output = False

    def response(self):
        high, low = self.getPinsStates(("VCC", "GND"))
        self.makePinsPassive(slice(None))
        if self._output:
            self.setPinState("Output", high)
        else:
            self.setPinState("Output", low)

class QuadNANDGate(Component):
    def __init__(self, pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        super().__init__(
            (
                "A1", "B1", "Y1", "A2", "B2", "Y2", "GND",
                "Y3", "A3", "B3", "Y4", "A4", "B4", "VCC"
            ),
            pinValues, connections
        )

    def response(self):
        high, low = self.getPinsStates(("VCC", "GND"))
        self.makePinsPassive(slice(None))
        for gate in range(1, 5):
            if self.getPin(f"A{gate}") and self.getPin(f"B{gate}"):
                self.setPinState(f"Y{gate}", low)
            else:
                self.setPinState(f"Y{gate}", high)

class Resistor(Component):
    def __init__(self, pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        super().__init__(2, pinValues, connections)

    def response(self):
        pin1, pin2 = self.getPinsStates(slice(None))
        if pin1[1] != pin2[1]:
            if pin1[1]:
                self.setPinState(2, pin1)
            else:
                self.setPinState(1, pin2)
