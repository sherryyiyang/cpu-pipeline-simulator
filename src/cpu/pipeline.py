from cpu.instruction import Instruction
from cpu.register_file import RegisterFile
from cpu.memory import Memory
from cpu.alu import ALU

class PipelineStage:
    def __init__(self, name):
        self.name = name
        self.instruction = None

    def __repr__(self):
        return f"{self.name}: {self.instruction}"

class Pipeline:
    def __init__(self, instruction_memory):
        self.IF = PipelineStage("Fetch")
        self.ID = PipelineStage("Decode")
        self.EX = PipelineStage("Execute")
        self.MEM = PipelineStage("Memory")
        self.WB = PipelineStage("Writeback")

        self.pc = 0
        self.clock = 0
        self.instructions = instruction_memory
        self.registers = RegisterFile()
        self.memory = Memory()
        self.alu = ALU()
        self.finished = False

    def step(self):
        self.clock += 1
        print(f"\n[Cycle {self.clock}]")

        # Writeback
        if self.WB.instruction:
            inst = self.WB.instruction
            if inst.dest is not None and inst.write_back:
                self.registers.write(inst.dest, inst.result)

        # Memory
        if self.MEM.instruction:
            inst = self.MEM.instruction
            if inst.op == "LOAD":
                inst.result = self.memory.load(inst.address)
            elif inst.op == "STORE":
                self.memory.store(inst.address, inst.src2_val)
            self.WB.instruction = inst
        else:
            self.WB.instruction = None

        # Execute
        if self.EX.instruction:
            inst = self.EX.instruction
            inst.result = self.alu.execute(inst.op, inst.src1_val, inst.src2_val)
            if inst.op in {"LOAD", "STORE"}:
                inst.address = inst.result
            self.MEM.instruction = inst
        else:
            self.MEM.instruction = None

        # Decode
        if self.ID.instruction:
            inst = self.ID.instruction
            inst.src1_val = self.registers.read(inst.src1)
            inst.src2_val = self.registers.read(inst.src2)
            self.EX.instruction = inst
        else:
            self.EX.instruction = None

        # Fetch
        if self.pc < len(self.instructions):
            inst = self.instructions[self.pc]
            self.ID.instruction = inst
            self.pc += 1
        else:
            self.ID.instruction = None

        if all(stage.instruction is None for stage in [self.IF, self.ID, self.EX, self.MEM, self.WB]):
            self.finished = True

        self.print_pipeline_state()

    def print_pipeline_state(self):
        print(self.IF)
        print(self.ID)
        print(self.EX)
        print(self.MEM)
        print(self.WB)
