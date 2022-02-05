from user_interface import UserInterface
from assembler import Assembler
from component import Component

class Simulator:
    def __init__(self, components: {str: Component} = None, step: callable = lambda components: None, assemblers: {str: Assembler} = None):
        self._components = dict()
        if isinstance(components, dict):
            for key in components:
                component = components[key]
                if Component.isComponent(component):
                    key = str(key).strip()
                    if not key.isalnum():
                        acceptable = True
                        for character in key:
                            if not character.isalnum():
                                if character not in (" ", "_"):
                                    acceptable = False
                                    break
                        if not acceptable:
                            raise ValueError(f"Component identifier must not contain symbols ({key})")
                    self._components[key] = component
        elif components is not None:
            raise TypeError(f"Components must be given as a dictionary where the key is an identifier used in menus ({components} is not valid)")
        self._step = step
        self._assemblers = dict()
        if isinstance(assemblers, dict):
            for key in assemblers:
                assembler = assemblers[key]
                if not isinstance(assembler, Assembler):
                    raise TypeError(f"{assembler} of type {type(assembler).__name__} is not a valid assembler (does not inherit from Assembler)")
                else:
                    self._assemblers[str(key)] = assembler
        elif assemblers is not None:
            raise TypeError(f"Assemblers must be given as a dictionary where the key is an identifier used in menus ({assemblers} is not valid)")

    @property
    def componentDict(self) -> {str: Component}:
        return self._components.copy()

    @property
    def components(self) -> [Component,]:
        return tuple(self._components.values())

    @property
    def componentNames(self) -> [str,]:
        return tuple(self._components.keys())

    def identifyComponent(self, identifier: Component or str or int) -> str:
        if isinstance(identifier, str):
            return identifier
        elif isinstance(identifier, Component):
            return self.componentNames[self.components.index(identifier)]
        elif isinstance(identifier, int):
            return self.componentNames[identifier - 1]
        else:
            raise TypeError(f"Cannot identify Component using {identifier} of type {type(identifier).__name__}")

    def getComponent(self, identifier: Component or str or int) -> Component:
        return self._components[self.identifyComponent(identifier)]

    def addComponent(self, name: str, component: Component):
        self._components[name] = component

    def removeComponent(self, identifier: Component or str or int) -> Component:
        key = self.identifyComponent(identifier)
        component = self._components[key]
        self._components.pop(key)
        return component

    @property
    def assemblerDict(self) -> {str: Assembler}:
        return self._assemblers.copy()

    @property
    def assemblers(self) -> [Assembler,]:
        return tuple(self._assemblers.values())

    @property
    def assemblerNames(self) -> [str,]:
        return tuple(self._assemblers.keys())

    def identifyAssembler(self, identifier: Assembler or str or int) -> str:
        if isinstance(identifier, str):
            return identifier
        elif isinstance(identifier, Assembler):
            return self.assemblerNames[self.assemblers.index(identifier)]
        elif isinstance(identifier, int):
            return self.assemblerNames[identifier - 1]
        else:
            raise TypeError(f"Cannot identify Assembler using {identifier} of type {type(identifier).__name__}")

    def getAssembler(self, identifier: Assembler or str or int) -> Assembler:
        return self._assemblers[self.identifyAssembler(identifier)]

    def addAssembler(self, name: str, assembler: Assembler):
        self._assemblers[name] = assembler

    def removeAssembler(self, identifier: Assembler or str or int) -> Assembler:
        key = self.identifyAssembler(identifier)
        assembler = self._assemblers[key]
        self._assemblers.pop(key)
        return assembler

    def step(self):
       self._step(self._components)

    def runSteps(self):
        while True:
            try:
                steps = int(UserInterface.input("Steps: "))
                for step in range(0, steps):
                    self.step()
                return
            except TypeError:
                UserInterface.output("/!\ STEPS MUST BE AN INTEGER")

    def stateMenu(self, component) -> bool:
        component = self.getComponent(component)
        UserInterface.output(component.state)
        menuOptions = ("Raw state",
                       "Load state",
                       "Back",
                       "Return to menu")
        while True:
            choice = UserInterface.menu(menuOptions)
            if choice == 1:
                UserInterface.output(str(component.state))
            elif choice == 2:
                prevState = component.state
                state = UserInterface.input("State = ")
                try:
                    component.state = UserInterface.strToDict(state)
                except Exception as error:
                    UserInterface.output(f"/!\ COULD NOT LOAD STATE ({type(error).__name__}): {error}")
                    component.state = prevState
            elif choice == 3:
                return False
            elif choice == 4:
                return True
            else:
                UserInterface.output("/!\ UNKNOWN MENU ERROR")

    def componentMenu(self, component) -> bool:
        menuOptions = ("State",
                       "Call method",
                       "Delete component",
                       "Component select",
                       "Return to menu")
        while True:
            choice = UserInterface.menu(menuOptions)
            if choice == 1:
                returnDepth = self.stateMenu(component)
                if returnDepth:
                    return True
            elif choice == 2:
                componentName = self.identifyComponent(component)
                component = self._components[componentName]
                componentName = componentName.replace(" ", "_")
                if componentName[0].isnumeric():
                    componentName = "_" + componentName
                exec(f"UserInterface.console({componentName} = component)")
            elif choice == 3:
                component = self.removeComponent(component)
                del component
                return False
            elif choice == 4:
                return False
            elif choice == 5:
                return True
            else:
                UserInterface.output("/!\ UNKNOWN MENU ERROR")

    def componentsSelect(self):
        while True:
            if len(self._components) == 0:
                return
            menuOptions = self.componentNames + ("Return to menu",)
            choice = UserInterface.menu(menuOptions)
            if choice == len(menuOptions):
                return
            elif choice > len(menuOptions) or choice < 1:
                UserInterface.output("/!\ UNKNOWN MENU ERROR")
            else:
                returnDepth = self.componentMenu(self.getComponent(choice))
                if returnDepth:
                    return

    @staticmethod
    def machineCodeMenu(machineCode) -> bool:
        menuOptions = ("Save to file",
                       "Restart assembler",
                       "Return to menu")
        while True:
            choice = UserInterface.menu(menuOptions)
            if choice == 1:
                UserInterface.saveFile(machineCode, True)
            elif choice == 2:
                return False
            elif choice == 3:
                return True
            else:
                UserInterface.output("/!\ UNKNOWN MENU ERROR")

    @staticmethod
    def normaliseAssembly(assembly: str or [str,]) -> [str,]:
        if isinstance(assembly, str):
            if assembly[-1] == "\n":
                assembly = assembly[:-1]
            return assembly.split("\n")
        else:
            return list(assembly)

    @staticmethod
    def displayAssembly(assembly: str or [str,]):
        assembly = Simulator.normaliseAssembly(assembly)
        for line in range(len(assembly)):
            UserInterface.output(f"{line + 1}:  {assembly[line]}")

    @staticmethod
    def writeAssembly(existingAssembly: str or [str,] = tuple()) -> [str,]:
        UserInterface.output("/UNDO to delete line\n/END to finish program\n")
        assembly = list()
        if existingAssembly:
            assembly = Simulator.normaliseAssembly(existingAssembly)
            Simulator.displayAssembly(assembly)
        while True:
            line = UserInterface.input(f"{len(assembly) + 1}:  ")
            if line.strip().lower() == "/end":
                UserInterface.output()
                return tuple(assembly)
            elif line.strip().lower() == "/undo":
                if len(assembly) == 0:
                    UserInterface.output("/!\ NO LINE TO UNDO")
                else:
                    del assembly[len(assembly) - 1]
                    UserInterface.output("LINE UNDONE")
            else:
                assembly += Simulator.normaliseAssembly(line)

    def assemblyMenu(self, assembly: str or [str,], assembler: Assembler) -> bool:
        assembly = Simulator.normaliseAssembly(assembly)
        Simulator.displayAssembly(assembly)
        menuOptions = ("Save to file",
                       "Assemble",
                       "Continue writing",
                       "Discard")
        while True:
            choice = UserInterface.menu(menuOptions)
            if choice == 1:
                strAssembly = ""
                for line in assembly:
                    strAssembly += line + "\n"
                UserInterface.saveFile(strAssembly)
            elif choice == 2:
                assembler = self.getAssembler(assembler)
                startAddress = UserInterface.input("Start address: ")
                try:
                    startAddress = int(startAddress)
                    try:
                        machineCode = assembler.assemble(assembly, startAddress)
                        UserInterface.output(machineCode)
                        return Simulator.machineCodeMenu(machineCode)
                    except Exception as error:
                        UserInterface.output(f"/!\ COULD NOT ASSEMBLE ({type(error).__name__}): {error}")
                except ValueError:
                    UserInterface.output("/!\ START ADDRESS MUST BE AN INTEGER")
            elif choice == 3:
                assembly = Simulator.writeAssembly(assembly)
            elif choice == 4:
                return False
            else:
                UserInterface.output("/!\ UNKNOWN MENU ERROR")

    def assemblerMenu(self, assembler) -> bool:
        menuOptions = ("Assemble from file",
                       "Write assembly",
                       "Remove instruction set",
                       "Instruction set select",
                       "Return to menu")
        while True:
            choice = UserInterface.menu(menuOptions)
            if choice == 1:
                success, assembly = UserInterface.loadFile()
                if success:
                    assembly = Simulator.normaliseAssembly(assembly)
                    returnDepth = self.assemblyMenu(assembly, assembler)
                    if returnDepth:
                        return True
            elif choice == 2:
                assembly = Simulator.writeAssembly()
                returnDepth = self.assemblyMenu(assembly, assembler)
                if returnDepth:
                  return True
            elif choice == 3:
                self.removeAssembler(assembler)
                return False
            elif choice == 4:
                return False
            elif choice == 5:
                return True
            else:
                UserInterface.output("/!\ UNKNOWN MENU ERROR")

    def assemblerSelect(self):
        while True:
            if len(self._assemblers) == 0:
                return
            menuOptions = self.assemblerNames + ("Return to menu",)
            choice = UserInterface.menu(menuOptions)
            if choice == len(menuOptions):
                return
            elif choice > len(menuOptions) or choice < 1:
                UserInterface.output("/!\ UNKNOWN MENU ERROR")
            else:
                returnDepth = self.assemblerMenu(choice)
                if returnDepth:
                    return

    def mainMenu(self):
        UserInterface.output("===== Computer System Simulator =====")
        while True:
            menuOptions = ["Step",
                           "Run steps",
                           "Components",
                           "Assembler",
                           "Console",
                           "End"]
            if len(self._components) == 0:
                menuOptions.remove("Components")
            if len(self._assemblers) == 0:
                menuOptions.remove("Assembler")
            choice = menuOptions[UserInterface.menu(menuOptions) - 1]
            if choice == "Step":
                self.step()
            elif choice == "Run steps":
                self.runSteps()
            elif choice == "Components":
                self.componentsSelect()
            elif choice == "Assembler":
                self.assemblerSelect()
            elif choice == "Console":
                UserInterface.console(simulator = self)
            elif choice == "End":
                return
            else:
                UserInterface.output("/!\ UNKNOWN MENU ERROR")
