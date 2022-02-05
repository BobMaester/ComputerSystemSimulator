from processor import Processor
from instruction_set import AddressingMode

class AddressingModes: # TODO
    class Absolute(AddressingMode): # a
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class AbsoluteIndexedIndirect(AddressingMode): # (a,x)
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class XIndexedAbsolute(AddressingMode): # a,x
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class YIndexedAbsolute(AddressingMode): # a,y
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class AbsoluteIndirect(AddressingMode): # (a)
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class Accumulator(AddressingMode): # A
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class Immediate(AddressingMode): # #
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class Implied(AddressingMode): # i
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            if operandString == "":
                return bytes(), tuple()
            else:
                raise AddressingMode.AddressingModeAssembleError("Implied addressing mode takes no operands")

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            return True, bytes()

    class Relative(AddressingMode): # r
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class Stack(AddressingMode): # s
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class ZeroPage(AddressingMode): # zp
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class ZeroPageIndexedIndirect(AddressingMode): # (zp,x)
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class XIndexedZeroPage(AddressingMode): # zp,x
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class YIndexedZeroPage(AddressingMode): # zp,y
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class ZeroPageIndirect(AddressingMode): # (zp)
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class ZeroPageIndirectIndexed(AddressingMode): # (zp),y
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

    class BranchBit(AddressingMode): # zp,r
        @staticmethod
        def assemble(operandString: str, address: int = 0, labels: [str,] = tuple()) -> [bytes, [[int, str],]]:
            pass

        @staticmethod
        def fetchOperand(processor: Processor, fetchCount: int) -> [bool, bytes]:
            pass

        @staticmethod
        def assembleLabel(labelAddress: int, instructionAddress: int) -> bytes:
            return AddressingMode.relativeLabel(labelAddress, instructionAddress)
