from __future__ import annotations
from component import Component
from abc import ABC, abstractmethod

class AddressingMode(ABC):
    class AddressingModeAssembleError(Exception):
        pass

    class LabelsNotSupportedError(Exception):
        pass

    class LabelAddressError(ValueError):
        pass

    @staticmethod
    @abstractmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def assembleLabel(labelAddress: int, instructionAddress: int) -> bytes:
        raise AddressingMode.LabelsNotSupportedError("Addressing mode does not support the use of labels")

    @staticmethod
    def fetchOperands(processor: Component) -> [bool, bytes]:
        return True, bytes()

class Operation(ABC):
    mnemonic = str()

    @staticmethod
    @abstractmethod
    def execute(processor: Component, addressingMode: AddressingMode):
        pass

class DynamicAddressingMode(AddressingMode):
    def __init__(self, assemble: callable, assembleLabel: callable = AddressingMode.assembleLabel, fetchOperand: callable = AddressingMode.fetchOperands):
        self._assemble = assemble
        self._fetchOperand = fetchOperand
        self._assembleLabel = assembleLabel

    def assemble(self, operandString, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return self._assemble(operandString, labels)

    def assembleLabel(self, labelAddress: int, instructionAddress: int) -> bytes:
        return self._assembleLabel(labelAddress, instructionAddress)

    def fetchOperands(self, processor) -> [bool, bytes]:
        return self._fetchOperand(processor)

class DynamicOperation(Operation):
    def __init__(self, mnemonic: str, execute: callable):
        self._mnemonic = str(mnemonic)
        self._execute = execute

    @property
    def mnemonic(self) -> str:
        return self._mnemonic

    def execute(self, processor: Component, addressingMode: AddressingMode):
        self._execute(processor, addressingMode)

class InstructionSet:
    @staticmethod
    def validateInstruction(instruction: [Operation, AddressingMode]) -> [Operation, AddressingMode]:
        if len(instruction) != 2:
            raise ValueError(f"Instructions must be of the form (Operation, AddressingMode) not {instruction}")
        if not (issubclass(instruction[0], Operation) and issubclass(instruction[1], AddressingMode)):
            raise TypeError(f"Invalid instruction types {type(instruction[0]).__name__, type(instruction[1]).__name__} must be (Operation, AddressingMode)")
        return tuple(instruction)

    @staticmethod
    def validateInstructions(instructions: [[Operation, AddressingMode],]) -> [[Operation, AddressingMode],]:
        validInstructions = list()
        mnemonics = {}
        for instruction in instructions:
            if instruction is None or instruction == (None, None):
                validInstructions.append((None, None))
            else:
                instruction = InstructionSet.validateInstruction(instruction)
                operation = instruction[0]
                mnemonic = operation.mnemonic
                if mnemonic in mnemonics:
                    if operation != mnemonics[mnemonic]:
                        raise ValueError(f"Operations in an instruction set must have unique mnemonics ({mnemonic} is repeated)")
                else:
                    mnemonics[mnemonic] = operation
                validInstructions.append(tuple(instruction))
        return tuple(validInstructions)

    @staticmethod
    def instructionsFromOpcodeDict(opcodeDict: {int: [Operation, AddressingMode]}) -> [[Operation, AddressingMode],]:
        instructions = [None] * (max(tuple(opcodeDict.keys())) + 1)
        for opcode in opcodeDict:
            instructions[opcode] = InstructionSet.validateInstruction(opcodeDict[opcode])
        return InstructionSet.validateInstructions(instructions)

    @staticmethod
    def instructionsFromOperationDict(operationsDict: {Operation: [[AddressingMode, int],]}) -> [[Operation, AddressingMode],]:
        instructions = {}
        for operation in operationsDict:
            for addressingMode, opcode in operationsDict[operation]:
                if opcode in instructions:
                    raise ValueError(f"An opcode cannot have multiple instructions ({opcode})")
                else:
                    instructions[opcode] = InstructionSet.validateInstruction((operation, addressingMode))
        return InstructionSet.instructionsFromOpcodeDict(instructions)

    @staticmethod
    def instructionsFromAddressingModeDict(addressingModeDict: {AddressingMode: [[Operation, int],]}) -> [[Operation, AddressingMode],]:
        instructions = {}
        for addressingMode in addressingModeDict:
            for operation, opcode in addressingModeDict[addressingMode]:
                if opcode in instructions:
                    raise ValueError(f"An opcode cannot have multiple instructions ({opcode})")
                else:
                    instructions[opcode] = InstructionSet.validateInstruction((operation, addressingMode))
        return InstructionSet.instructionsFromOpcodeDict(instructions)

    def __init__(self, instructions: [[Operation, AddressingMode],]):
        self._instructions = InstructionSet.validateInstructions(instructions)

    @property
    def instructions(self) -> [[Operation, AddressingMode]]:
        instructions = list()
        for instruction in self._instructions:
            if instruction != (None, None):
                instructions.append(instruction)
        return tuple(instructions)

    @property
    def operations(self) -> [Operation,]:
        operations = list()
        for operation, addressingMode in self._instructions:
            if operation is not None:
                if operation not in operations:
                    operations.append(operation)
        return tuple(operations)

    @property
    def addressingModes(self) -> [AddressingMode,]:
        addressingModes = list()
        for addressingMode, addressingMode in self._instructions:
            if addressingMode is not None:
                if addressingMode not in addressingModes:
                    addressingModes.append(addressingMode)
        return tuple(addressingModes)

    @property
    def opcodes(self) -> [int,]:
        opcodes = list()
        for opcode in range(len(self._instructions)):
            if self._instructions[opcode] != (None, None):
                if opcode not in opcodes:
                    opcodes.append(opcode)
        return tuple(opcodes)

    def getOperationByMnemonic(self, mnemonic: str) -> Operation:
        for operation, addressingMode in self._instructions:
            if operation is not None:
                if mnemonic.lower() == operation.mnemonic.lower():
                    return operation
        raise ValueError(f"No operation in instruction set, {self}, with mnemonic, {mnemonic}")

    def getInstruction(self, opcode: int or bytes) -> [Operation, AddressingMode]:
        if isinstance(opcode, bytes):
            opcode = int.from_bytes(opcode, "little")
        return self._instructions[opcode]

    def getOpcode(self, operation: Operation or str, addressingMode: AddressingMode) -> int:
        if isinstance(operation, str):
            operation = self.getOperationByMnemonic(operation)
        return self._instructions.index((operation, addressingMode))

    def operationAddressingModes(self, operation: Operation or str) -> [AddressingMode]:
        if isinstance(operation, str):
            operation = self.getOperationByMnemonic(operation)
        addressingModes = list()
        for instruction in self._instructions:
            if operation == instruction[0]:
                addressingModes.append(instruction[1])
        return addressingModes

    def addressingModeOperations(self, addressingMode: AddressingMode) -> [Operation]:
        operations = list()
        for instruction in self._instructions:
            if addressingMode == instruction[1]:
                operations.append(instruction[0])
        return operations

    def execute(self, processor: Component, opcode: int or bytes):
        operation, addressingMode = self.getInstruction(opcode)
        operation.execute(processor, addressingMode)

    @staticmethod
    def initialiseFromOpcodeDict(opcodeDict: {int: [Operation, AddressingMode]}) -> InstructionSet:
        return InstructionSet(InstructionSet.instructionsFromOpcodeDict(opcodeDict))

    @staticmethod
    def initialiseFromOperationDict(operationDict: {Operation: [[AddressingMode, int],]}) -> InstructionSet:
        return InstructionSet(InstructionSet.instructionsFromOperationDict(operationDict))

    @staticmethod
    def initialiseFromAddressingModeDict(addressingModeDict: {AddressingMode: [[Operation, int],]}) -> InstructionSet:
        return InstructionSet(InstructionSet.instructionsFromAddressingModeDict(addressingModeDict))
