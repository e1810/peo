import sys
import argparse

from peo.disasm import disasm
from peo.fhdr import fhdr

def main():
    parser = argparse.ArgumentParser(description="Python Extensions for objdump")
    parser.add_argument("file")  # 必須の引数
    parser.add_argument("-d", "--disassemble", action="store_true", help="Display assembler contents of executable sections")  # オプション(フラグ)
    parser.add_argument("-f", "--file-headers", action="store_true", help="Display the contents of the overall file header")

    args = parser.parse_args()

    filepath = args.file  # ファイルのパス

    if args.disassemble:
        disasm(filepath)
    elif args.file_headers:
        fhdr(filepath)

if __name__ == "__main__":
    main()