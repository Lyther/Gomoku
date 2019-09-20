"""
用来生成获胜下法的程式
"""

import gobang
import numpy as np

def main(my_color):
	f = open('chess_log.txt', 'r')
	board = np.zeros((15, 15), dtype=np.int)
	steps = 0
	global recent
	global next
	while True:
		step = f.readline()
		steps += 1
		if step == '':
			break
		pos = step.split(',')
		color = my_color * int(pos[2])
		board[int(pos[0]), int(pos[1])] = color
		if my_color == 1:
			if steps & 1:
				recent = board
			else:
				next = (int(pos[0]), int(pos[1]))
				string = gobang.hash(board)
				print("'", string, "':", next, ',', sep='')
		else:
			if not steps & 1:
				recent = board
			else:
				next = (int(pos[0]), int(pos[1]))
				string = gobang.hash(board)
				print("'", string, "':", next, ',', sep='')


if __name__ == '__main__':
	main(1)
