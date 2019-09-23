"""
用来生成获胜下法的程式
"""

import gobang
import numpy as np

def main(my_color):
	f = open('chess_log.txt', 'r')
	board = np.zeros((15, 15), dtype=np.int)
	steps = 0
	global next
	string = ''
	print('{', end='')
	while True:
		step = f.readline()
		steps += 1
		if step == '':
			break
		pos = step.split(',')
		if my_color == 1:
			if not steps & 1:
				next = (int(pos[0]), int(pos[1]))
				string = string + "'" + gobang.hash_board(board) + "':" + str(next) + ',\n'
		else:
			if steps & 1:
				next = (int(pos[0]), int(pos[1]))
				string = string + "'" + gobang.hash_board(board) + "':" + str(next) + ',\n'
		board[int(pos[0]), int(pos[1])] = pos[2]
	string = string[0:-2]
	print(string, end='')
	print('},')


if __name__ == '__main__':
	main(1)
