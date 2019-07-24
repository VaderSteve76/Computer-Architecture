"""CPU functionality."""

import sys

# op codes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

# reserved reg.
IM = 5
IS = 6
SP = 7

# flags
FL_LT = 0b100
FL_GT = 0b010
FL_EQ = 0b001
FL_TIMER = 0b00000001
FL_KEYBOARD = 0b00000010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = 0xf4
        self.processCounter = 0
        self.flags = 0
        self.isPaused = False
        self.instruction_sets_processCounter = False
        # self.interrupts = 1
        # self.last_timer_int = None

        self.branchTree = {
            HLT: self.op_HLT,
            LDI: self.op_LDI,
            PRN: self.op_PRN,
            MUL: self.op_MUL,
            PUSH: self.op_PUSH,
            POP: self.op_POP
        }

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    def stack_push(self, val):
        self.reg[SP] -= 1
        self.ram_write(self.reg[SP], val)

    def stack_pop(self):
        val = self.ram_read(self.reg[SP])
        self.reg[SP] += 1
        return val

    def load(self):
        """Load a program into memory."""
        address = 0

        fp = open(filename, "r")
        for line in fp:
            # split by comment and strip empty spaces
            instruction = line.split("#")[0].strip()
            if instruction == "":
                continue
            value = int(instruction, 2)
            self.ram[address] = value
            address += 1

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            curr_reg = self.ram[self.pc]
            opt_a = self.ram[self.pc + 1]
            opt_b = self.ram[self.pc + 2]
            if curr_reg == 0b00000001:
                running = False
                self.pc += 1

            elif curr_reg == 0b10000010:
                self.reg[opt_a] = opt_b
                self.pc += 3

            elif curr_reg == 0b01000111:
                print(self.reg[opt_a])
                self.pc += 2
            else:
                print(f'Unknown command {curr_reg}')
                sys.exit(1)
