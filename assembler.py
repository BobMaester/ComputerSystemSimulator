from instruction_set import InstructionSet, AddressingMode

class Assembler:
    class AssemblerError(Exception):
        pass

    def __init__(self, instructionSet: InstructionSet, symbols: {str: str} = None, labels: {str: int} = None):
        if not isinstance(instructionSet, InstructionSet):
            raise TypeError(f"An assembler must be associated with an instruction set ({instructionSet} is not valid)")
        self._instructionSet = instructionSet
        if symbols is None:
            self._symbols = dict()
        elif isinstance(symbols, dict):
            self._symbols = symbols
        else:
            raise TypeError(f"Symbols must be given as a dictionary with the key as the symbol identifier and the value as associated assembly (not {symbols})")
        if labels is None:
            self._labels = dict()
        elif isinstance(labels, dict):
            self._labels = labels
        else:
            raise TypeError(f"Labels must be given as a dictionary with the key as the label identifier and the value as the address in memory (not {labels})")

    @property
    def instructionSet(self) -> InstructionSet:
        return self._instructionSet

    @property
    def symbols(self) -> {str: str}:
        return self._symbols.copy()
    
    @symbols.deleter
    def symbols(self):
        self._symbols = dict()

    @property
    def symbolIdentifiers(self) -> [str,]:
         return tuple(self._symbols.keys())

    def addSymbol(self, identifier: str, meaning: str):
        if isinstance(meaning, int):
            self.addLabel(identifier, meaning)
        else:
            self._symbols[str(identifier).strip()] = str(meaning).strip()

    def removeSymbol(self, identifier: str):
        del self._symbols[identifier]

    @property
    def labels(self) -> {str: str}:
        return self._labels.copy()

    @labels.deleter
    def labels(self):
        self._labels = dict()

    @property
    def labelIdentifiers(self) -> [str,]:
        return tuple(self._labels.keys())

    def addLabel(self, identifier: str, address: int):
        if isinstance(address, int):
            self._labels[str(identifier).split()] = address
        else:
            self.addSymbol(identifier, str(address))

    def removeLabel(self, identifier: str):
        del self._labels[identifier]

    def _preprocessing(self, assembly: str or [str,]) -> [[[str, str],], {int: str}]:
        if isinstance(assembly, str):
            lines = assembly.split("\n")
        else:
            lines = tuple(assembly)
        instructionCalls = list()
        labelLines = dict()
        for line in lines:
            line = line.strip()
            if line[-1] == ":":
                labelLines[len(instructionCalls)] = line[:-1]
            elif "=" in line:
                split = line.index("=")
                self.addSymbol(line[:split], line[split + 1:])
            else:
                try:
                    split = line.index(" ")
                except ValueError:
                    split = len(line)
                mnemonic = line[:split]
                operands = line[split:].strip()
                for symbol in self.symbols:
                    operands = operands.replace(symbol, self.symbols[symbol])
                instructionCalls.append((mnemonic, operands))
        return instructionCalls, labelLines

    def _assembleLine(self, line: [str, str], address: int = 0, labels: [str,] = tuple()) -> [AddressingMode, bytes, [[str, int]]]:
        mnemonic, operands = line
        operation = self._instructionSet.getOperationByMnemonic(mnemonic)
        for addressingMode in self._instructionSet.operationAddressingModes(operation):
            try:
                assembledOperands, labelUses = addressingMode.assemble(operands, address, labels)
                opcode = self._instructionSet.getOpcode(operation, addressingMode)
                return addressingMode, bytes((opcode,)) + assembledOperands, labelUses
            except AddressingMode.AddressingModeAssembleError:
                pass
        raise Assembler.AssemblerError(f"Could not identify addressing mode: '{mnemonic} {operands}'")

    def assemble(self, assembly: str or [str,], startAddress: int = 0) -> bytes: # TODO labels without placeholders
        machineCode = bytes()
        lines, labels = self._preprocessing(assembly)
        labelUses = list()
        labelAddresses = dict()
        labelIdentifiers = self.labelIdentifiers + tuple(labels.values())
        for line in range(len(lines)):
            if line in labels:
                labelAddresses[labels[line]] = len(machineCode)
            addressingMode, lineMachineCode, lineLabelUses = self._assembleLine(lines[line], startAddress + line, labelIdentifiers)
            for identifier, byte in lineLabelUses:
                labelUses.append((len(machineCode) + 1 + byte, identifier, addressingMode))
            machineCode += lineMachineCode
        for address, label, addressingMode in labelUses:
            if label in labelAddresses:
                labelAddress = labelAddresses[label]
                self._labels[label] = labelAddress
            else:
                labelAddress = self._labels[label]
            assembledLabel = addressingMode.assembleLabel(labelAddress, address)
            machineCode = machineCode[:address] + assembledLabel + machineCode[address + len(assembledLabel):]
        return machineCode
