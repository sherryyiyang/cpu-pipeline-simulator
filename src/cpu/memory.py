class Memory:
    def __init__(self, size=1024):
        """Initialize memory with given size (in words)."""
        self.size = size
        self.mem = [0] * size

    def load(self, address):
        """Simulate a LOAD instruction from memory."""
        if address < 0 or address >= self.size:
            raise ValueError(f"Memory load error: address {address} out of bounds.")
        return self.mem[address]

    def store(self, address, value):
        """Simulate a STORE instruction to memory."""
        if address < 0 or address >= self.size:
            raise ValueError(f"Memory store error: address {address} out of bounds.")
        self.mem[address] = value

    def dump(self, start=0, end=10):
        """Utility function to print memory contents for debugging."""
        for i in range(start, min(end, self.size)):
            print(f"[{i}] = {self.mem[i]}")
