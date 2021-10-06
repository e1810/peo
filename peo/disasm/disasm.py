import sys
import subprocess as sp
from pprint import pprint

from peo.util import *
from peo.disasm.arrow import *


def disasm(filepath):
    proc = sp.run(["objdump", "-d", "-M", "intel", filepath], encoding="utf-8", stdout=sp.PIPE, stderr=sp.PIPE)

    # objdumpがエラーを出したらやめるっピ
    if proc.returncode != 0:
        print(proc.stderr)
        sys.exit(1)

    msgs = format_message(proc.stdout)

    for i, msg in enumerate(msgs):
        try:
            if "lea" in msg[2]:
                addr = int(msg[3].split(" ")[0], 16)
                msgs[i][3] = Color.greenify(f"{hex(addr)}; {get_section_as_str(filepath, '.rodata', addr)}")
        except IndexError:
            pass

    msgs = add_flow_arrow(msgs)

    # TODO: 出力を揃える
    for msg in msgs:
        print("  ".join(msg))
