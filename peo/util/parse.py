import re


# 両端の空白を削除、文中の連続した空白を半角空白1個に置き換え
def rm_consecutive_spaces(msg):
    return re.sub(r"\s+", " ", msg).strip()

# objdump -d -M intel ./a.out の出力結果はこれを元に付け加える
def format_message(lines):
    lines = lines.split("\n")  # 出力を行で分ける

    msgs = []  # linesを整理したものが入る
    for line in lines:
        if line == "":  # 何もない行はいらない
            continue
        items = re.split("[#\t]", line)  # 行を分ける 基本(アドレス、命令、読みやすい命令(、コメント))に分かれる

        msg = []  # items(line)を整理したものが入る
        for item in items:
            msg.append(rm_consecutive_spaces(item))
        msgs.append(msg)
    return msgs