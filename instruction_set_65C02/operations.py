from processor import Processor
from instruction_set import Operation, AddressingMode

def RMB(bit: int, processor: Processor, addressingMode: AddressingMode):
    pass

def SMB(bit: int, processor: Processor, addressingMode: AddressingMode):
    pass

def BBR(bit: int, processor: Processor, addressingMode: AddressingMode):
    pass

def BBS(bit: int, processor: Processor, addressingMode: AddressingMode):
    pass

class Operations: # TODO

    class BRK(Operation):
        mnemonic = "BRK"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BPL(Operation):
        mnemonic = "BPL"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class JSR(Operation):
        mnemonic = "JSR"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BMI(Operation):
        mnemonic = "BMI"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class RTI(Operation):
        mnemonic = "RTI"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BVC(Operation):
        mnemonic = "BVC"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class RTS(Operation):
        mnemonic = "RTS"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BVS(Operation):
        mnemonic = "BVS"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BRA(Operation):
        mnemonic = "BRA"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BCC(Operation):
        mnemonic = "BCC"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class LDY(Operation):
        mnemonic = "LDY"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BCS(Operation):
        mnemonic = "BCS"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class CPY(Operation):
        mnemonic = "CPY"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BNE(Operation):
        mnemonic = "BNE"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class CPX(Operation):
        mnemonic = "CPX"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BEQ(Operation):
        mnemonic = "BEQ"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class ORA(Operation):
        mnemonic = "ORA"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class AND(Operation):
        mnemonic = "AND"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class EOR(Operation):
        mnemonic = "EOR"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class ADC(Operation):
        mnemonic = "ADC"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class STA(Operation):
        mnemonic = "STA"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class LDA(Operation):
        mnemonic = "LDA"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class CMP(Operation):
        mnemonic = "CMP"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class SBC(Operation):
        mnemonic = "SBC"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class LDX(Operation):
        mnemonic = "LDX"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class TSB(Operation):
        mnemonic = "TSB"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class TRB(Operation):
        mnemonic = "TRB"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BIT(Operation):
        mnemonic = "BIT"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class STZ(Operation):
        mnemonic = "STZ"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class STY(Operation):
        mnemonic = "STY"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class ASL(Operation):
        mnemonic = "ASL"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class ROL(Operation):
        mnemonic = "ROL"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class LSR(Operation):
        mnemonic = "LSR"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class ROR(Operation):
        mnemonic = "ROR"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class STX(Operation):
        mnemonic = "STX"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class DEC(Operation):
        mnemonic = "DEC"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class INC(Operation):
        mnemonic = "INC"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class RMB0(Operation):
        mnemonic = "RMB0"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            RMB(0, processor, addressingMode)

    class RMB1(Operation):
        mnemonic = "RMB1"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            RMB(1, processor, addressingMode)

    class RMB2(Operation):
        mnemonic = "RMB2"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            RMB(2, processor, addressingMode)

    class RMB3(Operation):
        mnemonic = "RMB3"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            RMB(3, processor, addressingMode)

    class RMB4(Operation):
        mnemonic = "RMB4"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            RMB(4, processor, addressingMode)

    class RMB5(Operation):
        mnemonic = "RMB5"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            RMB(5, processor, addressingMode)

    class RMB6(Operation):
        mnemonic = "RMB6"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            RMB(6, processor, addressingMode)

    class RMB7(Operation):
        mnemonic = "RMB7"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            RMB(7, processor, addressingMode)

    class SMB0(Operation):
        mnemonic = "SMB0"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            SMB(0, processor, addressingMode)

    class SMB1(Operation):
        mnemonic = "SMB1"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            SMB(1, processor, addressingMode)

    class SMB2(Operation):
        mnemonic = "SMB2"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            SMB(2, processor, addressingMode)

    class SMB3(Operation):
        mnemonic = "SMB3"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            SMB(3, processor, addressingMode)

    class SMB4(Operation):
        mnemonic = "SMB4"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            SMB(4, processor, addressingMode)

    class SMB5(Operation):
        mnemonic = "SMB5"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            SMB(5, processor, addressingMode)

    class SMB6(Operation):
        mnemonic = "SMB6"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            SMB(6, processor, addressingMode)

    class SMB7(Operation):
        mnemonic = "SMB7"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            SMB(7, processor, addressingMode)

    class PHP(Operation):
        mnemonic = "PHP"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class CLC(Operation):
        mnemonic = "CLC"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class PLP(Operation):
        mnemonic = "PLP"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class SEC(Operation):
        mnemonic = "SEC"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class PHA(Operation):
        mnemonic = "PHA"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class CLI(Operation):
        mnemonic = "CLI"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class PLA(Operation):
        mnemonic = "PLA"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class SEI(Operation):
        mnemonic = "SEI"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class DEY(Operation):
        mnemonic = "DEY"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class TYA(Operation):
        mnemonic = "TYA"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class TAY(Operation):
        mnemonic = "TAY"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class CLV(Operation):
        mnemonic = "CLV"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class INY(Operation):
        mnemonic = "INY"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class CLD(Operation):
        mnemonic = "CLD"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class INX(Operation):
        mnemonic = "INX"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class SED(Operation):
        mnemonic = "SED"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class PHY(Operation):
        mnemonic = "PHY"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class PLY(Operation):
        mnemonic = "PLY"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class TXA(Operation):
        mnemonic = "TXA"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class TXS(Operation):
        mnemonic = "TXS"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class TAX(Operation):
        mnemonic = "TAX"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class TSX(Operation):
        mnemonic = "TSX"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class DEX(Operation):
        mnemonic = "DEX"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class PHX(Operation):
        mnemonic = "PHX"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class NOP(Operation):
        mnemonic = "NOP"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            processor.setRegister("TCU", bytes(1))

    class PLX(Operation):
        mnemonic = "PLX"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class WAI(Operation):
        mnemonic = "WAI"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class STP(Operation):
        mnemonic = "STP"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class JMP(Operation):
        mnemonic = "JMP"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            pass

    class BBR0(Operation):
        mnemonic = "BBR0"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBR(0, processor, addressingMode)

    class BBR1(Operation):
        mnemonic = "BBR1"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBR(1, processor, addressingMode)

    class BBR2(Operation):
        mnemonic = "BBR2"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBR(2, processor, addressingMode)

    class BBR3(Operation):
        mnemonic = "BBR3"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBR(3, processor, addressingMode)

    class BBR4(Operation):
        mnemonic = "BBR4"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBR(4, processor, addressingMode)

    class BBR5(Operation):
        mnemonic = "BBR5"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBR(5, processor, addressingMode)

    class BBR6(Operation):
        mnemonic = "BBR6"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBR(6, processor, addressingMode)

    class BBR7(Operation):
        mnemonic = "BBR7"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBR(7, processor, addressingMode)

    class BBS0(Operation):
        mnemonic = "BBS0"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBS(0, processor, addressingMode)

    class BBS1(Operation):
        mnemonic = "BBS1"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBS(1, processor, addressingMode)

    class BBS2(Operation):
        mnemonic = "BBS2"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBS(2, processor, addressingMode)

    class BBS3(Operation):
        mnemonic = "BBS3"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBS(3, processor, addressingMode)

    class BBS4(Operation):
        mnemonic = "BBS4"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBS(4, processor, addressingMode)

    class BBS5(Operation):
        mnemonic = "BBS5"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBS(5, processor, addressingMode)

    class BBS6(Operation):
        mnemonic = "BBS6"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBS(6, processor, addressingMode)

    class BBS7(Operation):
        mnemonic = "BBS7"

        @staticmethod
        def execute(processor: Processor, addressingMode: AddressingMode):
            BBS(7, processor, addressingMode)
