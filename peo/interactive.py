import subprocess as sp

from peo.util import format_message
from peo.checksec import checksec
from peo.fhdr import fhdr
from peo.disasm.comment import Comment
from peo.disasm.arrow import flow_arrow
from peo.disasm.setcolor import setcolor, arrow_clr
from peo.disasm.indent import organize, indent, combine

class Shell:
    def __init__(self, filepath):
        self.filepath = filepath
        proc = sp.run(
            ["objdump", "-d", "-M", "intel", filepath],
            encoding="utf-8",
            stdout=sp.PIPE,
            stderr=sp.PIPE
        )

        if proc.returncode != 0:
            print(proc.stderr)
            sys.exit(1)

        msgs = format_message(proc.stdout)
        self.msgs = Comment(filepath, msgs).add()

    def headers(self):
        fhdr(self.filepath)

    def checksec(self):
        checksec(self.filepath)

    def __print_msgs(self, msgs):
        msgs = organize(msgs)
        arrows, arrowcolors = flow_arrow(msgs)
        indent(arrows, msgs)
        clr_arrows = arrow_clr(arrows, arrowcolors)
        msgs = setcolor(msgs)
        perf_msgs = combine(clr_arrows, msgs)

        for i in range(len(perf_msgs)):
            print("   ".join(msgs[i]))
            if len(msgs[i]) != 1 and i+1 != len(msgs):
                if len(msgs[i+1]) == 1:
                    print()

    def print_msgs(self):
        self.__print_msgs(self.msgs.copy())

    def print_func(self, fcn):
        tmp = []
        fcn_flag = False
        for msg in self.msgs:
            if len(msg) == 1:
                fcn_flag = (f'<{fcn}>' in msg[0])
            if fcn_flag:
                tmp.append(msg)
        if len(tmp) == 0:
            print('no such function')
            return
        self.__print_msgs(tmp)

    def print_help(self):
        print('disasm: print all asm code')
        print('disasm [FUNCION]: print asm code of function')
        print('help: print help')
        print('exit: exit shell')


def interactive(filepath):
    shell = Shell(filepath)
    while True:
        space = []
        try: command = input('> ')
        except EOFError:
            print('exit')
            break
        command, *args = command.strip().split()

        if command == 'disasm':
            if len(args) == 0:
                shell.print_msgs()
            elif len(args) == 1:
                shell.print_func(args[0])
            else:
                print('disasm takes at most one argument (' + str(len(args)) + 'given)')
                continue
        elif command == 'headers':
            shell.headers()
        elif command == 'checksec':
            shell.checksec()
        elif command == 'help':
            shell.print_help()
        elif command == 'exit':
            break
        else:
            print('no such command, try "help"')
