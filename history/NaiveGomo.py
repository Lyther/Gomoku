import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
DEPTH = 4
PRIORITY = 1.2
INCREASE_I = 1.05
INCREASE_E = 0.95
DECREASE_I = 0.15
DECREASE_E = 0.02
BIAS = 1


class AI(object):


	# chessboard_size, color, time_out passed from agent
	def __init__(self, chessboard_size, color, time_out):

		self.chessboard_size = chessboard_size
		# You are white or black
		self.color = color
		# the max time you should use, your algorithm's run time must not exceed the timelimit.
		self.time_out = time_out
		# You need add your decision into your candidate_list.
		# System will get the end of your candidate_list as your decision.
		self.candidate_list = []

		self.iv = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.float)
		self.ev = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.float)

	# The input is current chessboard.
	def go(self, chessboard):
		print('Get chessboard: \n')
		print(chessboard)
		# Clear candidate_list
		self.candidate_list.clear()
		# ==================================================================
		# Write your algorithm here
		# Here is the simplest sample:Random decision
		idx = np.where(chessboard == COLOR_NONE)
		idx = list(zip(idx[0], idx[1]))
		print('Get empty spaces: \n')
		print(idx)

		for i, j in idx:
			self.evaluate_e(i, j, chessboard)
			self.evaluate_i(i, j, chessboard)
		new_pos = self.choose(idx, chessboard)
		print(new_pos)
		# ==============Find new pos========================================
		# Make sure that the position of your decision in chess board is empty.
		# If not, return error.
		assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
		# Add your decision into candidate_list, Records the chess board
		self.candidate_list.append(new_pos)

	def evaluate_i(self, x, y, chessboard):
		self.iv[x][y] = 0
		for i in range(1, DEPTH+1):
			if x - i < 0 or chessboard[x - i][y] == -self.color:
				break
			elif chessboard[x - i][y] == self.color:
				self.iv[x][y] += INCREASE_I
			elif self.iv[x][y]:
				self.iv[x][y] -= DECREASE_I
		for i in range(1, DEPTH+1):
			if x + i >= self.chessboard_size or chessboard[x + i][y] == -self.color:
				break
			elif chessboard[x + i][y] == self.color:
				self.iv[x][y] += INCREASE_I
			elif self.iv[x][y]:
				self.iv[x][y] -= DECREASE_I
		for i in range(1, DEPTH+1):
			if y - i < 0 or chessboard[x][y - i] == -self.color:
				break
			elif chessboard[x][y - i] == self.color:
				self.iv[x][y] += INCREASE_I
			elif self.iv[x][y]:
				self.iv[x][y] -= DECREASE_I
		for i in range(1, DEPTH+1):
			if y + i >= self.chessboard_size or chessboard[x][y + i] == -self.color:
				break
			elif chessboard[x][y + i] == self.color:
				self.iv[x][y] += INCREASE_I
			elif self.iv[x][y]:
				self.iv[x][y] -= DECREASE_I
		for i in range(1, DEPTH+1):
			if x - i < 0 or y - i < 0 or chessboard[x - i][y - i] == -self.color:
				break
			elif chessboard[x - i][y - i] == self.color:
				self.iv[x][y] += INCREASE_I
			elif self.iv[x][y]:
				self.iv[x][y] -= DECREASE_I
		for i in range(1, DEPTH+1):
			if x - i < 0 or y + i >= self.chessboard_size or chessboard[x - i][y + i] == -self.color:
				break
			elif chessboard[x - i][y + i] == self.color:
				self.iv[x][y] += INCREASE_I
			elif self.iv[x][y]:
				self.iv[x][y] -= DECREASE_I
		for i in range(1, DEPTH+1):
			if x + i >= self.chessboard_size or y - i < 0 or chessboard[x + i][y - i] == -self.color:
				break
			elif chessboard[x + i][y - i] == self.color:
				self.iv[x][y] += INCREASE_I
			elif self.iv[x][y]:
				self.iv[x][y] -= DECREASE_I
		for i in range(1, DEPTH+1):
			if x + i >= self.chessboard_size or y + i >= self.chessboard_size or chessboard[x + i][y + i] == -self.color:
				break
			elif chessboard[x + i][y + i] == self.color:
				self.iv[x][y] += INCREASE_I
			elif self.iv[x][y]:
				self.iv[x][y] -= DECREASE_I

	def evaluate_e(self, x, y, chessboard):
		self.ev[x][y] = 0
		cache = 0
		for i in range(1, DEPTH+1):
			if x - i < 0 or chessboard[x - i][y] == self.color:
				break
			elif self.ev[x][y] == 0 and chessboard[x - i][y] == 0:
				break
			elif chessboard[x - i][y] == -self.color:
				self.ev[x][y] += INCREASE_E
				cache += INCREASE_E
			elif self.ev[x][y]:
				self.ev[x][y] -= DECREASE_E
		if cache >= 3 * INCREASE_E:
			self.ev[x][y] += INCREASE_E
		cache = 0
		for i in range(1, DEPTH+1):
			if x + i >= self.chessboard_size or chessboard[x + i][y] == self.color:
				break
			elif self.ev[x][y] == 0 and chessboard[x + i][y] == 0:
				break
			elif chessboard[x + i][y] == -self.color:
				self.ev[x][y] += INCREASE_E
				cache += INCREASE_E
			elif self.ev[x][y]:
				self.ev[x][y] -= DECREASE_E
		if cache >= 3 * INCREASE_E:
			self.ev[x][y] += INCREASE_E
		cache = 0
		for i in range(1, DEPTH+1):
			if y - i < 0 or chessboard[x][y - i] == self.color:
				break
			elif self.ev[x][y] == 0 and chessboard[x][y - i] == 0:
				break
			elif chessboard[x][y - i] == -self.color:
				self.ev[x][y] += INCREASE_E
				cache += INCREASE_E
			elif self.ev[x][y]:
				self.ev[x][y] -= DECREASE_E
		if cache >= 3 * INCREASE_E:
			self.ev[x][y] += INCREASE_E
		cache = 0
		for i in range(1, DEPTH+1):
			if y + i >= self.chessboard_size or chessboard[x][y + i] == self.color:
				break
			elif self.ev[x][y] == 0 and chessboard[x][y + i] == 0:
				break
			elif chessboard[x][y + i] == -self.color:
				self.ev[x][y] += INCREASE_E
				cache += INCREASE_E
			elif self.ev[x][y]:
				self.ev[x][y] -= DECREASE_E
		if cache >= 3 * INCREASE_E:
			self.ev[x][y] += INCREASE_E
		cache = 0
		for i in range(1, DEPTH+1):
			if x - i < 0 or y - i < 0 or chessboard[x - i][y - i] == self.color:
				break
			elif self.ev[x][y] == 0 and chessboard[x - i][y - i] == 0:
				break
			elif chessboard[x - i][y - i] == -self.color:
				self.ev[x][y] += INCREASE_E
				cache += INCREASE_E
			elif self.ev[x][y]:
				self.ev[x][y] -= DECREASE_E
		if cache >= 3 * INCREASE_E:
			self.ev[x][y] += INCREASE_E
		cache = 0
		for i in range(1, DEPTH+1):
			if x - i < 0 or y + i >= self.chessboard_size or chessboard[x - i][y + i] == self.color:
				break
			elif self.ev[x][y] == 0 and chessboard[x - i][y + i] == 0:
				break
			elif chessboard[x - i][y + i] == -self.color:
				self.ev[x][y] += INCREASE_E
				cache += INCREASE_E
			elif self.ev[x][y]:
				self.ev[x][y] -= DECREASE_E
		if cache >= 3 * INCREASE_E:
			self.ev[x][y] += INCREASE_E
		cache = 0
		for i in range(1, DEPTH+1):
			if x + i >= self.chessboard_size or y - i < 0 or chessboard[x + i][y - i] == self.color:
				break
			elif self.ev[x][y] == 0 and chessboard[x + i][y - i] == 0:
				break
			elif chessboard[x + i][y - i] == -self.color:
				self.ev[x][y] += INCREASE_E
				cache += INCREASE_E
			elif self.ev[x][y]:
				self.ev[x][y] -= DECREASE_E
		if cache >= 3 * INCREASE_E:
			self.ev[x][y] += INCREASE_E
		cache = 0
		for i in range(1, DEPTH+1):
			if x + i >= self.chessboard_size or y + i >= self.chessboard_size or chessboard[x + i][y + i] == self.color:
				break
			elif self.ev[x][y] == 0 and chessboard[x + i][y + i] == 0:
				break
			elif chessboard[x + i][y + i] == -self.color:
				self.ev[x][y] += INCREASE_E
				cache += INCREASE_E
			elif self.ev[x][y]:
				self.ev[x][y] -= DECREASE_E
		if cache >= 3 * INCREASE_E:
			self.ev[x][y] += INCREASE_E
		cache = 0

	def choose(self, idx, chessboard):
		score = 0
		x, y = idx[int(len(idx)/2)]
		for i, j in idx:
			c = self.iv[i][j] * PRIORITY + self.ev[i][j]
			c += self.countNear(i, j, chessboard)
			print('======', (i, j), '======')
			print(self.iv[i][j], self.ev[i][j], c)
			if c > score:
				print('Score update', (i, j), c)
				score = c
				x, y = i, j
		return x, y

	def countNear(self, x, y, chessboard):
		bias = 0
		if x - 1 >= 0 and chessboard[x-1][y] != 0:
			bias += BIAS
		if x - 1 >= 0 and y - 1 >= 0 and chessboard[x-1][y-1] != 0:
			bias += BIAS
		if y - 1 >= 0 and chessboard[x][y-1] != 0:
			bias += BIAS
		if x + 1 < self.chessboard_size and y - 1 >= 0 and chessboard[x+1][y-1] != 0:
			bias += BIAS
		if x + 1 < self.chessboard_size and chessboard[x+1][y] != 0:
			bias += BIAS
		if y + 1 < self.chessboard_size and chessboard[x][y+1] != 0:
			bias += BIAS
		if x - 1 >= 0 and y + 1 < self.chessboard_size and chessboard[x-1][y+1] != 0:
			bias += BIAS
		if x + 1 < self.chessboard_size and y + 1 < self.chessboard_size and chessboard[x+1][y+1] != 0:
			bias += BIAS
		return min(bias, 2 * BIAS)
