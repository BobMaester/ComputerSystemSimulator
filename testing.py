from simulator import Simulator
from user_interface import UserInterface
from instruction_set_65C02.instructions import instructions
from instruction_set_65C02.operations import Operations
from instruction_set_65C02.addressing_modes import AddressingModes
from processor import Processor
from memory import Memory, SpecificMemory, RandomAccessMemory, ReadOnlyMemory
from additional_hardware import PowerSupply, Clock, QuadNANDGate, Button, Resistor
from assembler import Assembler
from instruction_set import InstructionSet, AddressingMode, Operation
from component import Component, Node, Connection, Pin, Wire
from general import int_to_bool, bytes_to_tuple, slice_to_tuple, BinaryElectric
import unittest
import random

class TestComponent(Component):
    def response(self):
        pass

    def pinSelect(self, pin: int or str) -> Pin:
        return self.pinSelect(pin)

    def pinsSelect(self, pins: [int or str,] or slice) -> [Pin,]:
        return self.pinsSelect(pins)

    def makePinActive(self, pin: int or str):
        self._makePinActive(pin)

    def makePinPassive(self, pin: int or str):
        self._makePinPassive(pin)

    def setPinActivity(self, pin: int or str, activity: bool or int):
        self._setPinActivity(pin, activity)

    def makePinsActive(self, pins: [int or str,] or slice):
        self._makePinsActive(pins)

    def makePinsPassive(self, pins: [int or str,] or slice):
        self._makePinsPassive(pins)

    def setPinsActivity(self, pins: [int or str,] or slice, activity: bool or int):
        self._setPinsActivity(pins, activity)

    def setPinsActivities(self, pins: [int or str,] or slice, activities: [bool or int,] or bytes):
        self._setPinsActivities(pins, activities)

    def setPinState(self, pin: int or str, state: [bool or int, bool or int]):
        self._setPinState(pin, state)

    def setPinsStates(self, pins: [int or str,] or slice, states: [[bool or int, bool or int],]):
        self._setPinsStates(pins, states)

class Component_test(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
