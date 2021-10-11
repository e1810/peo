import sys
import subprocess as sp
from pprint import pprint

from peo.util import *
from peo.disasm.arrow import *
from peo.disasm.setcolor import *


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
                msgs[i][3] = f"{hex(addr)}; {get_section_as_str(filepath, '.rodata', addr)}"
        except IndexError:
            pass

    #msgs = split(msgs)
    arrows = flow_arrow(msgs)
    for i in range(len(msgs)):
        msgs[i] = [arrows[i]] + msgs[i]
    
    msgs = setcolor(msgs)

    # TODO: 出力を揃える
    for msg in msgs:
        print("  ".join(msg))
