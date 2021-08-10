import sys
import subprocess as sp

def rm_comment(msg):
    try:
        msg = msg[0:msg.index("#")]
    except:
        pass
    return msg

def rm_consecutive_spaces(msg):
    return msg.strip().replace("  ", " ")

class Color:
    colors = {
        "normal"         : "\033[0m",
        "black"          : "\033[30m",
        "red"            : "\033[31m",
        "green"          : "\033[32m",
        "yellow"         : "\033[33m",
        "blue"           : "\033[34m",
        "purple"         : "\033[35m",
        "cyan"           : "\033[36m",
        "white"          : "\033[37m",
        "bold"           : "\033[1m",
        "highlight"      : "\033[3m",
        "highlight_off"  : "\033[23m",
        "underline"      : "\033[4m",
        "underline_off"  : "\033[24m",
        "blink"          : "\033[5m",
        "blink_off"      : "\033[25m",
    }

    @staticmethod
    def blackify(msg):     return Color.colorify(msg, "black")
    @staticmethod
    def redify(msg):       return Color.colorify(msg, "red")
    @staticmethod
    def greenify(msg):     return Color.colorify(msg, "green")
    @staticmethod
    def yellowify(msg):    return Color.colorify(msg, "yellow")
    @staticmethod
    def blueify(msg):      return Color.colorify(msg, "blue")
    @staticmethod
    def grayify(msg):      return Color.colorify(msg, "gray")
    @staticmethod
    def light_grayify(msg):return Color.colorify(msg, "light_gray")
    @staticmethod
    def purplify(msg):     return Color.colorify(msg, "purple")
    @staticmethod
    def cyanify(msg):      return Color.colorify(msg, "cyan")
    @staticmethod
    def boldify(msg):      return Color.colorify(msg, "bold")
    @staticmethod
    def highlightify(msg): return Color.colorify(msg, "highlight")
    @staticmethod
    def underlinify(msg):  return Color.colorify(msg, "underline")
    @staticmethod
    def blinkify(msg):     return Color.colorify(msg, "blink")

    @staticmethod
    def colorify(text, attrs):
        colors = Color.colors
        msg = [colors[attr] for attr in attrs.split() if attr in colors]
        msg.append(str(text))
        if colors["highlight"] in msg:   msg.append(colors["highlight_off"])
        if colors["underline"] in msg:   msg.append(colors["underline_off"])
        if colors["blink"] in msg:       msg.append(colors["blink_off"])
        msg.append(colors["normal"])
        return "".join(msg)



if __name__ == "__main__":
    filename = "a.out"
    p = sp.run(["objdump", "-d", "-M", "intel", filename], encoding="utf-8", stdout=sp.PIPE, stderr=sp.PIPE)
    if p.returncode != 0:
        print(p.stderr)
        sys.exit(1)

    lines = p.stdout.split("\n")
    for line in lines:
        items = line.split("\t")
        if len(items) == 3:
            items[2] = rm_comment(items[2])
        msg = []
        for item in items:
            msg.append(rm_consecutive_spaces(item))
        print(msg)