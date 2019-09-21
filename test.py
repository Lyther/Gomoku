'''
单元测试，根据main函数的参数测试不同的单元
'''
import imp
import gobang
import numpy as np

def test(unit):
	if unit == 0:   # 测试评估函数
		board = np.zeros((15,15), dtype=np.int)
		board[7, 6] = 1
		board[7, 8] = 1
		board[6, 7] = 1
		board[8, 7] = 1
		print(gobang.earn(board, -1, 7, 7, 15, 0))
	if unit == 1:
		board = np.zeros((15, 15), dtype=np.int)
		board[2, 2:4] = 1
		board[4, 1:3] = 1
		board[1, 10:12] = -1
		board[2, 10] = -1
		board[4, 12] = -1
		print(gobang.earn(board, -1, 4, 10, 15, 0))
		print(gobang.earn(board, -1, 1, 9, 15, 0))
	if unit == 2:
		board = np.zeros((15, 15), dtype=np.int)
		board[7,7] = board[7,9] = board[7,10] = board[10,9] = board[9,9] = board[9,10] = -1
		board[7,8] = board[8,7] = board[10,10] = board[11,11] = board[12,12] = board[14,14] = 1
		print(gobang.earn(board, -1, 9, 7, 15, 0))
		print(gobang.earn(board, -1, 13, 13, 15, 0))
	if unit == 3:
		board = np.zeros((15, 15), dtype=np.int)
		board[7, 7] = -1
		board[8, 7] = 1
		agent = imp.load_source('AI', "gobang.py").AI(15, 1, 5)
		agent.go(np.zeros((15, 15), dtype=np.int))
		print(agent.candidate_list[-1])
		agent.go(np.copy(board))
		print(agent.candidate_list[-1])
	if unit == 4:
		board = np.zeros((15, 15), dtype=np.int)
		board[8, 7] = board[7, 8] = board[8, 6] = board[6, 7] = board[10, 7] = board[7, 3] = board[5, 2] = board[9, 5] = \
		board[5, 5] = board[6, 2] = board[5, 4] = board[4, 2] = board[7, 2] = board[8, 3] = board[10, 4] = board[11, 2] = 1
		board[7, 7] = board[7, 6] = board[9, 6] = board[8, 5] = board[7, 4] = board[7, 5] = board[6, 3] = board[6, 5] = \
		board[4, 5] = board[6, 4] = board[8, 4] = board[5, 3] = board[3, 2] = board[8, 2] = board[9, 4] = board[10, 3] = -1
		print(gobang.earn(board, -1, 11, 3, 15, 0))
		print(gobang.earn(board, -1, 8, 9, 15, 0))
	if unit == 5:
		board = np.zeros((15, 15), dtype=np.int)
		agent = imp.load_source('AI', "gobang.py").AI(15, -1, 5)
		board[7, 7] = -1
		board[8, 8] = 1
		agent.go(np.copy(board))
		print(agent.candidate_list[-1])

if __name__ == '__main__':
	test(5)