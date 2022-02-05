from instruction_set import InstructionSet
from component import Component
from general import slice_to_tuple

class Processor(Component):
    class InvalidRegisterError(Exception):
        pass

    def __init__(self, instructionSet: InstructionSet, registerValues: [bytes,] or bytes = tuple(), pinValues: [bool or int,] or bytes = tuple(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        if not isinstance(instructionSet, InstructionSet):
            raise TypeError(f"A processor's instruction set must inherit from InstructionSet ({instructionSet} does not)")
        self._instructionSet = InstructionSet
        self._registers = {
            "PC"  : bytes(2),
            "MAR" : bytes(2),
            "MBR" : bytes(1),
            "IR"  : bytes(1),
            "P"   : bytes(1),
            "TCU" : bytes(1),
            "S"   : bytes(1),
            "A"   : bytes(1),
            "X"   : bytes(1),
            "Y"   : bytes(1)
        }
        super().__init__(
            (
                "VPB",  "RDY",  "PHI1O", "IRQB",  "MLB",
                "NMIB", "SYNC", "VDD",   "A0",    "A1",
                "A2",   "A3",   "A4",    "A5",    "A6",
                "A7",   "A8",   "A9",    "A10",   "A11",
                "VSS",  "A12",  "A13",   "A14",   "A15",
                "D7",   "D6",   "D5",    "D4",    "D3",
                "D2",   "D1",   "D0",    "RWB",   "NC",
                "BE",   "PHI2", "SOB",   "PHI2O", "RESB"
            ),
            pinValues, connections
        )
        if registerValues:
            self.setRegisters(slice(None), registerValues)

    @property
    def registers(self) -> [str,]:
        return tuple(self._registers.keys())

    def registerSelect(self, register: str or int) -> str:
        if isinstance(register, int):
            return self.registers[register]
        else:
            register = str(register)
            if register in self._registers:
                return register
            raise Processor.InvalidRegisterError(f"No register called {register}. Registers are: {self.registers}")

    def registersSelect(self, registers: [int or str,] or slice) -> [str,]:
        if isinstance(registers, slice):
            registers = slice_to_tuple(registers, len(self._registers))
        registerNames = list()
        for register in registers:
            registerNames.append(self.registerSelect(register))
        return tuple(registerNames)

    def getRegister(self, register: str or int) -> bytes:
        return self._registers[self.registerSelect(register)]

    def setRegister(self, register: str or int, value: bytes):
        register = self.registerSelect(register)
        if not isinstance(value, bytes):
            raise TypeError(f"Registers store binary data as bytes not {type(value).__name__} ({value})")
        if len(value) != len(self._registers[register]):
            raise ValueError(f"{register} is a {len(self._registers[register])}-byte register so cannot be set with a {len(value)}-byte value ({value})")
        self._registers[register] = value

    def getRegisters(self, registers: [int or str,] or slice) -> [bytes,]:
        registers = self.registersSelect(registers)
        values = list()
        for register in registers:
            values.append(self._registers[register])
        return tuple(values)

    def setRegisters(self, registers: [int or str,] or slice, values: [bytes,] or bytes):
        prevValues = self.getRegisters(slice(None))
        registers = self.registersSelect(registers)
        try:
            if isinstance(values, bytes):
                pointer = 0
                for register in registers:
                    nextPointer = pointer + len(self._registers[register])
                    self.setRegister(register, values[pointer : nextPointer])
                    pointer = nextPointer
            else:
                if len(values) != len(registers):
                    raise ValueError(f"{len(registers)} registers cannot be set with {len(values)} values ({values})")
                for index in range(len(registers)):
                    self.setRegister(registers[index], values[index])
        except Exception as error:
            self.setRegisters(slice(None), prevValues)
            raise error

    @property
    def state(self) -> {str: any}:
        state = Component.state.__get__(self)
        state["registers"] = self.getRegisters(slice(None))
        return state

    @state.setter
    def state(self, state: {str: any}):
        prevState = self.state
        Component.state.__set__(self, state)
        try:
            registersState = state["registers"]
        except KeyError:
            raise Component.StateError("registers", state)
        try:
            self.setRegisters(slice(None), registersState)
        except Exception as error:
            self.state = prevState
            raise error

    @state.deleter
    def state(self):
        Component.state.__delete__(self)
        for register in self._registers:
            self._registers[register] = bytes(len(self._registers[register]))

    def execute(self): # TODO
        # if TCU == \x00
        #     currentInstruction = instructionSet.getInstruction(IR)
        # else
        #     currentInstruction[0].execute(self, currentInstruction[1])
        #     if TCU == \x00
        #         currentInstruction = (None, None)
        #         TCU -= 1
        # TCU += 1
        pass

    def response(self): # TODO
        # # process pins
        # if clock has changed
        #     self.execute()
        pass
