from __future__ import annotations
from processor import Processor
from instruction_set import AddressingMode

class LabelModes:
    @staticmethod
    def immediateLabel(labelAddress: int, instructionAddress: int = None) -> bytes:
        return labelAddress.to_bytes(2, "little")

    @staticmethod
    def relativeLabel(labelAddress: int, instructionAddress: int) -> bytes:
        return bytes([labelAddress - instructionAddress])

class Absolute(AddressingMode): # a
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class AbsoluteIndexedIndirect(AddressingMode): # (a,x)
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class XIndexedAbsolute(AddressingMode): # a,x
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class YIndexedAbsolute(AddressingMode): # a,y
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class AbsoluteIndirect(AddressingMode): # (a)
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class Accumulator(AddressingMode): # A
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class Immediate(AddressingMode): # #
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class Implied(AddressingMode): # i
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        if operandString == str():
            return bytes(), tuple()
        else:
            raise AddressingMode.AddressingModeAssembleError("Implied addressing mode takes no operands")

class Relative(AddressingMode): # r
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class Stack(AddressingMode): # s
    assemble = Implied.assemble

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class ZeroPage(AddressingMode): # zp
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class ZeroPageIndexedIndirect(AddressingMode): # (zp,x)
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class XIndexedZeroPage(AddressingMode): # zp,x
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class YIndexedZeroPage(AddressingMode): # zp,y
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class ZeroPageIndirect(AddressingMode): # (zp)
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class ZeroPageIndirectIndexed(AddressingMode): # (zp),y
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

class BranchBit(AddressingMode): # zp,r
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        pass

    @staticmethod
    def assembleLabel(labelAddress: int, instructionAddress: int) -> bytes:
        return LabelModes.relativeLabel(labelAddress, instructionAddress)

class AddressingModes:
    Absolute = Absolute
    AbsoluteIndexedIndirect = AbsoluteIndexedIndirect
    XIndexedAbsolute = XIndexedAbsolute
    YIndexedAbsolute = YIndexedAbsolute
    AbsoluteIndirect = AbsoluteIndirect
    Accumulator = Accumulator
    Immediate = Immediate
    Implied = Implied
    Relative = Relative
    Stack = Stack
    ZeroPage = ZeroPage
    ZeroPageIndexedIndirect = ZeroPageIndexedIndirect
    XIndexedZeroPage = XIndexedZeroPage
    YIndexedZeroPage = YIndexedZeroPage
    ZeroPageIndirect = ZeroPageIndirect
    ZeroPageIndirectIndexed = ZeroPageIndirectIndexed
    BranchBit = BranchBit
