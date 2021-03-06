from __future__ import annotations
from abc import ABC, abstractmethod
from general import intToBool, bytesToTuple, sliceToTuple, BinaryElectric as BinElec

class Component(ABC):
    class PinNotFoundError(KeyError):
        def __init__(self, identifier: str):
            super().__init__(f"No pin with identifier: {identifier}")

    class PinIndexError(IndexError):
        def __init__(self, index: int, maxIndex: int):
            super().__init__(f"Pin index, {index}, is not in pin range (1 <= index <= {maxIndex})")

    class NoComponentError(TypeError):
        def __init__(self):
            super().__init__("The component given is None (there is no component)")

    class StateError(KeyError):
        def __init__(self, key: str, state: {str: any}):
            super().__init__(f"Insufficient data to load state ({state} has no '{key}' state)")

    @staticmethod
    def isComponent(potentialComponent: Component) -> True:
        if potentialComponent is None:
            raise Component.NoComponentError()
        elif not isinstance(potentialComponent, Component):
            raise TypeError(f"All components must inherit from the component class ({type(potentialComponent).__name__} does not)")
        else:
            return True

    @staticmethod
    def normalisePinValues(pinValues: [bool or int,] or bytes) -> [bool,]:
        if isinstance(pinValues, bytes):
            return bytesToTuple(pinValues)
        else:
            normalisedValues = list()
            for value in pinValues:
                normalisedValues.append(intToBool(value))
            return tuple(normalisedValues)

    def __init__(self, pins: int or [str,], pinValues: [bool or int,] or bytes = bytes(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        self._pins = list()
        pinsIterable = pins
        if isinstance(pins, int):
            pinsIterable = range(1, pins + 1)
        for pin in pinsIterable:
            self._pins.append(Pin(str(pin), (False, False)))
        self._pins = tuple(self._pins)
        del self.state
        if pinValues:
            if len(pinValues) > 0:
                self.setPinsValues(slice(len(pinValues)),Component.normalisePinValues(pinValues))
        self.connectComponents(connections)

    def __del__(self):
        try:
            pins = self._pins
            self._pins = None
            for pin in pins:
                try:
                    del pin
                except:
                    pass
        except:
            pass

    @property
    def pins(self) -> [str,]:
        pinNames = list()
        for pin in self._pins:
            pinNames.append(pin.identifier)
        return pinNames

    @property
    def pinCount(self) -> int:
        return len(self._pins)

    @property
    def activePins(self) -> [str,]:
        activePins = list()
        for pin in self._pins:
            if pin.activity:
                activePins.append(pin.identifier)
        return tuple(activePins)

    def pinIndex(self, pin: int or str) -> int:
        if isinstance(pin, int):
            if 1 <= pin <= len(self._pins):
                return pin
            raise Component.PinIndexError(pin, len(self._pins))
        else:
            identifier = str(pin)
            for index in range(len(self._pins)):
                if identifier == self._pins[index].identifier:
                    return index + 1
            raise Component.PinNotFoundError(identifier)

    def pinIdentifier(self, pin: int or str) -> str:
        return self._pins[self.pinIndex(pin)].identifier

    def pinSelect(self, pin: int or str) -> Pin:
        return self._pins[self.pinIndex(pin) - 1]

    def pinsIndexes(self, pins: [int or str,] or slice) -> [int,]:
        if isinstance(pins, slice):
            return sliceToTuple(pins, len(self._pins) + 1, 1)
        else:
            indexes = list()
            for pin in pins:
                indexes.append(self.pinIndex(pin))
            return tuple(indexes)

    def pinsIdentifiers(self, pins: [int or str,] or slice) -> [str,]:
        indexes = self.pinsIndexes(pins)
        identifiers = list()
        for index in indexes:
            identifiers.append(self._pins[index - 1].identifier)
        return identifiers

    def pinsSelect(self, pins: [int or str,] or slice) -> [Pin,]:
        pinsObjects = list()
        for index in self.pinsIndexes(pins):
            pinsObjects.append(self._pins[index - 1])
        return tuple(pinsObjects)

    def getPin(self, pin: int or str) -> bool:
        return self.pinSelect(pin).value

    def setPin(self, pin: int or str):
        self.pinSelect(pin).set()

    def resetPin(self, pin: int or str):
        self.pinSelect(pin).reset()

    def setPinValue(self, pin: int or str, value: bool or int):
        self.pinSelect(pin).value = value

    def getPins(self, pins: [int or str,] or slice) -> [bool,]:
        values = list()
        for pin in self.pinsSelect(pins):
            values.append(pin.value)
        return tuple(values)

    def setPins(self, pins: [int or str,] or slice):
        for pin in self.pinsSelect(pins):
            pin.set()

    def resetPins(self, pins: [int or str,] or slice):
        for pin in self.pinsSelect(pins):
            pin.reset()

    def setPinsValue(self, pins: [int or str,] or slice, value: bool or int):
        for pin in self.pinsSelect(pins):
            pin.value = value

    def setPinsValues(self, pins: [int or str,] or slice, values: [bool or int,] or bytes):
        values = Component.normalisePinValues(values)
        indexes = self.pinsIndexes(pins)
        if len(indexes) > len(values):
            raise ValueError(f"Cannot set pins values with fewer values given than pins ({self.pinsIdentifiers(indexes)} set to values: {values})")
        state = self.state
        try:
            for index in indexes:
                self._pins[index].value = values[index]
        except Exception as error:
            self.state = state
            raise error

    def getPinActivity(self, pin: int or str) -> bool:
        return self.pinSelect(pin).activity

    def makePinActive(self, pin: int or str):
        self.pinSelect(pin).active()

    def makePinPassive(self, pin: int or str):
        self.pinSelect(pin).passive()

    def setPinActivity(self, pin: int or str, activity: bool or int):
        self.pinSelect(pin).activity = activity

    def getPinsActivities(self, pins: [int or str,] or slice) -> [bool,]:
        activities = list()
        for pin in self.pinsSelect(pins):
            activities.append(pin.activity)
        return tuple(activities)

    def makePinsActive(self, pins: [int or str,] or slice):
        for pin in self.pinsSelect(pins):
            pin.active()

    def makePinsPassive(self, pins: [int or str,] or slice):
        for pin in self.pinsSelect(pins):
            pin.passive()

    def setPinsActivity(self, pins: [int or str,] or slice, activity: bool or int):
        for pin in self.pinsSelect(pins):
            pin.activity = activity

    def setPinsActivities(self, pins: [int or str,] or slice, activities: [bool or int,] or bytes):
        activities = Component.normalisePinValues(activities)
        indexes = self.pinsIndexes(pins)
        if len(indexes) > len(activities):
            raise ValueError(f"Cannot set pins activities with fewer activities given than pins ({self.pinsIdentifiers(indexes)} set to activities: {activities})")
        state = self.state
        try:
            for index in indexes:
                self._pins[index].activity = activities[index]
        except Exception as error:
            self.state = state
            raise error

    def getPinState(self, pin: int or str) -> [bool, bool]:
        return self.pinSelect(pin).state

    def setPinState(self, pin: int or str, state: [bool or int, bool or int]):
        self.pinSelect(pin).state = state

    def getPinsStates(self, pins: [int or str,] or slice) -> [[bool, bool],]:
        states = list()
        for pin in self.pinsSelect(pins):
            states.append(pin.state)
        return tuple(states)

    def setPinsState(self, pins: [int or str,] or slice, state: [bool or int, bool or int]):
        for pin in self.pinsSelect(pins):
            pin.state = state

    def setPinsStates(self, pins: [int or str,] or slice, states: [[bool or int, bool or int],]):
        indexes = self.pinsIndexes(pins)
        if len(indexes) > len(states):
            raise ValueError(f"Cannot set pins states with fewer states given than pins ({self.pinsIdentifiers(indexes)} set to states: {states})")
        state = self.state
        try:
            for index in indexes:
                self.setPinState(index, states[index - 1])
        except Exception as error:
            self.state = state
            raise error

    @property
    def state(self) -> {str: any}:
        return {"pins": self.getPinsStates(slice(None))}

    @state.setter
    def state(self, state: {str: any}):
        prevState = self.state
        try:
            pinsState = state["pins"]
        except KeyError:
            raise Component.StateError("pins", state)
        try:
            self.setPinsStates(slice(None), pinsState)
        except Exception as error:
            self.state = prevState
            raise error

    @state.deleter
    def state(self):
        for pin in self._pins:
            pin.state = (False, False)

    def connectPin(self, pin: int or str, connectedComponent: Component, connectedPin: int or str):
        if Component.isComponent(connectedComponent):
            nodes = [self.pinSelect(pin), connectedComponent.pinSelect(connectedPin)]
            for node in range(2):
                existingConnection = nodes[node].connection
                if existingConnection is not None:
                    if isinstance(existingConnection.node, Wire):
                        nodes[node] = existingConnection.node
                    else:
                        nodes[node] = Wire((nodes[node], existingConnection.node))
            Connection.createConnection(nodes[0], nodes[1])

    def connectPins(self, pins: [int or str,] or slice, connectedComponent: Component, connectedPins: [int or str,] or slice):
        if Component.isComponent(connectedComponent):
            pins = self.pinsIndexes(pins)
            connectedPins = connectedComponent.pinsSelect(connectedPins)
            length = len(pins)
            if len(connectedPins) != length:
                raise ValueError(f"Cannot connect {length} pins of {self} to {len(connectedPins)} pins of {connectedComponent} (Component.connectPins makes 1:1 connections)")
            for index in range(length):
                self.connectPin(pins[index], connectedComponent, connectedPins[index])

    def disconnectPin(self, pin: int or str):
        del self.pinSelect(pin).connection

    def disconnectPins(self, pins: [int or str,] or slice):
        pins = self.pinsSelect(pins)
        for pin in pins:
            del pin.connection

    def connectComponent(self, component: Component, mapping: [[int or str, int or str],]):
        for pin1, pin2 in mapping:
            self.connectPin(pin1, component, pin2)

    def connectComponents(self, connections: [[Component, [[int or str, int or str],]]]):
        for component, mapping in connections:
            self.connectComponent(component, mapping)

    def retrievePinStates(self):
        for pin in self._pins:
            pin.retrieveState()

    @abstractmethod
    def response(self):
        pass

    def respond(self):
        self.retrievePinStates()
        self.response()

class Connection(ABC):
    connectionTypes = dict()

    class ConnectionNotFoundError(ValueError):
        pass

    class IrrelevantConnectionError(ValueError):
        pass

    class WrongConnectionTypeError(TypeError):
        def __init__(self, expectedType: type, givenType: type):
            super().__init__(f"{expectedType.__name__} connections cannot be formed using type {givenType.__name__}")

    @staticmethod
    def createConnection(source: Node, target: Node, inverse: Connection = None) -> Connection:
        try:
            return Connection.connectionTypes[type(target)](source, target, inverse)
        except KeyError:
            raise TypeError(f"No known connection type for node type {type(target)}")

    @abstractmethod
    def __init__(self, source: Node, target: Node, inverse: Connection = None):
        self._node = target
        self._inverse = None
        if inverse is not None:
            if not isinstance(inverse, Connection):
                raise TypeError("The inverse should only be used during initialisation of a connection pair and must itself be a Connection instance")
            if inverse._inverse is not None:
                raise ValueError(f"Cannot initialise Connection: inverse connection, {inverse}, already has an inverse")
            self._inverse = inverse
        else:
            self._inverse = Connection.createConnection(target, source, self)
            self.connect(self._inverse)
            self._inverse.connect(self)

    def __del__(self):
        try:
            self.disconnect(self)
            inverse = self._inverse
            self._inverse = None
            del inverse
        except:
            pass

    def __invert__(self) -> Connection:
        return self._inverse

    def __eq__(self, other: Connection) -> bool:
        if isinstance(other, type(self)):
            return self._node == other._node
        return False

    @property
    def node(self) -> Node:
        return self._node

    @abstractmethod
    def connect(self, connector: Connection or Node):
        pass

    @abstractmethod
    def disconnect(self, identifier: Connection or Node):
        pass

    @abstractmethod
    def retrieveState(self, exclude: [Node,]) -> [bool, bool]:
        pass

class Node(ABC):
    class ExcludedNodeError(Exception):
        pass

    SpecificConnection = Connection

    def formConnection(self, connector: Connection or Node) -> Connection:
        if isinstance(connector, Connection):
            if connector.node == self:
                return ~connector
            elif (~connector).node == self:
                return connector
            else:
                raise Connection.IrrelevantConnectionError(f"Connection, {connector}, does not involve node, {self}")
        elif isinstance(connector, Node):
            return Connection.createConnection(self, connector)
        else:
            raise TypeError(f"Can only form connection using type Connection or Node not {type(connector).__name__} ({connector})")

    @abstractmethod
    def retrieveState(self, exclude: [Node,]) -> [bool, bool]:
        pass

class Pin(Node):
    class SpecificConnection(Connection):
        def __init__(self, source: Node, target: Node, inverse: Connection = None):
            if not isinstance(target, Pin):
                raise Connection.WrongConnectionTypeError(type(self), type(target))
            super().__init__(source, target, inverse)
            self._node = target

        def connect(self, connector: Connection or Node):
            self._node.connection = connector

        def disconnect(self, identifier: Connection or Node = None):
            if identifier is not None:
                if isinstance(identifier, Connection):
                    if identifier != self and identifier != ~self:
                        raise Connection.ConnectionNotFoundError(f"Pin's connection is not {identifier}")
                elif isinstance(identifier, Node):
                    if identifier != (~self)._node:
                        raise Connection.ConnectionNotFoundError(f"Pins is not connected to node {identifier}")
            del self._node.connection

        def retrieveState(self, exclude: [Node,]) -> [bool, bool]:
            if self._node in exclude:
                raise Node.ExcludedNodeError
            return self._node.state

    def __init__(self, identifier: str, state: [bool or int, bool or int] = (False, False), connection: Connection or Node = None):
        self._identifier = str(identifier)
        self._value, self._activity = BinElec.validateState(state)
        self._connection = None
        if connection is not None:
            self.connection = connection

    def __del__(self):
        try:
            del self.connection
        except:
            pass

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, value: bool or int):
        self._value = intToBool(value)

    def set(self):
        self._value = True

    def reset(self):
        self._value = False

    @property
    def activity(self) -> bool:
        return self._activity

    @activity.setter
    def activity(self, activity: bool or int):
        self._activity = intToBool(activity)

    def active(self):
        self._activity = True

    def passive(self):
        self._activity = False

    @property
    def state(self) -> [bool or int, bool or int]:
        return self._value, self._activity

    @state.setter
    def state(self, state: [bool or int, bool or int]):
        prevValue, prevActivity = self._value, self._activity
        try:
            self._value, self._activity = BinElec.validateState(state)
        except Exception as error:
            self._value, self._activity = prevValue, prevActivity
            raise error

    @property
    def connection(self) -> Connection:
        return self._connection

    @connection.setter
    def connection(self, connector: Connection or Node):
        newConnection = self.formConnection(connector)
        if newConnection != self._connection:
            del self.connection
            self._connection = newConnection

    @connection.deleter
    def connection(self):
        if self._connection is not None:
            connection = self._connection
            self._connection = None
            del connection

    def retrieveState(self, exclude: [Node,] = tuple()) -> [bool, bool]:
        if self in exclude:
            raise Node.ExcludedNodeError(f"{self} is already excluded in {exclude}")
        if self._connection is None:
            self._value = self._activity = False
        else:
            self._value, self._activity = BinElec.validateState(self._connection.retrieveState(tuple(list(exclude) + [self])))
        return self.state

class Wire(Node):
    class SpecificConnection(Connection):
        def __init__(self, source: Node, target: Node, inverse: Connection = None):
            if not isinstance(target, Wire):
                raise Connection.WrongConnectionTypeError(type(self), type(target))
            super().__init__(source, target, inverse)
            self._node = target

        def connect(self, connector: Connection or Node):
            self._node.connect(connector)

        def disconnect(self, identifier: Connection or Node):
            self._node.disconnect(identifier)

        def retrieveState(self, exclude: [Node,]) -> [bool, bool]:
            return self._node.retrieveState(exclude)

    def __init__(self, connections: [Connection or Node,] = tuple()):
        self._connections = list()
        self.connections = connections

    def __del__(self):
        try:
            del self.connections
        except:
            pass

    def __len__(self) -> int:
        return len(self._connections)

    @property
    def connections(self) -> [Connection,]:
        return tuple(self._connections)

    @connections.setter
    def connections(self, connectors: [Connection or Node,]):
        prevConnections = list()
        for connection in self._connections:
            prevConnections.append(connection.node)
        del self.connections
        try:
            for connector in connectors:
                self.connect(connector)
        except Exception as error:
            self.connections = prevConnections
            raise error

    @connections.deleter
    def connections(self):
        connections = self._connections
        self._connections = list()
        for connection in connections:
            connection.disconnect(self)

    def getConnection(self, identifier: Connection or Node or int) -> Connection:
        if isinstance(identifier, Connection):
            connection = identifier
            if connection.node == self:
                connection = ~connection
            if connection in self._connections:
                return connection
            raise Connection.ConnectionNotFoundError(f"{connection} not in {self._connections}")
        elif isinstance(identifier, Node):
            node = identifier
            for connection in self._connections:
                if connection.node == node:
                    return connection
            raise Connection.ConnectionNotFoundError(f"No connection to {node} in {self._connections}")
        elif isinstance(identifier, int):
            return self._connections[identifier]
        raise TypeError(f"Cannot identify connections using type {type(identifier).__name__} ({identifier})")

    def connect(self, connector: Connection or Node):
        connection = self.formConnection(connector)
        if not connection in self._connections:
            self._connections.append(connection)

    def disconnect(self, identifier: Connection or Node or int):
        connection = self.getConnection(identifier)
        self._connections.remove(connection)
        del connection

    def retrieveState(self, exclude: [Node,] = tuple()) -> [bool, bool]:
        if self in exclude:
            raise Node.ExcludedNodeError(f"{self} is already excluded in {exclude}")
        exclude = list(exclude)
        exclude.append(self)
        state = (False, False)
        for connection in self._connections:
            if connection.node not in exclude:
                state = BinElec.combine(state, connection.retrieveState(exclude))
            if state == (True, True):
                return True, True
        return state

    def __getitem__(self, identifier: Connection or Node or int) -> Connection:
        return self.getConnection(identifier)

    def __delitem__(self, identifier: Connection or Node or int):
        self.disconnect(identifier)

Connection.connectionTypes = {Pin: Pin.SpecificConnection, Wire: Wire.SpecificConnection}
