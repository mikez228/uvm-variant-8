import struct
import sys
from instructions import OPCODES


def assemble_line(parts):
    cmd = parts[0].upper()

    # LOAD B C
    if cmd == "LOAD":
        _, B, C = parts
        A = OPCODES[cmd]
        value = (
            (A & 0xF) |
            (int(B) << 4) |
            (int(C) << 25)
        )
        return struct.pack("<I", value)

    # READ B C D
    if cmd == "READ":
        _, B, C, D = parts
        A = OPCODES[cmd]
        value = (
            (A & 0xF) |
            (int(B) << 4) |
            (int(C) << 13) |
            (int(D) << 19)
        )
        return struct.pack("<I", value)

    # WRITE B C D
    if cmd == "WRITE":
        _, B, C, D = parts
        A = OPCODES[cmd]
        value = (
            (A & 0xF) |
            (int(B) << 4) |
            (int(C) << 13) |
            (int(D) << 19)
        )
        return struct.pack("<I", value)

    # NOT B C D (6 байт)
    if cmd == "NOT":
        _, B, C, D = parts
        A = OPCODES[cmd]
        value = (
            (A & 0xF) |
            (int(B) << 4) |
            (int(C) << 10) |
            (int(D) << 36)
        )
        return struct.pack("<Q", value)[:6]

    raise ValueError(f"Неизвестная команда: {cmd}")


def assemble(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as src, \
         open(output_file, "wb") as dst:

        for line in src:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            dst.write(assemble_line(parts))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python assembler.py input.asm output.bin")
        sys.exit(1)

    assemble(sys.argv[1], sys.argv[2])
    print("Ассемблирование завершено")
