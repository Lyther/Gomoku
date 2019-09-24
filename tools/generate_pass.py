# -*- coding: gbk -*-
import gobang
import numpy as np
import os

def main(my_color):
	f = open('C:/Users/Enderaoe/Downloads/chess_log.txt', 'r')
	board = np.zeros((15, 15), dtype=np.int)
	steps = 0
	global next
	string = ''
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
	string = '{' + string[0:-2] + '},\n'
	print('New state machine construction successful, calling rewrite...')
	insert_gobang(string)
	f.close()
	print('Program success return, deleting log file...')
	os.remove('C:/Users/Enderaoe/Downloads/chess_log.txt')
	print('Deletion successful, goodbye!')

def insert_gobang(string):
	buffer = ''
	f = open('../gobang.py', 'r', encoding='utf-8')
	content = f.readlines()
	for i in content:
		buffer = buffer + i.replace('TABLE = [', 'TABLE = [' + string)
	f.close()
	f = open('../gobang.py', 'w', encoding='utf-8')
	print('Ready to rewrite state machine.')
	f.write(buffer)


# -1表示自己是黑棋，1表示自己是白棋
if __name__ == '__main__':
	f = open('C:/Users/Enderaoe/Downloads/chess_log.txt', 'r')
	print('File open success, judging self color...')
	content = f.readlines()
	f.close()
	if content[-1][-2:] == '-1':
		print('[-1] self color is black, calling state modification function...')
		main(-1)
	else:
		print('[1] self color is white, calling state modification function...')
		main(1)
