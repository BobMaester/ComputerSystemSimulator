def int_to_bool(value: int or bool) -> bool:
    if isinstance(value, bool):
        return value
    elif isinstance(value, int):
        if value == 0:
            return False
        elif value == 1:
            return True
        else:
            raise ValueError(f"Cannot convert {value} to bool (integers must be 1 or 0 to be converted)")
    else:
        raise TypeError(f"int_to_bool only converts integers to boolean not {type(value)} ({value})")

def bytes_to_tuple(value: bytes) -> [bool,]:
    output = list()
    for byte in value:
        for bit in range(8, 0, -1):
            output.append((byte // (2 ** bit)) == 1)
            byte %= 2 ** bit
    return tuple(output[::-1])

def slice_to_tuple(value: slice, maximum: int = None, minimum: int = 0) -> [int,]:
    start, stop, step = value.start, value.stop, value.step
    if start is None:
        start = minimum
    if stop is None:
        if maximum is None:
            raise ValueError("Cannot convert slice with no stop value to tuple if not maximum is given")
        stop = maximum
    if step is None:
        step = 1
    return tuple(range(start, stop, step))

def strToDict(string: str):
    dictionary = dict()
    string = str(string).strip()
    if string[0] == "{":
        string = string[1:]
    else:
        string += "}"
    bracketDepth = 0
    value = ""
    key = ""
    for character in string:
        if (character == "," or character == "}") and bracketDepth == 0:
            exec(f"dictionary[{key}] = {value.strip()}")
            value = key = ""
        elif character == ":":
            key = value.strip()
            value = ""
        else:
            value += character
        if character == "(" or character == "[" or character == "}":
            bracketDepth += 1
        elif character == ")" or character == "]" or character == "}":
            bracketDepth -= 1
    return dictionary

class BinaryElectric:
    @staticmethod
    def validateState(state: [bool or int, bool or int]) -> [bool, bool]:
        if len(state) != 2:
            raise ValueError(f"Binary electric states must be composed of a value and activity (not {state})")
        value, activity = state
        value = int_to_bool(value)
        activity = int_to_bool(activity)
        return value, activity

    @staticmethod
    def validState(state: [bool or int, bool or int]) -> True:
        BinaryElectric.validateState(state)
        return True

    @staticmethod
    def combine(A: [bool or int, bool or int], B: [bool or int, bool or int]) -> [bool, bool]:
        A, B = BinaryElectric.validateState(A), BinaryElectric.validateState(B)
        if A == B:
            return A
        elif A == (True, True) or B == (True, True):
            return True, True
        elif A[1] or B[1]:
            return False, True
        elif A[0] or B[0]:
            return True, False
        else:
            return False, False
