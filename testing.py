from simulator import Simulator
from user_interface import UserInterface
from instruction_set_65C02.instructions import instructions
from instruction_set_65C02.operations import Operations
from instruction_set_65C02.addressing_modes import AddressingModes
from processor import Processor
from memory import Memory, SpecificMemory, ReadOnlyMemory as ROM, RandomAccessMemory as RAM
from additional_hardware import PowerSupply, Button, Clock, QuadNANDGate as NAND, Resistor
from assembler import Assembler
from instruction_set import InstructionSet, AddressingMode, Operation
from component import Component, Node, Connection, Pin, Wire
from general import intToBool, bytesToTuple, sliceToTuple, BinaryElectric as BinElec
import random
import unittest

class RandomData:
    @staticmethod
    def string(length: int = 1) -> str:
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        string = ""
        for character in range(length):
            string += random.choice(characters)
        return string

    @staticmethod
    def float(lower: int = 0, upper: int = 1) -> float:
        integer = random.randint(lower, upper)
        if integer == upper:
            return integer + 0.0
        return integer + random.random()

    @staticmethod
    def slice(minimum: int, maximum: int) -> slice:
        start = random.randint(minimum, maximum)
        stop = start
        while stop == start:
            stop = random.randint(minimum, maximum)
        spread = stop - start
        if spread > 0:
            step = random.randint(1, spread)
        else:
            step = random.randint(spread, -1)
        return slice(start, stop, step)

    @staticmethod
    def state() -> [int, int]:
        return random.randint(0, 1), random.randint(0, 1)

    @staticmethod
    def connection(pinCount: int, states: [[bool or int, bool or int]] = None) -> Wire:
        if states is None:
            states = list()
            for state in range(pinCount):
                states.append(RandomData.state())
        wire = Wire()
        for pin in range(pinCount):
            if random.randint(0, 1) == 0:
                wire = Wire((wire,))
            wire.connect(Pin(f"randomPin{pin}", RandomData.state()))
        return wire

class NullComponent(Component):
    def response(self):
        print(f"TestComponent.response({self})")


# general.py

class Test_intToBool(unittest.TestCase):
    def test_exhaustiveBooleanData(self):
        returnedValue = intToBool(True)
        self.assertTrue(returnedValue)
        self.assertIsInstance(returnedValue, bool)
        returnedValue = intToBool(False)
        self.assertFalse(returnedValue)
        self.assertIsInstance(returnedValue, bool)

    def test_exhaustiveIntegerValidData(self):
        returnedValue = intToBool(1)
        self.assertTrue(returnedValue)
        self.assertIsInstance(returnedValue, bool)
        returnedValue = intToBool(0)
        self.assertFalse(returnedValue)
        self.assertIsInstance(returnedValue, bool)

    def test_integerInvalidData(self):
        for test in range(10):
            testData = 0
            while testData == 1 or testData == 0:
                testData = random.randint(-1024, 1024)
            self.assertRaises(ValueError, intToBool, testData)

    def test_invalidType(self):
        for testData in "1", "0", 1.0, 0.0, bytes([1]), bytes([0]):
            self.assertRaises(TypeError, intToBool, testData)

    def test_randomInvalidType(self):
        for test in range(10):
            for testData in (random.randbytes(random.randint(0, 16)),
                             RandomData.float(-1024, 1024),
                             RandomData.string(random.randint(0, 1024))):
                self.assertRaises(TypeError, intToBool, testData)

class Test_bytesToTuple(unittest.TestCase):
    @staticmethod
    def inverseFunction(returnedValue: [bool,]):
        total = 0
        for bit in range(len(returnedValue)):
            total += returnedValue[bit] * 2 ** bit
        return total.to_bytes((len(returnedValue) + 1) // 8, "big")

    def bytesToTuple_test(self, testData: bytes):
        returnedValue = bytesToTuple(testData)
        self.assertEqual(testData, Test_bytesToTuple.inverseFunction(returnedValue))
        self.assertIsInstance(returnedValue, tuple)
        for x in returnedValue:
            self.assertIsInstance(x, bool)

    def test_expectedData(self):
        for test in range(10):
            self.bytesToTuple_test(random.randbytes(random.randint(1, 16)))

    def test_lowExtremeData(self):
        self.bytesToTuple_test(bytes())

    def test_highExtremeData(self):
        for test in range(10):
            self.bytesToTuple_test(random.randbytes(random.randint(128, 256)))

    def test_invalidType(self):
        for test in range(10):
            for testData in (random.randint(-1024, 1024),
                             RandomData.float(-1024, 1024),
                             RandomData.string(random.randint(0, 1024))):
                self.assertRaises(TypeError, bytesToTuple, testData)

class Test_BinElec(unittest.TestCase):
    def test_validateState_exhaustiveBooleanData(self):
        for activity in False, True:
            for value in False, True:
                returnedValue = BinElec.validateState([value, activity])
                self.assertEqual((value, activity), returnedValue)
                self.assertIsInstance(returnedValue, tuple)
                for x in returnedValue:
                    self.assertIsInstance(x, bool)

    def test_validateState_exhaustiveIntegerValidData(self):
        expected = (False, False), (True, False), (False, True), (True, True)
        for activity in range(2):
            for value in range(2):
                returnedValue = BinElec.validateState((value, activity))
                self.assertEqual(expected[2 * activity + value], returnedValue)
                self.assertIsInstance(returnedValue, tuple)
                for x in returnedValue:
                    self.assertIsInstance(x, bool)

    def test_validateState_invalidLength(self):
        for test in range(10):
            testData = list()
            for item in range(random.randint(3, 1024)):
                testData.append(bool(random.randint(0, 1024) // 2))
            self.assertRaises(ValueError, BinElec.validateState, testData)

    def test_ValidState_success(self):
        for activity in False, True:
            for value in False, True:
                self.assertTrue(BinElec.validState((value, activity)))

    def test_combine_exhaustiveValidData(self):
        inputs = ((0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1),
                  (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1),
                  (1, 0, 0, 0), (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 1, 1),
                  (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 0), (1, 1, 1, 1))
        expectedOutcomes = ((False, False), (False, True), (True, False), (True, True),
                            (False, True),  (False, True), (False, True), (True, True),
                            (True, False),  (False, True), (True, False), (True, True),
                            (True, True),   (True, True),  (True, True),  (True, True))
        for index in range(len(inputs)):
            v1, a1, v2, a2 = inputs[index]
            returnedValue = BinElec.combine((v1, a1), (v2, a2))
            self.assertEqual(expectedOutcomes[index], returnedValue)
            self.assertIsInstance(returnedValue, tuple)
            for x in returnedValue:
                self.assertIsInstance(x, bool)


# component.py

class Test_Pin(unittest.TestCase):
    def test_stateRestorationOnFailedSet(self):
        testPin = Pin("testPin")
        for test in range(10):
            state = RandomData.state()
            testPin.state = state
            for testData in (random.randint(-1024, 1024),
                             random.randbytes(random.randint(0, 16)),
                             RandomData.float(-1024, 1024),
                             RandomData.string(random.randint(0, 1024))):
                try:
                    testPin.state = testData
                except:
                    pass
                self.assertEqual(state, testPin.state)

    def test_retrieveState(self):
        for test in range(10):
            pinCount = random.randint(0, 16)
            states = list()
            for state in range(pinCount):
                states.append(RandomData.state())
            state = RandomData.state()
            testPin = Pin("testPin", state, RandomData.connection(pinCount, states))
            returnedValue = testPin.retrieveState()
            state = False, False
            for x in states:
                state = BinElec.combine(state, x)
            print("expectedState:", state)
            self.assertEqual(state, returnedValue)

    def test_retrieveState_excludedFromSelf(self):
        for test in range(10):
            testPin = Pin("testPin", connection = RandomData.connection(random.randint(0, 16)))
            self.assertRaises(Node.ExcludedNodeError, testPin.retrieveState, [testPin,])

    def test_replaceConnection(self):
        testPin = Pin("testPin", connection = RandomData.connection(random.randint(0, 16)))
        for test in range(10):
            testPin.connection = RandomData.connection(random.randint(0, 16))

    def test_destructor(self):
        testPin1 = Pin("testPin")
        testPin2 = Pin("testPin")
        testPin1.connection = testPin2
        self.assertEqual(testPin1.connection.node, testPin2)
        del testPin2
        self.assertIsNone(testPin1.connection)

class Test_Wire(unittest.TestCase):
    def test_getConnection(self):
        pass

class Test_Connection(unittest.TestCase):
    pass

class Test_Component(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
