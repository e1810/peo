from peo.util import *

#命令系統で配列持ってみた
jumper = ["jmp", "ja", "jae", "jb", "jbe", "jc", "jcxz", "je", "jg", "jge", "jl", "jle", "jna", "jnae", "jnb", "jnbe", "jnc", "jne", "jng", "jnge", "jnl", "jnle", "jno", "jnp", "jns", "jnz", "jo", "jp", "jpe", "jpo", "js", "jz"]

caller = ["call"]

stacker = ["push", "pop"]

math = ["add", "sub", "and", "or", "xor"]

#配色辞書
clr_func = {"jumper":Color.yellowify, "caller":Color.bg_redify, "stacker":Color.purplify, "math":Color.blueify, "other":Color.blackify}

#必要なアセンブラ部と命令部の取り出し
def split(msgs):
    for i in range(len(msgs)):
        if len(msgs[i]) >= 3:
            msg = msgs[i][2].split(' ')
            msgs[i][2] = setcolor(msgs[i][2], msg)
    return msgs

#配色と適応
def setcolor(msgs, msg):
    if msg[0] in jumper:
        msgs = clr_func["jumper"](msgs)
        return msgs
    
    elif msg[0] in caller:
        msgs = clr_func["caller"](msgs)
        return msgs
    
    elif msg[0] in stacker:
        msg[0] = clr_func["stacker"](msg[0])
        msgs = ' '.join(msg)
        return msgs
    
    elif msg[0] in math:
        msg[0] = clr_func["math"](msg[0])
        msgs = ' '.join(msg)
        return msgs
    
    else:
        msg[0] = clr_func["other"](msg[0])
        msgs = ' '.join(msg)
        return msgs
