import sys
import argparse

from peo.disasm import disasm

def main():
    parser = argparse.ArgumentParser(description="Python Extensions for objdump")
    parser.add_argument("file")  # 必須の引数
    parser.add_argument("-d", "--disassemble", action="store_true", help="Display assembler contents of executable sections")  # オプション(フラグ)

    args = parser.parse_args()

    filepath = args.file  # ファイルのパス

    if args.disassemble:
        disasm(filepath)

if __name__ == "__main__":
    main()