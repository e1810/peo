import re

class DepthManager:
	depths = []
	def __init__(self, n: int):
		self.depths = [0] * n
	def max(self, s: int, e: int) -> int:
		ret = 0
		for i in range(s, e+1):
			ret = max(ret, self.depths[i])
		return ret

	def update(self, s: int, e: int, x: int) -> int:
		for i in range(s, e+1):
			self.depths[i] = x



def add_flow_arrow(msgs: str) -> str:
	ret = []
	insts = []
	for i in range(3, len(msgs)):
		if re.match("[0-9a-f]+:", msgs[i][0]):
			insts.append(msgs[i])
		else:
			if insts:
				ret += __arrowing_in_func(insts)
				insts = []
			ret.append(msgs[i])
	if insts:
		ret += __arrowing_in_func(insts)

	return ret


def __arrowing_in_func(insts: str) -> list:
	# 基本的に逆から見ていく  矢印終点に辿り着いたら始点まで戻る形で矢を張る
	# 終点が同じ2つの矢があると上のやつしかできない 要修正

	arrows = [[' '] for i in range(len(insts))]
	depthM = DepthManager(len(insts))
	e2b = dict()
	for i in range(len(insts)-1, -1, -1):
		addr = insts[i][0][:-1]
		if addr in e2b:
			st = e2b[addr]
			depth = depthM.max(i, st)
			arrows[i] = list('>' + '\u2500' * depth + '\u250c') + arrows[st][2+depth:]
			for j in range(i+1, st):
				while len(arrows[j]) <= depth + 1:
					arrows[j].append(' ')
				arrows[j][depth+1] = '\u2502'
			arrows[st] = list('<' + '\u2500' * depth + '\u2514') + arrows[i][2+depth:]
			depthM.update(i, st, depth+2)

		if len(insts[i]) < 3 or len(insts[i][2].split()) == 1: continue
		opc, opr, *_ = insts[i][2].split()
		if opc[0] != 'j': continue
		if re.match('^[0-9a-f]*$', opr) is None: continue
		if int(opr, 16) > int(addr, 16): continue
		e2b[opr] = i

	e2b = dict()
	for i in range(len(insts)):
		addr = insts[i][0][:-1]
		if addr in e2b:
			st = e2b[addr]
			depth = depthM.max(st, i)
			arrows[st] = list('<' + '\u2500' * depth + '\u250c') + arrows[st][2+depth:]
			for j in range(st+1, i):
				while len(arrows[j]) <= depth + 1:
					arrows[j].append(' ')
				arrows[j][depth+1] = '\u2502'
			arrows[i] = list('>'+ '\u2500' * depth + '\u2514') + arrows[i][2+depth:]
			depthM.update(st, i, depth+2)

		if len(insts[i]) < 3 or len(insts[i][2].split()) == 1: continue
		opc, opr, *_ = insts[i][2].split()
		if opc[0] != 'j': continue
		if re.match('^[0-9a-f]*$', opr) is None: continue
		if int(opr, 16) < int(addr, 16): continue
		e2b[opr] = i

	depth = depthM.max(0, len(insts)-1)
	for i in range(len(insts)):
		arrows[i] += [' '] * (depth - len(arrows[i]))
		arrows[i].reverse()
		insts[i] = [''.join(arrows[i])] + insts[i]
	return insts