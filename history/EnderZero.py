import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

# My score for each state
iL2 = 20
iH2 = 40
iL3 = 60
iH3 = 80
iL4 = 100
iH4 = 1000
iH5 = 10000
# Enemy's score for each state
eL2 = 30
eH2 = 50
eL3 = 70
eH3 = 90
eL4 = 110
eH4 = 1100
eH5 = 11000


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

		# Initial AI
		# All possible types on board
		ih5 = [self.color, self.color, self.color, self.color, self.color]
		ih4 = [0, self.color, self.color, self.color, self.color, 0]
		il41 = [0, self.color, self.color, self.color, self.color, -self.color]
		il42 = [self.color, 0, self.color, self.color, self.color]
		il43 = [self.color, self.color, 0, self.color, self.color]
		ih31 = [0, self.color, self.color, self.color, 0]
		ih32 = [self.color, 0, self.color, self.color]
		il31 = [0, 0, self.color, self.color, self.color, -self.color]
		il32 = [0, self.color, 0, self.color, self.color, -self.color]
		il33 = [0, self.color, self.color, 0, self.color, -self.color]
		il34 = [self.color, 0, 0, self.color, self.color]
		il35 = [self.color, 0, self.color, 0, self.color]
		il36 = [-self.color, 0, self.color, self.color, self.color, 0, -self.color]
		ih21 = [0, 0, self.color, self.color, 0, 0]
		ih22 = [0, self.color, 0, self.color, 0]
		ih23 = [self.color, 0, 0, self.color]
		il21 = [0, 0, 0, self.color, self.color, -self.color]
		il22 = [0, 0, self.color, 0, self.color, -self.color]
		il23 = [0, self.color, 0, 0, self.color, -self.color]
		il24 = [self.color, 0, 0, 0, self.color]

		eh5 = [-self.color, -self.color, -self.color, -self.color, -self.color]
		eh4 = [0, -self.color, -self.color, -self.color, -self.color, 0]
		el41 = [0, -self.color, -self.color, -self.color, -self.color, self.color]
		el42 = [-self.color, 0, -self.color, -self.color, -self.color]
		el43 = [-self.color, -self.color, 0, -self.color, -self.color]
		eh31 = [0, -self.color, -self.color, -self.color, 0]
		eh32 = [-self.color, 0, -self.color, -self.color]
		eh33 = [-self.color, -self.color, 0, -self.color]
		el31 = [0, 0, -self.color, -self.color, -self.color, self.color]
		el32 = [0, -self.color, 0, -self.color, -self.color, self.color]
		el33 = [0, -self.color, -self.color, 0, -self.color, self.color]
		el34 = [-self.color, 0, 0, -self.color, -self.color]
		el35 = [-self.color, 0, -self.color, 0, -self.color]
		el36 = [self.color, 0, -self.color, -self.color, -self.color, 0, self.color]
		eh21 = [0, 0, -self.color, -self.color, 0, 0]
		eh22 = [0, -self.color, 0, -self.color, 0]
		eh23 = [-self.color, 0, 0, -self.color]
		el21 = [0, 0, 0, -self.color, -self.color, self.color]
		el22 = [0, 0, -self.color, 0, -self.color, self.color]
		el23 = [0, -self.color, 0, 0, -self.color, self.color]
		el24 = [-self.color, 0, 0, 0, -self.color]

		self.types = [ih5, ih4, il41, il42, il43, ih31, ih32, il31, il32, il33, il34, il35, il36, ih21, ih22, ih23, il21, il22, il23, il24, eh5, eh4, el41, el42, el43, eh31, eh32, eh33, el31, el32, el33, el34, el35, el36, eh21, eh22, eh23, el21, el22, el23, el24]
		self.weight = {str(ih5): iH5, str(ih4): iH4, str(il41): iL4, str(il42): iL4, str(il43): iL4, str(ih31): iH3, str(ih32): iH3, str(il31): iL3, str(il32): iL3, str(il33): iL3, str(il34): iL3, str(il35): iL3, str(il36): iL3, str(ih21): iH2, str(ih22): iH2, str(ih23): iH2, str(il21): iL2, str(il22): iL2, str(il23): iL2, str(il24): iL2, str(eh5): eH5, str(eh4): eH4, str(el41): eL4, str(el42): eL4, str(el43): eL4, str(eh31): eH3, str(eh32): eH3, str(eh33): eH3, str(el31): eL3, str(el32): eL3, str(el33): eL3, str(el34): eL3, str(el35): eL3, str(el36): eL3, str(eh21): eH2, str(eh22): eH2, str(eh23): eH2, str(el21): eL2, str(el22): eL2, str(el23): eL2, str(el24): eL2}

		self.board = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
		self.scores = {}
		self.links = 4
		self.recent = (-1, -1)
		self.maxScores = {}

	# The input is current chessboard.
	def go(self, chessboard):
		print('Get chessboard: \n')
		print(chessboard)
		found = False
		for i in range(self.chessboard_size):
			if found:
				break
			for j in range(self.chessboard_size):
				if found:
					break
				if chessboard[i][j] != self.board[i][j] and chessboard[i][j] != self.color:
					self.recent = (i, j)
					found = True
		print('Find recent index: ')
		print(self.recent)
		self.board = chessboard
		# Clear candidate_list
		self.candidate_list.clear()
		# ==================================================================
		# Write your algorithm here
		# Here is the simplest sample:Random decision
		idx = np.where(chessboard == COLOR_NONE)
		idx = list(zip(idx[0], idx[1]))
		print('Get empty spaces: \n')
		print(idx)

		if self.color == -1 and self.recent == (-1, -1):
			new_pos = (7, 7)
		elif len(idx) == 1:
			new_pos = idx[0]
		else:
			for i in range(self.chessboard_size):
				for j in range(self.chessboard_size):
					if (i, j) in idx:
						self.scores = {}
						for k in range(4, 8):
							self.search_row(i, j, k)
						self.maxScores = self.scores
						for k in range(4, 8):
							self.search_col(i, j, k)
						for k in range(4, 8):
							self.search_ob1(i, j, k)
						for k in range(4, 8):
							self.search_ob2(i, j, k)
			new_pos = self.choose()
		print('Get next step: ')
		print(new_pos)
		# ==============Find new pos========================================
		# Make sure that the position of your decision in chess board is empty.
		# If not, return error.
		assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
		# Add your decision into candidate_list, Records the chess board
		self.candidate_list.append(new_pos)

	def search_row(self, row, column, length):
		for i in range(self.chessboard_size - length):
			if column in range(i, i + length):
				tpls = self.board[row, i:i+length].tolist()
				tpls[column - i] = self.color
				key = str((row, column))
				if tpls in self.types:
					if key in self.scores:
						self.scores[key] = max(self.weight[str(tpls)], self.scores[key])
					else:
						self.scores[key] = self.weight[str(tpls)]
				tpls[column - i] = -self.color
				if tpls in self.types:
					if key in self.scores:
						self.scores[key] = max(self.weight[str(tpls)], self.scores[key])
					else:
						self.scores[key] = self.weight[str(tpls)]
				else:
					if key in self.scores:
						self.scores[key] = max(tpls.count(self.color), tpls.count(-self.color), self.scores[key])
					else:
						self.scores[key] = max(tpls.count(self.color), tpls.count(-self.color))

	def search_col(self, row, column, length):
		for i in range(self.chessboard_size - length):
			if row in range(i, i + length):
				tpls = self.board[i:i+length, column].tolist()
				tpls[row - i] = self.color
				key = str((row, column))
				if tpls in self.types:
					if key in self.scores:
						self.scores[key] = max(self.weight[str(tpls)], self.scores[key])
					else:
						self.scores[key] = self.weight[str(tpls)]
				tpls[row - i] = -self.color
				if tpls in self.types:
					if key in self.scores:
						self.scores[key] = max(self.weight[str(tpls)], self.scores[key])
					else:
						self.scores[key] = self.weight[str(tpls)]
				else:
					if key in self.scores:
						self.scores[key] = max(tpls.count(self.color), tpls.count(-self.color), self.scores[key])
					else:
						self.scores[key] = max(tpls.count(self.color), tpls.count(-self.color))

	def search_ob1(self, row, column, length):
		for i in range(self.chessboard_size - length):
			for j in range(self.chessboard_size - length):
				if row - i == column - j and row in range(i, i + length) and range(j, j + length):
					tpls = [self.board[i+k][j+k] for k in range(length)]
					tpls[row - i] = self.color
					key = str((row, column))
					if tpls in self.types:
						if key in self.scores:
							self.scores[key] = max(self.weight[str(tpls)], self.scores[key])
						else:
							self.scores[key] = self.weight[str(tpls)]
					tpls[row - i] = -self.color
					if tpls in self.types:
						if key in self.scores:
							self.scores[key] = max(self.weight[str(tpls)], self.scores[key])
						else:
							self.scores[key] = self.weight[str(tpls)]
					else:
						if key in self.scores:
							self.scores[key] = max(tpls.count(self.color), tpls.count(-self.color), self.scores[key])
						else:
							self.scores[key] = max(tpls.count(self.color), tpls.count(-self.color))

	def search_ob2(self, row, column, length):
		for i in range(self.chessboard_size - length):
			for j in range(length, self.chessboard_size):
				if row - i == -(column - j) and row in range(i, i + length) and range(j - length, j):
					tpls = [self.board[i+k][j-k] for k in range(length)]
					tpls[row - i] = self.color
					key = str((row, column))
					if tpls in self.types:
						if key in self.scores:
							self.scores[key] = max(self.weight[str(tpls)], self.scores[key])
						else:
							self.scores[key] = self.weight[str(tpls)]
					tpls[row - i] = -self.color
					if tpls in self.types:
						if key in self.scores:
							self.scores[key] = max(self.weight[str(tpls)], self.scores[key])
						else:
							self.scores[key] = self.weight[str(tpls)]
					else:
						if key in self.scores:
							self.scores[key] = max(tpls.count(self.color), tpls.count(-self.color), self.scores[key])
						else:
							self.scores[key] = max(tpls.count(self.color), tpls.count(-self.color))

	def choose(self):
		maximum = self.maxScores[max(self.maxScores, key=self.maxScores.get)]
		md = 1000
		(rx, ry) = (0, 0)
		for key, value in self.maxScores.items():
			if value == maximum:
				print(value)
				print(key)
				tup = key.split(', ')
				x = int(tup[0].strip('('))
				y = int(tup[1].strip(')'))
				distance = pow(self.recent[0] - x, 2) + pow(self.recent[1] - y, 2)
				if distance < md:
					md = distance
					(rx, ry) = (x, y)
		return (rx, ry)
