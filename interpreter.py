import struct
import sys
import json
from memory import Memory


def run(binary_file, dump_file, start, end):
    mem = Memory()

    with open(binary_file, "rb") as f:
        data = f.read()

    pc = 0
    while pc < len(data):
        opcode = data[pc] & 0xF

        # LOAD
        if opcode == 10:
            val = struct.unpack_from("<I", data, pc)[0]
            B = (val >> 4) & ((1 << 21) - 1)
            C = (val >> 25) & 0x3F
            mem.registers[C] = B
            pc += 4

        # READ
        elif opcode == 8:
            val = struct.unpack_from("<I", data, pc)[0]
            B = (val >> 4) & 0x1FF
            C = (val >> 13) & 0x3F
            D = (val >> 19) & 0x3F
            addr = mem.registers[C] + B
            mem.registers[D] = mem.memory[addr]
            pc += 4

        # WRITE
        elif opcode == 7:
            val = struct.unpack_from("<I", data, pc)[0]
            B = (val >> 4) & 0x1FF
            C = (val >> 13) & 0x3F
            D = (val >> 19) & 0x3F
            addr = mem.registers[D] + B
            mem.memory[addr] = mem.registers[C]
            pc += 4

        # NOT
        elif opcode == 4:
            raw = data[pc:pc+6] + b"\x00\x00"
            val = struct.unpack("<Q", raw)[0]
            B = (val >> 4) & 0x3F
            C = (val >> 10) & ((1 << 26) - 1)
            D = (val >> 36) & 0x1FF
            addr = mem.registers[B] + D
            mem.memory[addr] = ~mem.memory[C]
            pc += 6

        else:
            raise RuntimeError(f"Неизвестный opcode {opcode}")

    with open(dump_file, "w", encoding="utf-8") as f:
        json.dump(mem.memory[start:end], f, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Использование: python interpreter.py program.bin dump.json start end")
        sys.exit(1)

    run(
        sys.argv[1],
        sys.argv[2],
        int(sys.argv[3]),
        int(sys.argv[4])
    )
    print("Выполнение завершено")
