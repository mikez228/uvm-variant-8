class Memory:
    def __init__(self, mem_size=1024, reg_count=64):
        # объединённая память команд и данных
        self.memory = [0] * mem_size
        # регистры
        self.registers = [0] * reg_count
