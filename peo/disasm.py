import sys
import subprocess as sp
from pprint import pprint

from peo.util import *

def disasm(filepath):
    proc = sp.run(["objdump", "-d", "-M", "intel", filepath], encoding="utf-8", stdout=sp.PIPE, stderr=sp.PIPE)

    # objdumpがエラーを出したらやめるっピ
    if proc.returncode != 0:
        print(proc.stderr)
        sys.exit(1)

    msgs = format_message(proc.stdout)
    pprint(msgs)