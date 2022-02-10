from __future__ import annotations
from abc import ABC, abstractmethod
from general import int_to_bool, bytes_to_tuple, slice_to_tuple, BinaryElectric as BinElec

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
    def isComponent(potentialComponent) -> True:
        if potentialComponent is None:
            raise Component.NoComponentError()
        elif not isinstance(potentialComponent, Component):
            raise TypeError(f"All components must inherit from the component class ({type(potentialComponent).__name__} does not)")
        else:
            return True

    @staticmethod
    def normalisePinValues(pinValues: [bool or int,] or bytes):
        normalisedValues = list()
        if isinstance(pinValues, bytes):
            return bytes_to_tuple(pinValues)
        else:
            for value in pinValues:
                normalisedValues.append(int_to_bool(value))
            return tuple(normalisedValues)

    def __init__(self, pins: int or [str,], pinValues: [bool or int,] or bytes = tuple(), connections: [[Component, [[int or str, int or str],]],] = tuple()):
        self._pins = list()
        pinsIterable = pins
        if isinstance(pins, int):
            pinsIterable = range(1, pins + 1)
        for pin in pinsIterable:
            self._pins.append(Pin(self, str(pin), (False, False)))
        self._pins = tuple(self._pins)
        del self.state
        if pinValues:
            if len(pinValues) > 0:
                self.setPinsValues(slice(len(pinValues)),Component.normalisePinValues(pinValues))
        if connections:
            for component, mapping in connections:
                self.connectComponent(component, mapping)

    def __del__(self):
        try:
            for pin in self._pins:
                del pin
        except AttributeError:
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

    def _pinSelect(self, pin: int or str) -> Pin:
        return self._pins[self.pinIndex(pin) - 1]

    def pinsIndexes(self, pins: [int or str,] or slice) -> [int,]:
        if isinstance(pins, slice):
            return slice_to_tuple(pins, len(self._pins) + 1, 1)
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

    def _pinsSelect(self, pins: [int or str,] or slice) -> [Pin,]:
        pinsObjects = list()
        for index in self.pinsIndexes(pins):
            pinsObjects.append(self._pins[index - 1])
        return tuple(pinsObjects)

    def getPin(self, pin: int or str) -> bool:
        return self._pinSelect(pin).value

    def setPin(self, pin: int or str):
        self._pinSelect(pin).set(self)

    def resetPin(self, pin: int or str):
        self._pinSelect(pin).reset(self)

    def setPinValue(self, pin: int or str, value: bool or int):
        self._pinSelect(pin).setValue(self, value)

    def getPins(self, pins: [int or str,] or slice) -> [bool,]:
        values = list()
        for pin in self._pinsSelect(pins):
            values.append(pin.value)
        return tuple(values)

    def setPins(self, pins: [int or str,] or slice):
        for pin in self._pinsSelect(pins):
            pin.set(self)

    def resetPins(self, pins: [int or str,] or slice):
        for pin in self._pinsSelect(pins):
            pin.reset(self)

    def setPinsValue(self, pins: [int or str,] or slice, value: bool or int):
        for pin in self._pinsSelect(pins):
            pin.setValue(self, value)

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
        return self._pinSelect(pin).activity

    def _makePinActive(self, pin: int or str):
        self._pinSelect(pin).active(self)

    def _makePinPassive(self, pin: int or str):
        self._pinSelect(pin).passive(self)

    def _setPinActivity(self, pin: int or str, activity: bool or int):
        self._pinSelect(pin).setActivity(self, activity)

    def getPinsActivities(self, pins: [int or str, ] or slice) -> [bool, ]:
        activities = list()
        for pin in self._pinsSelect(pins):
            activities.append(pin.activity)
        return tuple(activities)

    def _makePinsActive(self, pins: [int or str,] or slice):
        for pin in self._pinsSelect(pins):
            pin.active(self)

    def _makePinsPassive(self, pins: [int or str,] or slice):
        for pin in self._pinsSelect(pins):
            pin.passive(self)

    def _setPinsActivity(self, pins: [int or str,] or slice, activity: bool or int):
        for pin in self._pinsSelect(pins):
            pin.setActivity(self, activity)

    def _setPinsActivities(self, pins: [int or str,] or slice, activities: [bool or int,] or bytes):
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
        return self._pinSelect(pin).state

    def _setPinState(self, pin: int or str, state: [bool or int, bool or int]):
        self._pinSelect(pin).setState(self, state)

    def getPinsStates(self, pins: [int or str, ] or slice) -> [[bool, bool], ]:
        states = list()
        for pin in self._pinsSelect(pins):
            states.append(pin.state)
        return tuple(states)

    def _setPinsState(self, pins: [int or str,] or slice, state: [bool or int, bool or int]):
        for pin in self._pinsSelect(pins):
            pin.setState(self, state)

    def _setPinsStates(self, pins: [int or str,] or slice, states: [[bool or int, bool or int],]):
        indexes = self.pinsIndexes(pins)
        if len(indexes) > len(states):
            raise ValueError(f"Cannot set pins states with fewer states given than pins ({self.pinsIdentifiers(indexes)} set to states: {states})")
        state = self.state
        try:
            for index in indexes:
                self._setPinState(index, states[index - 1])
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
            self._setPinsStates(slice(None), pinsState)
        except Exception as error:
            self.state = prevState
            raise error

    @state.deleter
    def state(self):
        for pin in self._pins:
            pin.setState(self, (False, False))

    def connectPin(self, pin: int or str, connectedComponent: Component, connectedPin: int or str):
        if Component.isComponent(connectedComponent):
            self._pinSelect(pin).connection = connectedComponent._pinSelect(connectedPin)

    def connectPins(self, pins: [int or str,] or slice, connectedComponent: Component, connectedPins: [int or str,] or slice):
        if Component.isComponent(connectedComponent):
            pins = self.pinsIndexes(pins)
            connectedPins = connectedComponent._pinsSelect(connectedPins)
            length = len(pins)
            if len(connectedPins) != length:
                raise ValueError(f"Cannot connect {length} pins of {self} to {len(connectedPins)} pins of {connectedComponent} (Component.connectPins makes 1:1 connections)")
            for index in range(length):
                self.connectPin(pins[index], connectedComponent, connectedPins[index])

    def disconnectPin(self, pin: int or str):
        del self._pinSelect(pin).connection

    def disconnectPins(self, pins: [int or str,] or slice):
        pins = self._pinsSelect(pins)
        for pin in pins:
            del pin.connection

    def connectComponent(self, component: Component, mapping: [[int or str, int or str],]):
        for pin1, pin2 in mapping:
            self.connectPin(pin1, component, pin2)

    @abstractmethod
    def response(self):
        pass

    def retrievePinStates(self):
        for pin in self._pins:
            pin.retrieveState(self)

    def respond(self):
        self.retrievePinStates()
        self.response()

class Node(ABC):
    def formConnection(self, connector: Connection or Node) -> Connection:
        if isinstance(connector, Connection):
            if connector.node == self:
                return ~connector
            elif (~connector).node == self:
                return connector
            else:
                raise Connection.IrrelevantConnectionError(f"Connection, {connector}, does not involve node, {self}")
        elif isinstance(connector, Node):
            return Connection(self, connector)
        else:
            raise TypeError(f"Can only form connection using type Connection or Node not {type(connector).__name__} ({connector})")

    @abstractmethod
    def retrieveState(self, exclude: [Node,]) -> [bool, bool]:
        pass

class Connection:
    class ExcludedNodeError(Exception):
        pass

    class ConnectionNotFoundError(Exception):
        pass

    class IrrelevantConnectionError(ValueError):
        pass

    class _ConnectionNode(ABC):
        _node = None

        @property
        def node(self) -> Node:
            return self._node

        @abstractmethod
        def connect(self, connector: Connection or Node):
            pass

        @abstractmethod
        def disconnect(self, connection: Connection or Node):
            pass

        @abstractmethod
        def retrieveState(self, exclude: [Node,]) -> [bool, bool]:
            pass

    class _PinConnection(_ConnectionNode):
        def __init__(self, pin: Pin):
            if isinstance(pin, Pin):
                self._node = pin
            else:
                raise TypeError(f"Only Pins can be used in a PinConnection (not {pin})")

        def connect(self, connector: Connection or Node):
            self._node.connection = connector

        def disconnect(self, connection: Connection or Node = None):
            if connection == self._node.connection:
                del self._node.connection

        def retrieveState(self, exclude: [Node,]):
            return self._node.state

    class _WireConnection(_ConnectionNode):
        def __init__(self, wire: Wire):
            if isinstance(wire, Wire):
                self._node = wire
            else:
                raise TypeError(f"Only Wires can be used in a WireConnection (not {wire})")

        def connect(self, connector: Connection or Node):
            self._node.connect(connector)

        def disconnect(self, connection: Connection or Node):
            self._node.disconnect(connection)

        def retrieveState(self, exclude: [Node,]) -> [bool, bool]:
            return self._node.retrieveState(exclude)

    def __init__(self, source: Node, target: Node, inverse: Connection = None):
        if not isinstance(target, Node):
            raise TypeError(f"Connections can only connect nodes to other nodes (not {source.__name__} to {target.__name__})")
        if isinstance(target, Pin):
            self._node = Connection._PinConnection(target)
        elif isinstance(target, Wire):
            self._node = Connection._WireConnection(target)
        else:
            raise TypeError(f"Unknown Node type, cannot connect {target.__name__}")
        if inverse is not None:
            if not isinstance(inverse, Connection):
                raise TypeError("The inverse should only be used during initialisation of a connection pair and must itself be a Connection instance")
            self._inverse = inverse
        else:
            self._inverse = Connection(target, source, self)
            self.connect(self._inverse)
            self._inverse.connect(self)

    def __del__(self):
        try:
            if self._node is not None:
                node = self._node
                self._node = None
                try:
                    node.disconnect(self)
                except Connection.ConnectionNotFoundError:
                    pass
            elif self._inverse._inverse is not None:
                del self._inverse
        except AttributeError:
            pass

    def __invert__(self) -> Connection:
        return self._inverse

    def __eq__(self, other: Connection) -> bool:
        if isinstance(other, Connection):
            return self._node == other._node
        return False

    @property
    def node(self) -> Node:
        return self._node.node

    def connect(self, connector: Connection or Node):
        self._node.connect(connector)

    def disconnect(self, connection: Connection or Node = None):
        self._node.disconnect(connection)

    def retrieveState(self, exclude: [Node,]) -> [bool, bool]:
        return self._node.retrieveState(exclude)

class Pin(Node):
    class UnauthorisedComponentError(Exception):
        pass

    def __init__(self, component: Component, identifier: str, state: [bool or int, bool or int] = (False, False), connection: Connection or Node = None):
        self._component = component
        self._identifier = str(identifier)
        self._value, self._activity = BinElec.validateState(state)
        self._connection = None
        if connection is not None:
            self.connection = connection
        Component.isComponent(component)

    def __del__(self):
        try:
            del self.connection
        except AttributeError:
            pass

    @property
    def identifier(self) -> str:
        return self._identifier

    def _authorise(self, authority: Component) -> bool:
        if authority == self._component:
            return True
        return False

    @property
    def value(self) -> bool:
        return self._value

    def set(self, authority: Component):
        self._authorise(authority)
        self._value = True

    def reset(self, authority: Component):
        self._authorise(authority)
        self._value = False

    def setValue(self, authority: Component, value: bool or int):
        self._authorise(authority)
        self._value = int_to_bool(value)

    @property
    def activity(self) -> bool:
        return self._activity

    def active(self, authority: Component):
        self._authorise(authority)
        self._activity = True

    def passive(self, authority: Component):
        self._authorise(authority)
        self._activity = False

    def setActivity(self, authority: Component, activity: bool or int):
        self._authorise(authority)
        self._activity = int_to_bool(activity)

    @property
    def state(self) -> [bool or int, bool or int]:
        return self._value, self._activity

    def setState(self, authority: Component, state: [bool or int, bool or int]):
        self._authorise(authority)
        prevValue, prevActivity = self._value, self._activity
        try:
            self._value, self._activity = int_to_bool(state[0]), int_to_bool(state[1])
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

    def retrieveState(self, authority: Component = None, exclude: [Node,] = tuple()) -> [bool, bool]:
        self._authorise(authority)
        if self._connection is None:
            self._value = self._activity = False
        else:
            state = self._connection.retrieveState(list(exclude) + [self])
            self._value, self._activity = BinElec.validateState(state)
        return self.state

class Wire(Node):
    def __init__(self, connections: [Connection or Node,]):
        self._connections = list()
        self.connections = connections

    def __del__(self):
        try:
            del self.connections
        except AttributeError:
            pass

    def __len__(self) -> int:
        return len(self._connections)

    @property
    def connections(self) -> [Connection,]:
        return tuple(self._connections)

    @connections.setter
    def connections(self, connectors: [Connection or Node,]):
        prevConnections = self._connections
        del self.connections
        try:
            for connector in connectors:
                self.connect(connector)
        except Exception as error:
            self.connections = prevConnections
            raise error

    @connections.deleter
    def connections(self):
        for connection in self._connections:
            del connection

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
        raise ValueError(f"Cannot identify connections using type {type(identifier).__name__} ({identifier})")

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
            raise Connection.ExcludedNodeError(f"{self} is already excluded in {exclude}")
        exclude = list(exclude)
        exclude.append(self)
        state = (False, False)
        for connection in self._connections:
            if connection.node not in exclude:
                state = BinElec.combine(state, connection.retrieveState(exclude))
            if state == (True, True):
                break
        return state

    def __getitem__(self, identifier: Connection or Node or int) -> Connection:
        return self.getConnection(identifier)

    def __delitem__(self, identifier: Connection or Node or int):
        self.disconnect(identifier)
