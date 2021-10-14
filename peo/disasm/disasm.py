import sys
import subprocess as sp
from pprint import pprint

from peo.util import format_message
from peo.disasm.comment import Comment
from peo.disasm.arrow import flow_arrow
from peo.disasm.setcolor import setcolor


def disasm(filepath):
    proc = sp.run(["objdump", "-d", "-M", "intel", filepath], encoding="utf-8", stdout=sp.PIPE, stderr=sp.PIPE)

    # objdumpがエラーを出したらやめるっピ
    if proc.returncode != 0:
        print(proc.stderr)
        sys.exit(1)

    msgs = format_message(proc.stdout)

    msgs = Comment(filepath, msgs).add()

    arrows = flow_arrow(msgs)
    msgs = setcolor(msgs)
    
    for i in range(len(msgs)):
        msgs[i] = [arrows[i]] + msgs[i]

    # TODO: 出力を揃える
    for msg in msgs:
        print("  ".join(msg))
