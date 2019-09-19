'''
单元测试，根据main函数的参数测试不同的单元
'''
import main
import numpy as np

def test(unit):
	if unit == 0:   # 测试评估函数
		board = np.zeros((15,15), dtype=np.int)
		board[7, 6] = 1
		board[7, 8] = 1
		board[6, 7] = 1
		board[8, 7] = 1
		print(main.earn(board, -1, 7, 7, 15, 0))
	if unit == 1:
		board = np.zeros((15, 15), dtype=np.int)
		board[2, 2:4] = 1
		board[4, 1:3] = 1
		board[1, 10:12] = -1
		board[2, 10] = -1
		board[4, 12] = -1
		print(main.earn(board, -1, 4, 10, 15, 0))
		print(main.earn(board, -1, 1, 9, 15, 0))
	if unit == 2:
		board = np.zeros((15, 15), dtype=np.int)
		board[7,7] = board[7,9] = board[7,10] = board[10,9] = board[9,9] = board[9,10] = -1
		board[7,8] = board[8,7] = board[10,10] = board[11,11] = board[12,12] = board[14,14] = 1
		print(main.earn(board, -1, 9, 7, 15, 0))
		print(main.earn(board, -1, 13, 13, 15, 0))


if __name__ == '__main__':
	test(2)