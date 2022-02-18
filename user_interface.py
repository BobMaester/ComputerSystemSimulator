class UserInterface:
    class UnknownBooleanResponseError(ValueError):
        pass

    @staticmethod
    def format(data: any, indent: int = 0) -> str:
        if isinstance(data, tuple) or isinstance(data, list):
            formattedItems = list()
            totalLength = 0
            multiLine = False
            for item in data:
                formattedItem = UserInterface.format(item, indent + 2)
                totalLength += len(formattedItem)
                if "\n" in formattedItem:
                    multiLine = True
                formattedItems.append(formattedItem)
            if totalLength + indent > 64:
                multiLine = True
            output = " " * indent
            if isinstance(data, tuple):
                output += "("
            else:
                output += "["
            if multiLine:
                for item in formattedItems:
                    output += f"\n{item},"
                output = output[:-1] + "\n" + " " * indent
            else:
                for item in formattedItems:
                    output += item[indent + 2:] + ", "
                output = output[:-2]
            if isinstance(data, tuple):
                return output + ")"
            else:
                return output + "]"
        elif isinstance(data, dict):
            formattedDict = dict()
            maxKeyLength = 0
            maxValueLength = 0
            totalLength = 0
            multiLine = False
            for key in data:
                formattedKey = UserInterface.format(key, indent + 2)[indent + 2:]
                keyLength = len(formattedKey)
                if keyLength > maxKeyLength:
                    maxKeyLength = keyLength
                workingIndent = indent + 2
                if "\n" in formattedKey:
                    workingIndent += 2
                formattedValue = UserInterface.format(data[key], workingIndent)[workingIndent:]
                valueLength = len(formattedValue)
                if valueLength > maxValueLength:
                    maxValueLength = valueLength
                totalLength += keyLength + valueLength - 1 - 2 * indent
                formattedDict[formattedKey] = formattedValue
            if (not multiLine) and (maxKeyLength + maxValueLength + indent > 57 or totalLength > 66):
                multiLine = True
            output = " " * indent + "{"
            for key in formattedDict:
                value = formattedDict[key]
                if multiLine:
                    output += "\n" + " " * (indent + 2)
                output += key
                if "\n" in key:
                    output += f"\n{indent + 2}: "
                    if "\n" in value:
                        output += f"\n{' ' * (indent + 2)}{value}"
                    else:
                        output += value
                else:
                    if multiLine:
                        output += f"{' ' * (maxKeyLength - len(key))}"
                    output += " : "
                    if "\n" in value:
                        output += value.replace("\n", "\n" + " " * (maxKeyLength + 3))
                    else:
                        output += value
                output += ", "
            output = output[:-2]
            if "\n" in output:
                output += "\n" + " " * indent
            return output + "}"
        elif isinstance(data, bytes):
            output = " " * indent
            for byte in range(len(data)):
                value = data[byte]
                for bit in range(7, -1, -1):
                    if value >= 2 ** bit:
                        value -= 2 ** bit
                        output += "1"
                    else:
                        output += "0"
                if byte % 8 == 7:
                    output += "\n" + " " * indent
                else:
                    output += " "
            return output[:-1]
        else:
            return " " * indent + str(data)

    @staticmethod
    def output(data: any = str()):
        print(UserInterface.format(data))

    @staticmethod
    def input(prompt: any = str()) -> str:
        return input(UserInterface.format(prompt))

    @staticmethod
    def booleanInput(prompt: any = str(), additionalResponses: {str: bool} = None) -> bool:
        knownResponses = {"yes": True, "no": False,
                          "true": True, "false": False,
                          "y": True, "n": False,
                          "1": True, "0": False}
        if additionalResponses is not None:
            for newResponse in additionalResponses:
                knownResponses[str(newResponse)] = bool(additionalResponses[newResponse])
        response = UserInterface.input(prompt)
        try:
            return knownResponses[response.lower().strip()]
        except KeyError:
            raise UserInterface.UnknownBooleanResponseError(f"'{response}' is not a known boolean response i.e. y/n")

    @staticmethod
    def menu(options: [str,]) -> int:
        UserInterface.output(str())
        for option in range(len(options)):
            UserInterface.output(f"{option + 1}. {options[option]}")
        while True:
            choice = UserInterface.input("> ").lower().strip()
            if choice.isnumeric():
                choiceInt = int(choice)
                if 1 <= choiceInt <= len(options):
                    return choiceInt
            for option in range(len(options)):
                if choice == options[option].lower().strip():
                    return option + 1
            UserInterface.output("/!\ INVALID SELECTION")

    @staticmethod
    def loadFile(binary: bool = False) -> [bool, str or bytes]:
        fileName = UserInterface.input("File: ")
        try:
            open(fileName).close()
        except FileNotFoundError:
            UserInterface.output("/!\ FILE NOT FOUND")
            return False, None
        if binary:
            mode = "rb"
        else:
            mode = "r"
        with open(fileName, mode) as file:
            return True, file.read()

    @staticmethod
    def saveFile(data: str or bytes, binary: bool = False) -> bool:
        fileName = UserInterface.input("File: ")
        try:
            open(fileName).close()
            while True:
                try:
                    overwrite = UserInterface.booleanInput("Overwrite? ", {"overwrite": True})
                    if overwrite:
                        break
                    else:
                        return False
                except UserInterface.UnknownBooleanResponseError:
                    UserInterface.output("/!\ COULD NOT INTERPRET")
        except FileNotFoundError:
            pass
        if binary:
            mode = "wb"
        else:
            mode = "w"
        with open(fileName, mode) as file:
            file.write(data)
        return True

    @staticmethod
    def console(**kwargs):
        for key, arg in kwargs.items():
            exec(f"{key} = arg")
            UserInterface.output(f'{key} = {arg}')
        UserInterface.output("/END to exit console\n")
        while True:
            command = UserInterface.input()
            if command.strip().lower() == "/end":
                return
            else:
                try:
                    exec(command)
                except Exception as error:
                    UserInterface.output(f"/!\ COULD NOT EXECUTE ({type(error).__name__}): {error}")
