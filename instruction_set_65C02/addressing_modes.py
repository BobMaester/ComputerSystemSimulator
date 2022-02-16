from __future__ import annotations
from processor import Processor
from instruction_set import AddressingMode
from general import bytesToTuple

class LabelModes:
    @staticmethod
    def immediateLabel(labelAddress: int, instructionAddress: int = None) -> bytes:
        return labelAddress.to_bytes(2, "little")

    @staticmethod
    def relativeLabel(labelAddress: int, instructionAddress: int) -> bytes:
        return bytes([labelAddress - instructionAddress])

class AssembleMethods:
    @staticmethod
    def noOperands(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        if operandString == str():
            return bytes(), tuple()
        else:
            raise AddressingMode.AddressingModeAssembleError("Implied addressing mode takes no operands")
    
    @staticmethod
    def absolute(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def zeroPage(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

    @staticmethod
    def extractIndexedAddress(operandString: str) -> str:
        operandString = operandString.strip()
        if operandString[-1].lower() != "x" and operandString[-1].lower() != "y":
            raise AddressingMode.AddressingModeAssembleError("Indexed addressed operands must end with the index register used (x or y)")
        operandString = operandString[:-1].strip()
        if operandString[-1] != ",":
            raise AddressingMode.AddressingModeAssembleError("Indexed registers must be seperated from the address with a comma")
        return operandString[:-1].strip()

    @staticmethod
    def extractIndirectAddress(operandString: str) -> str:
        operandString = operandString.strip()
        if operandString[0] != "(" or operandString[-1] != ")":
            raise AddressingMode.AddressingModeAssembleError("Indirect address must be contained within brackets")
        return operandString[1 : -1].strip()

class FetchMethods:
    @staticmethod
    def readMemory1(processor: Processor, address: bytes):
        address = bytesToTuple(address)
        for bit in range(16):
            processor.setPinState(f"A{bit}", (address, True))
        processor.setPinState("RWB", (True, True))

    @staticmethod
    def readMemory2(processor: Processor) -> bytes:
        data = 0
        for bit in range(8):
            data += processor.getRegister(f"D{bit}") * 2 ** bit
        return bytes((data,))

    @staticmethod
    def writeMemory(processor: Processor, address: bytes, data: bytes):
        address = bytesToTuple(address)
        data = bytesToTuple(data)
        for bit in range(16):
            processor.setPinState(f"A{bit}", (address[bit], True))
            if bit < 8:
                processor.setPinState(f"D{bit}", (data[bit], True))
        processor.setPinState("RWB", (False, True))

class Absolute(AddressingMode): # a
    assemble = AssembleMethods.absolute

class AbsoluteIndexedIndirect(AddressingMode): # (a,x)
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return AssembleMethods.absolute(AssembleMethods.extractIndexedAddress(AssembleMethods.extractIndirectAddress(operandString)), labels)

class XIndexedAbsolute(AddressingMode): # a,x
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return AssembleMethods.absolute(AssembleMethods.extractIndexedAddress(operandString), labels)

class YIndexedAbsolute(AddressingMode): # a,y
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return AssembleMethods.absolute(AssembleMethods.extractIndexedAddress(operandString), labels)

class AbsoluteIndirect(AddressingMode): # (a)
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return AssembleMethods.absolute(AssembleMethods.extractIndirectAddress(operandString), labels)

class Accumulator(AddressingMode): # A
    assemble = AssembleMethods.noOperands

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        return True, processor.getRegister("A")

class Immediate(AddressingMode): # #
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

class Implied(AddressingMode): # i
    assemble = AssembleMethods.noOperands

class Relative(AddressingMode): # r
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        pass

class Stack(AddressingMode): # s
    assemble = AssembleMethods.noOperands

    @staticmethod
    def fetchOperands(processor: Processor) -> [bool, bytes]:
        return True, processor.getRegister("S")

class ZeroPage(AddressingMode): # zp
    assemble = AssembleMethods.zeroPage

class ZeroPageIndexedIndirect(AddressingMode): # (zp,x)
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return AssembleMethods.zeroPage(AssembleMethods.extractIndexedAddress(AssembleMethods.extractIndirectAddress(operandString)), labels)

class XIndexedZeroPage(AddressingMode): # zp,x
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return AssembleMethods.zeroPage(AssembleMethods.extractIndexedAddress(operandString), labels)

class YIndexedZeroPage(AddressingMode): # zp,y
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return AssembleMethods.zeroPage(AssembleMethods.extractIndexedAddress(operandString), labels)

class ZeroPageIndirect(AddressingMode): # (zp)
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return AssembleMethods.zeroPage(AssembleMethods.extractIndirectAddress(operandString), labels)

class ZeroPageIndirectIndexed(AddressingMode): # (zp),y
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        return AssembleMethods.zeroPage(AssembleMethods.extractIndirectAddress(AssembleMethods.extractIndexedAddress(operandString)), labels)

class BranchBit(AddressingMode): # zp,r
    @staticmethod
    def assemble(operandString: str, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
        try:
            zeroPage, relative = operandString.split(",", 1)
        except ValueError:
            raise AddressingMode.AddressingModeAssembleError("Branch bit instructions must be formed of a zero page address and a relative address seperated by a comma")
        byte1, labelUses1 = AssembleMethods.zeroPage(zeroPage)
        byte2, labelUses2 = Relative.assemble(relative, labels)
        return byte1 + byte2, labelUses1 + labelUses2

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
