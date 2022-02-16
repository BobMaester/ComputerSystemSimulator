from component import Component
from abc import abstractmethod
from general import bytesToTuple, sliceToTuple

class Memory(Component):
    class InvalidMemoryAddressError(IndexError):
        pass

    @abstractmethod
    def __init__(self, pins: [str,] or int, data: [bytes,] or bytes or str = bytes(), pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        self._data = bytes()
        super().__init__(pins, pinValues, connections)
        if data:
            if isinstance(data, str):
                self.load(data)
            else:
                self.writeAddresses(slice(len(data)), data)

    @abstractmethod
    def __len__(self) -> int:
        pass

    def validateAddress(self, address: int or bytes) -> int:
        if isinstance(address, bytes):
            address = int.from_bytes(address, "big")
        elif not isinstance(address, int):
            raise TypeError(f"Address must be int or bytes, not type {type(address).__name__} ({address})")
        if 0 <= address < len(self):
            return address
        else:
            raise ValueError(f"Address {address} is out of range")

    def validateAddresses(self, addresses: [int or bytes,] or slice) -> [int,]:
        if isinstance(addresses, slice):
            addresses = sliceToTuple(addresses, len(self))
        validatedAddresses = list()
        for address in addresses:
            validatedAddresses.append(self.validateAddress(address))
        return tuple(validatedAddresses)

    @abstractmethod
    def read(self, address: int or bytes) -> bytes:
        pass

    @abstractmethod
    def write(self, address: int or bytes, value: bytes):
        pass

    @abstractmethod
    def readAddresses(self, addresses: [int or bytes,] or slice) -> [bytes,]:
        pass

    @abstractmethod
    def writeAddresses(self, addresses: [int or bytes,] or slice, values: [bytes,] or bytes):
        pass

    def __getitem__(self, addresses: int or bytes or [int or bytes,] or slice) -> bytes or [bytes,]:
        if isinstance(addresses, int) or isinstance(addresses, bytes):
            return self.read(addresses)
        else:
            return self.readAddresses(addresses)

    def __setitem__(self, addresses: int or bytes or [int or bytes,] or slice, values: bytes or [bytes,]):
        if isinstance(addresses, int) or isinstance(addresses, bytes):
            return self.write(addresses, values)
        else:
            return self.writeAddresses(addresses, values)

    @property
    def data(self) -> bytes:
        return self.readAddresses(slice(None))

    @data.setter
    def data(self, data: bytes or [bytes,]):
        self.writeAddresses(slice(None), data)

    @data.deleter
    def data(self):
        self.writeAddresses(slice(None), bytes())

    def save(self, fileName: str):
        with open(fileName, "wb") as file:
            file.write(self.data)

    def load(self, fileName: str):
        with open(fileName, "rb") as file:
            self.data = file.read(len(self))

    @property
    def state(self) -> {str: any}:
        state = Component.state.__get__(self)
        state["data"] = self.data
        return state

    @state.setter
    def state(self, state: {str: any}):
        prevState = self.state
        Component.state.__set__(self, state)
        try:
            dataState = state["data"]
        except KeyError:
            raise Component.StateError("data", state)
        try:
            self.data = dataState
        except Exception as error:
            self.state = prevState
            raise error

    @state.deleter
    def state(self):
        Component.state.__delete__(self)
        del self.data

class SpecificMemory(Memory):
    def __init__(self, pins: [str,] or int, data: [bytes,] or bytes or str = bytes(), pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        self._data = bytes()
        super().__init__(pins, data, pinValues, connections)

    def __len__(self) -> int:
        return 32768 # == 2 ** 15

    def read(self, address: int or bytes) -> bytes:
        address = self.validateAddress(address)
        return self._data[address : address + 1]

    def write(self, address: int or bytes, value: bytes):
        if not isinstance(value, bytes):
            raise TypeError(f"Can only write bytes type data to memory not {type(value).__name__} ({value})")
        if len(value) != 1:
            raise ValueError(f"Memory addresses of {type(self).__name__} only store one byte")
        address = self.validateAddress(address)
        self._data = self._data[:address] + value + self._data[address + 1:]

    def readAddresses(self, addresses: [int or bytes,] or slice) -> [bytes,]:
        addresses = self.validateAddresses(addresses)
        data = list()
        for address in addresses:
            data.append(self.read(address))
        return tuple(data)

    def writeAddresses(self, addresses: [int or bytes,] or slice, values: [bytes,] or bytes):
        addresses = self.validateAddresses(addresses)
        for index in range(len(addresses)):
            self.write(addresses[index], values[index : index + 1])

    @property
    def data(self) -> bytes:
        return self._data

    @data.setter
    def data(self, data: bytes or [bytes,]):
        if isinstance(data, bytes):
            if len(data) != len(self._data):
                raise ValueError(f"Data is incorrect length (cannot set as {data})")
            self._data = data
        else:
            unaddressedData = bytes()
            for address in data:
                unaddressedData += address
            self.data = unaddressedData

    @data.deleter
    def data(self):
        self._data = bytes(2 ** 15)

    def response(self):
        high, low = self.getPinsStates((28, 14))
        self.makePinsPassive(slice(None))
        if self.getPin(20) == high[0]:
            addressPins = 10, 9, 8, 7, 6, 5, 4, 3, 25, 24, 21, 23, 2, 26, 1
            dataPins = 11, 12, 13, 15, 16, 17, 18, 19
            address = 0
            for bit in range(15):
                address += self.getPin(addressPins[bit]) * (2 ** bit)
            modePins = self.getPins((22, 27))
            if modePins == (high[0], low[0]):
                data = 0
                for bit in range(8):
                    data += self.getPin(dataPins[bit] * (2 ** bit))
                self.write(address, bytes([data]))
            elif modePins == (low[0], high[0]):
                data = bytesToTuple(self.read(address))[::-1]
                for bit in range(8):
                    if data[bit]:
                        self.setPinState(dataPins[bit], high)
                    else:
                        self.setPinState(dataPins[bit], low)

class ReadOnlyMemory(SpecificMemory):
    def __init__(self, data: [bytes,] or bytes or str = bytes(), pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        super().__init__(
            (
                "A14",  "A12",  "A7",   "A6",   "A5",   "A4",   "A3",
                "A2",   "A1",   "A0",   "I/O0", "I/O1", "I/O2", "GND",
                "I/O3", "I/O4", "I/O5", "I/O6", "I/O7", "CEB",  "A10",
                "OEB",  "A11",  "A9",   "A8",   "A13",  "WEB",  "VCC"
            ),
            data, pinValues, connections)

class RandomAccessMemory(SpecificMemory):
    def __init__(self, data: [bytes,] or bytes or str = bytes(), pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        super().__init__(
            (
                "A14",  "A12",  "A7",   "A6",   "A5",   "A4",   "A3",
                "A2",   "A1",   "A0",   "I/O0", "I/O1", "I/O2", "Vss",
                "I/O3", "I/O4", "I/O5", "I/O6", "I/O7", "CSB",  "A10",
                "OEB",  "A11",  "A9",   "A8",   "A13",  "WEB",  "Vcc"
            ),
            data, pinValues, connections)

    def response(self):
        if not self.getPin(28):
            del self.data
            self.makePinsPassive(slice(None))
        else:
            super().response()
