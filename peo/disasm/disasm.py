import sys
import subprocess as sp

from peo.util import format_message
from peo.disasm.comment import Comment
from peo.disasm.arrow import flow_arrow
from peo.disasm.setcolor import setcolor
from peo.disasm.indent import organize, indent


def disasm(filepath):
    proc = sp.run(["objdump", "-d", "-M", "intel", filepath], encoding="utf-8", stdout=sp.PIPE, stderr=sp.PIPE)

    # objdumpがエラーを出したらやめるっピ
    if proc.returncode != 0:
        print(proc.stderr)
        sys.exit(1)

    msgs = format_message(proc.stdout)
    msgs = Comment(filepath, msgs).add()
    msgs = organize(msgs)

    arrows = flow_arrow(msgs)
    msgs = setcolor(msgs)
    msgs = indent(arrows, msgs)

    # TODO: 出力を揃える
    for i in range(len(msgs)):
        print("   ".join(msgs[i]))
        if len(msgs[i]) != 1 and i+1 != len(msgs):
            if len(msgs[i+1]) == 1:
                print()
