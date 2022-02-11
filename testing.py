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
        print(f"TestComponent.response({self})")

class Component_test(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
