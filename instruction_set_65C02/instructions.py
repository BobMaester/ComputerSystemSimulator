from instruction_set_65C02.operations import Operations
from instruction_set_65C02.addressing_modes import AddressingModes

instructions = (
    (Operations.BRK, AddressingModes.Stack),
    (Operations.ORA,  AddressingModes.ZeroPageIndexedIndirect),
    None,
    None,
    (Operations.TSB, AddressingModes.ZeroPage),
    (Operations.ORA,  AddressingModes.ZeroPage),
    (Operations.ASL, AddressingModes.ZeroPage),
    (Operations.RMB0, AddressingModes.ZeroPage),
    (Operations.PHP, AddressingModes.Stack),
    (Operations.ORA,  AddressingModes.Immediate),
    (Operations.ASL, AddressingModes.Accumulator),
    None,
    (Operations.TSB, AddressingModes.Absolute),
    (Operations.ORA,  AddressingModes.Absolute),
    (Operations.ASL, AddressingModes.Absolute),
    (Operations.BBR0, AddressingModes.BranchBit),
    (Operations.BPL, AddressingModes.Relative),
    (Operations.ORA,  AddressingModes.ZeroPageIndirectIndexed),
    (Operations.ORA, AddressingModes.ZeroPageIndirect),
    None,
    (Operations.TRB, AddressingModes.ZeroPage),
    (Operations.ORA,  AddressingModes.XIndexedZeroPage),
    (Operations.ASL, AddressingModes.XIndexedZeroPage),
    (Operations.RMB1, AddressingModes.ZeroPage),
    (Operations.CLC, AddressingModes.Implied),
    (Operations.ORA,  AddressingModes.YIndexedAbsolute),
    (Operations.INC, AddressingModes.Accumulator),
    None,
    (Operations.TRB, AddressingModes.Absolute),
    (Operations.ORA,  AddressingModes.XIndexedAbsolute),
    (Operations.ASL, AddressingModes.XIndexedAbsolute),
    (Operations.BBR1, AddressingModes.BranchBit),
    (Operations.JSR, AddressingModes.Absolute),
    (Operations.AND,  AddressingModes.ZeroPageIndexedIndirect),
    None,
    None,
    (Operations.BIT, AddressingModes.ZeroPage),
    (Operations.AND,  AddressingModes.ZeroPage),
    (Operations.ROL, AddressingModes.ZeroPage),
    (Operations.RMB2, AddressingModes.ZeroPage),
    (Operations.PLP, AddressingModes.Stack),
    (Operations.AND,  AddressingModes.Immediate),
    (Operations.ROL, AddressingModes.Accumulator),
    None,
    (Operations.BIT, AddressingModes.Absolute),
    (Operations.AND,  AddressingModes.Absolute),
    (Operations.ROL, AddressingModes.Absolute),
    (Operations.BBR2, AddressingModes.BranchBit),
    (Operations.BMI, AddressingModes.Relative),
    (Operations.AND,  AddressingModes.ZeroPageIndirectIndexed),
    (Operations.AND, AddressingModes.ZeroPageIndirect),
    None,
    (Operations.BIT, AddressingModes.XIndexedZeroPage),
    (Operations.AND,  AddressingModes.XIndexedZeroPage),
    (Operations.ROL, AddressingModes.XIndexedZeroPage),
    (Operations.RMB3, AddressingModes.ZeroPage),
    (Operations.SEC, AddressingModes.Implied),
    (Operations.AND,  AddressingModes.YIndexedAbsolute),
    (Operations.DEC, AddressingModes.Accumulator),
    None,
    (Operations.BIT, AddressingModes.XIndexedAbsolute),
    (Operations.AND,  AddressingModes.XIndexedAbsolute),
    (Operations.ROL, AddressingModes.XIndexedAbsolute),
    (Operations.BBR3, AddressingModes.BranchBit),
    (Operations.RTI, AddressingModes.Stack),
    (Operations.EOR,  AddressingModes.ZeroPageIndexedIndirect),
    None,
    None,
    None,
    (Operations.EOR,  AddressingModes.ZeroPage),
    (Operations.LSR, AddressingModes.ZeroPage),
    (Operations.RMB4, AddressingModes.ZeroPage),
    (Operations.PHA, AddressingModes.Stack),
    (Operations.EOR,  AddressingModes.Immediate),
    (Operations.LSR, AddressingModes.Accumulator),
    None,
    (Operations.JMP, AddressingModes.Absolute),
    (Operations.EOR,  AddressingModes.Absolute),
    (Operations.LSR, AddressingModes.Absolute),
    (Operations.BBR4, AddressingModes.BranchBit),
    (Operations.BVC, AddressingModes.Relative),
    (Operations.EOR,  AddressingModes.ZeroPageIndirectIndexed),
    (Operations.EOR, AddressingModes.ZeroPageIndirect),
    None,
    None,
    (Operations.EOR,  AddressingModes.XIndexedZeroPage),
    (Operations.LSR, AddressingModes.XIndexedZeroPage),
    (Operations.RMB5, AddressingModes.ZeroPage),
    (Operations.CLI, AddressingModes.Implied),
    (Operations.EOR,  AddressingModes.YIndexedAbsolute),
    (Operations.PHY, AddressingModes.Stack),
    None,
    None,
    (Operations.EOR,  AddressingModes.XIndexedAbsolute),
    (Operations.LSR, AddressingModes.XIndexedAbsolute),
    (Operations.BBR5, AddressingModes.BranchBit),
    (Operations.RTS, AddressingModes.Stack),
    (Operations.ADC,  AddressingModes.ZeroPageIndexedIndirect),
    None,
    None,
    (Operations.STZ, AddressingModes.ZeroPage),
    (Operations.ADC,  AddressingModes.ZeroPage),
    (Operations.ROR, AddressingModes.ZeroPage),
    (Operations.RMB6, AddressingModes.ZeroPage),
    (Operations.PLA, AddressingModes.Stack),
    (Operations.ADC,  AddressingModes.Immediate),
    (Operations.ROR, AddressingModes.Accumulator),
    None,
    (Operations.JMP, AddressingModes.AbsoluteIndirect),
    (Operations.ADC,  AddressingModes.Absolute),
    (Operations.ROR, AddressingModes.Absolute),
    (Operations.BBR6, AddressingModes.BranchBit),
    (Operations.BVS, AddressingModes.Relative),
    (Operations.ADC,  AddressingModes.ZeroPageIndirectIndexed),
    (Operations.ADC, AddressingModes.ZeroPageIndirect),
    None,
    (Operations.STZ, AddressingModes.XIndexedZeroPage),
    (Operations.ADC,  AddressingModes.XIndexedZeroPage),
    (Operations.ROR, AddressingModes.XIndexedZeroPage),
    (Operations.RMB7, AddressingModes.ZeroPage),
    (Operations.SEI, AddressingModes.Implied),
    (Operations.ADC,  AddressingModes.YIndexedAbsolute),
    (Operations.PLY, AddressingModes.Stack),
    None,
    (Operations.JMP, AddressingModes.AbsoluteIndexedIndirect),
    (Operations.ADC,  AddressingModes.XIndexedAbsolute),
    (Operations.ROR, AddressingModes.XIndexedAbsolute),
    (Operations.BBR7, AddressingModes.BranchBit),
    (Operations.BRA, AddressingModes.Relative),
    (Operations.STA,  AddressingModes.ZeroPageIndexedIndirect),
    None,
    None,
    (Operations.STY, AddressingModes.ZeroPage),
    (Operations.STA,  AddressingModes.ZeroPage),
    (Operations.STX, AddressingModes.ZeroPage),
    (Operations.SMB0, AddressingModes.ZeroPage),
    (Operations.DEY, AddressingModes.Implied),
    (Operations.BIT,  AddressingModes.Immediate),
    (Operations.TXA, AddressingModes.Implied),
    None,
    (Operations.STY, AddressingModes.Absolute),
    (Operations.STA,  AddressingModes.Absolute),
    (Operations.STX, AddressingModes.Absolute),
    (Operations.BBS0, AddressingModes.BranchBit),
    (Operations.BCC, AddressingModes.Relative),
    (Operations.STA,  AddressingModes.ZeroPageIndirectIndexed),
    (Operations.STA, AddressingModes.ZeroPageIndirect),
    None,
    (Operations.STY, AddressingModes.XIndexedZeroPage),
    (Operations.STA,  AddressingModes.XIndexedZeroPage),
    (Operations.STX, AddressingModes.YIndexedZeroPage),
    (Operations.SMB1, AddressingModes.ZeroPage),
    (Operations.TYA, AddressingModes.Implied),
    (Operations.STA,  AddressingModes.YIndexedAbsolute),
    (Operations.TXS, AddressingModes.Implied),
    None,
    (Operations.STZ, AddressingModes.Absolute),
    (Operations.STA,  AddressingModes.XIndexedAbsolute),
    (Operations.STZ, AddressingModes.XIndexedAbsolute),
    (Operations.BBS1, AddressingModes.BranchBit),
    (Operations.LDY, AddressingModes.Immediate),
    (Operations.LDA,  AddressingModes.ZeroPageIndexedIndirect),
    (Operations.LDX, AddressingModes.Immediate),
    None,
    (Operations.LDY, AddressingModes.ZeroPage),
    (Operations.LDA,  AddressingModes.ZeroPage),
    (Operations.LDX, AddressingModes.ZeroPage),
    (Operations.SMB2, AddressingModes.ZeroPage),
    (Operations.TAY, AddressingModes.Implied),
    (Operations.LDA,  AddressingModes.Immediate),
    (Operations.TAX, AddressingModes.Implied),
    None,
    (Operations.LDY, AddressingModes.Absolute),
    (Operations.LDA,  AddressingModes.Absolute),
    (Operations.LDX, AddressingModes.Absolute),
    (Operations.BBS2, AddressingModes.BranchBit),
    (Operations.BCS, AddressingModes.Relative),
    (Operations.LDA,  AddressingModes.ZeroPageIndirectIndexed),
    (Operations.LDA, AddressingModes.ZeroPageIndirect),
    None,
    (Operations.LDY, AddressingModes.XIndexedZeroPage),
    (Operations.LDA,  AddressingModes.XIndexedZeroPage),
    (Operations.LDX, AddressingModes.YIndexedZeroPage),
    (Operations.SMB3, AddressingModes.ZeroPage),
    (Operations.CLV, AddressingModes.Implied),
    (Operations.LDA,  AddressingModes.YIndexedAbsolute),
    (Operations.TSX, AddressingModes.Implied),
    None,
    (Operations.LDY, AddressingModes.XIndexedAbsolute),
    (Operations.LDA,  AddressingModes.XIndexedAbsolute),
    (Operations.LDX, AddressingModes.YIndexedAbsolute),
    (Operations.BBS3, AddressingModes.BranchBit),
    (Operations.CPY, AddressingModes.Immediate),
    (Operations.CMP,  AddressingModes.ZeroPageIndexedIndirect),
    None,
    None,
    (Operations.CPY, AddressingModes.ZeroPage),
    (Operations.CMP,  AddressingModes.ZeroPage),
    (Operations.DEC, AddressingModes.ZeroPage),
    (Operations.SMB4, AddressingModes.ZeroPage),
    (Operations.INY, AddressingModes.Implied),
    (Operations.CMP,  AddressingModes.Immediate),
    (Operations.DEX, AddressingModes.Implied),
    (Operations.WAI,  AddressingModes.Implied),
    (Operations.CPY, AddressingModes.Absolute),
    (Operations.CMP,  AddressingModes.Absolute),
    (Operations.DEC, AddressingModes.Absolute),
    (Operations.BBS4, AddressingModes.BranchBit),
    (Operations.BNE, AddressingModes.Relative),
    (Operations.CMP,  AddressingModes.ZeroPageIndirectIndexed),
    (Operations.CMP, AddressingModes.ZeroPageIndirect),
    None,
    None,
    (Operations.CMP,  AddressingModes.XIndexedZeroPage),
    (Operations.DEC, AddressingModes.XIndexedZeroPage),
    (Operations.SMB5, AddressingModes.ZeroPage),
    (Operations.CLD, AddressingModes.Implied),
    (Operations.CMP,  AddressingModes.YIndexedAbsolute),
    (Operations.PHX, AddressingModes.Stack),
    (Operations.STP,  AddressingModes.Implied),
    None,
    (Operations.CMP,  AddressingModes.XIndexedAbsolute),
    (Operations.DEC, AddressingModes.XIndexedAbsolute),
    (Operations.BBS5, AddressingModes.BranchBit),
    (Operations.CPX, AddressingModes.Immediate),
    (Operations.SBC,  AddressingModes.ZeroPageIndexedIndirect),
    None,
    None,
    (Operations.CPX, AddressingModes.ZeroPage),
    (Operations.SBC,  AddressingModes.ZeroPage),
    (Operations.INC, AddressingModes.ZeroPage),
    (Operations.SMB6, AddressingModes.ZeroPage),
    (Operations.INX, AddressingModes.Implied),
    (Operations.SBC,  AddressingModes.Immediate),
    (Operations.NOP, AddressingModes.Implied),
    None,
    (Operations.CPX, AddressingModes.Absolute),
    (Operations.SBC,  AddressingModes.Absolute),
    (Operations.INC, AddressingModes.Absolute),
    (Operations.BBS6, AddressingModes.BranchBit),
    (Operations.BEQ, AddressingModes.Relative),
    (Operations.SBC,  AddressingModes.ZeroPageIndirectIndexed),
    (Operations.SBC, AddressingModes.ZeroPageIndirect),
    None,
    None,
    (Operations.SBC,  AddressingModes.XIndexedZeroPage),
    (Operations.INC, AddressingModes.XIndexedZeroPage),
    (Operations.SMB7, AddressingModes.ZeroPage),
    (Operations.SED, AddressingModes.Implied),
    (Operations.SBC,  AddressingModes.YIndexedAbsolute),
    (Operations.PLX, AddressingModes.Stack),
    None,
    None,
    (Operations.SBC,  AddressingModes.XIndexedAbsolute),
    (Operations.INC, AddressingModes.XIndexedAbsolute),
    (Operations.BBS7, AddressingModes.BranchBit)
)
