from simulator import Simulator
from processor import Processor
from memory import ReadOnlyMemory as ROM, RandomAccessMemory as RAM
from additional_hardware import PowerSupply, Button, Clock, QuadNANDGate as NAND, Resistor
from assembler import Assembler
from instruction_set import InstructionSet
from instruction_set_65C02.instructions import instructions

instructionSet = InstructionSet(instructions)

powerSupply = PowerSupply()

processor = Processor(
    instructionSet,
    connections = (
        (
            powerSupply, (
                ("VDD", "Power"),
                ("VSS", "Ground")
            )
        ),
    )
)

rom = ROM(
    connections = (
        (
            powerSupply, (
                ("VCC", "Power"),
                ("GND", "Ground"),
                ("WEB", "Power"),
                ("OEB", "Ground")
            )
        ),
        (
            processor, (
                ("I/O0", "D0"),
                ("I/O1", "D1"),
                ("I/O2", "D2"),
                ("I/O3", "D3"),
                ("I/O4", "D4"),
                ("I/O5", "D5"),
                ("I/O6", "D6"),
                ("I/O7", "D7"),
                ("A0", "A0"),
                ("A1", "A1"),
                ("A2", "A2"),
                ("A3", "A3"),
                ("A4", "A4"),
                ("A5", "A5"),
                ("A6", "A6"),
                ("A7", "A7"),
                ("A8", "A8"),
                ("A9", "A9"),
                ("A10", "A10"),
                ("A11", "A11"),
                ("A12", "A12"),
                ("A13", "A13"),
                ("A14", "A14")
            )
        )
    )
)

ram = RAM(
    connections = (
        (
            powerSupply, (
                ("Vcc", "Power"),
                ("Vss", "Ground")
            )
        ),
        (
            processor, (
                ("I/O0", "D0"),
                ("I/O1", "D1"),
                ("I/O2", "D2"),
                ("I/O3", "D3"),
                ("I/O4", "D4"),
                ("I/O5", "D5"),
                ("I/O6", "D6"),
                ("I/O7", "D7"),
                ("A0", "A0"),
                ("A1", "A1"),
                ("A2", "A2"),
                ("A3", "A3"),
                ("A4", "A4"),
                ("A5", "A5"),
                ("A6", "A6"),
                ("A7", "A7"),
                ("A8", "A8"),
                ("A9", "A9"),
                ("A10", "A10"),
                ("A11", "A11"),
                ("A12", "A12"),
                ("A13", "A13"),
                ("A14", "A14"),
                ("WEB", "RWB"),
                ("OEB", "A14")
            )
        )
    )
)

clock = Clock(
    connections = (
        (
            powerSupply, (
                ("VCC", "Power"),
                ("GND", "Ground")
            )
        ),
        (processor, (("Output", "PHI2"),))
    )
)

nand = NAND(
    connections = (
        (
            powerSupply, (
                ("VCC", "Power"),
                ("GND", "Ground"),
                ("A1", "Power"),
                ("B1", "Power"),
                ("B3", "Power"),
                ("B3", "Power")
            )
        ),
        (
            processor, (
                ("A4", "A15"),
                ("B4", "A15")
            )
        ),
        (rom, (("Y4", "CEB"),)),
        (ram, (("Y2", "CSB"),)),
        (clock, (("A2", "Output"),))
    )
)
nand.connectPin("Y4", nand, "B2")

reset = Button(
    connections = (
        (powerSupply, ((3, "Ground"),)),
        (processor, ((1, "RESB"),))
    )
)

r1 = Resistor(
    connections = (
        (powerSupply, ((1, "Power"),)),
        (reset, ((2, 1),))
    )
)

r2 = Resistor(
    connections = (
        (powerSupply, ((1, "Power"),)),
        (processor, ((2, "RDY"),))
    )
)

def step(components):
    components["System clock"].step()
    for component in ("Resistor R1",
                      "Resistor R2",
                      "RESET button",
                      "System clock",
                      "65C02 microprocessor",
                      "NAND gates",
                      "AT28C256 ROM",
                      "HM62256B RAM"):
        components["Power supply"].response()
        components[component].respond()

presetSimulator = Simulator(
    components = {
        "65C02 microprocessor": processor,
        "AT28C256 ROM": rom,
        "HM62256B RAM": ram,
        "NAND gates": nand,
        "System clock": clock,
        "Power supply": powerSupply,
        "RESET button": reset,
        "Resistor R1": r1,
        "Resistor R2": r2
    },
    step = step,
    assemblers = {"65C02": Assembler(instructionSet)}
)

if __name__ == "__main__":
    presetSimulator.mainMenu()
