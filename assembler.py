from instruction_set import InstructionSet, AddressingMode

class Assembler:
    class AssemblerError(Exception):
        pass

    def __init__(self, instructionSet: InstructionSet, symbols: {str: str} or [[str, str]] = None, labels: {str: int} or [[str, int]] = None):
        if not isinstance(instructionSet, InstructionSet):
            raise TypeError(f"An assembler must be associated with an instruction set ({instructionSet} is not valid)")
        self._instructionSet = instructionSet
        self._symbols = dict()
        if symbols:
            self.addSymbols(symbols)
        self._labels = dict()
        if labels:
            self.addLabels(labels)

    @property
    def instructionSet(self) -> InstructionSet:
        return self._instructionSet

    @property
    def symbols(self) -> {str: str}:
        return self._symbols.copy()

    @symbols.setter
    def symbols(self, symbols: {str: str} or [[str, str],]):
        prevSymbols = self._symbols
        self._symbols = dict()
        try:
            self.addSymbols(symbols)
        except Exception as error:
            self._symbols = prevSymbols
            raise error

    @symbols.deleter
    def symbols(self):
        self._symbols = dict()

    @property
    def symbolIdentifiers(self) -> [str,]:
         return tuple(self._symbols.keys())

    def addSymbol(self, identifier: str, meaning: str):
        self._symbols[str(identifier).strip()] = str(meaning).strip()

    def addSymbols(self, symbols: {str: str} or [[str, str],]):
        prevSymbols = self._symbols.copy()
        try:
            if isinstance(symbols, dict):
                for identifier in symbols:
                    self.addSymbol(identifier, symbols[identifier])
            else:
                for identifier, meaning in symbols:
                    self.addSymbol(identifier, meaning)
        except Exception as error:
            self._symbols = prevSymbols
            raise error

    def removeSymbol(self, identifier: str):
        del self._symbols[identifier]

    def removeSymbols(self, identifiers: [str,]):
        prevSymbols = self._symbols.copy()
        try:
            for identifier in identifiers:
                self.removeSymbol(identifier)
        except Exception as error:
            self._symbols = prevSymbols
            raise error

    @property
    def labels(self) -> {str: int}:
        return self._labels.copy()

    @labels.setter
    def labels(self, labels: {str: int} or [[str, int],]):
        prevLabels = self._labels
        self._labels = dict()
        try:
            self.addLabels(labels)
        except Exception as error:
            self._labels = prevLabels
            raise error

    @labels.deleter
    def labels(self):
        self._labels = dict()

    @property
    def labelIdentifiers(self) -> [str,]:
        return tuple(self._labels.keys())

    def addLabel(self, identifier: str, address: int):
        if not isinstance(address, int):
            raise TypeError(f"Label must have an integer address (not {address} of type {type(address).__name__})")
        self._labels[str(identifier).strip()] = address

    def addLabels(self, labels: {str: int} or [[str, int],]):
        prevLabels = self._labels.copy()
        try:
            if isinstance(labels, dict):
                for identifier in labels:
                    self.addLabel(identifier, labels[identifier])
            else:
                for identifier, address in labels:
                    self.addLabel(identifier, address)
        except Exception as error:
            self._labels = prevLabels
            raise error

    def removeLabel(self, identifier: str):
        del self._labels[identifier]

    def removeLabels(self, identifiers: [str,]):
        prevLabels = self._labels.copy()
        try:
            for identifier in identifiers:
                self.removeLabel(identifier)
        except Exception as error:
            self._labels = prevLabels
            raise error

    def _preprocessing(self, assembly: str or [str,]) -> [[[str, str],], {int: str}]:
        if isinstance(assembly, str):
            lines = assembly.split("\n")
        else:
            lines = tuple(assembly)
        instructionCalls = list()
        labelLines = dict()
        for line in lines:
            try:
                line = line[:line.index(";")]
            except ValueError:
                pass
            if line:
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

    def _assembleLine(self, line: [str, str], labels: [str,] = tuple()) -> [AddressingMode, bytes, [[int, str]]]:
        mnemonic, operands = line
        operation = self._instructionSet.getOperationByMnemonic(mnemonic)
        for addressingMode in self._instructionSet.operationAddressingModes(operation):
            try:
                assembledOperands, labelUses = addressingMode.assemble(operands, labels)
                opcode = self._instructionSet.getOpcode(operation, addressingMode)
                return addressingMode, bytes((opcode,)) + assembledOperands, labelUses
            except AddressingMode.AddressingModeAssembleError:
                pass
        raise Assembler.AssemblerError(f"Could not identify addressing mode: '{mnemonic} {operands}'")

    def assemble(self, assembly: str or [str,], startAddress: int = 0) -> bytes:
        prevSymbols = self._symbols.copy()
        prevLabels = self._labels.copy()
        try:
            machineCode = bytes()
            lines, labels = self._preprocessing(assembly)
            labelUses = list()
            labelIdentifiers = self.labelIdentifiers + tuple(labels.values())
            for line in range(len(lines)):
                if line in labels:
                    self.addLabel(labels[line], len(machineCode) + startAddress)
                addressingMode, lineMachineCode, lineLabelUses = self._assembleLine(lines[line], labelIdentifiers)
                for byte, identifier in lineLabelUses:
                    labelUses.append((len(machineCode) + byte, identifier, addressingMode))
                machineCode += lineMachineCode
            for address, label, addressingMode in labelUses:
                assembledLabel = addressingMode.assembleLabel(self._labels[label], address + startAddress)
                machineCode = machineCode[:address] + assembledLabel + machineCode[address + len(assembledLabel):]
            return machineCode
        except Exception as error:
            self._symbols = prevSymbols
            self._labels = prevLabels
            raise error
