import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

# My score for each state
iL2 = 10
iH2 = 50
iL3 = 100
iH3 = 500
iL4 = 1000
iH4 = 5000
iH5 = 10000
# Enemy's score for each state
eL2 = 15
eH2 = 55
eL3 = 105
eH3 = 505
eL4 = 1005
eH4 = 5005
eH5 = 10005


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

		self.score = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)

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

		if self.isEmpty(chessboard):
			new_pos = (7, 7)
		else:
			for (i, j) in idx:

		# ==============Find new pos========================================
		# Make sure that the position of your decision in chess board is empty.
		# If not, return error.
		assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
		# Add your decision into candidate_list, Records the chess board
		self.candidate_list.append(new_pos)

	def updateScore(self, x, y, chessboard):
		chessboard[x][y] = self.color
		self.score[x][y] = self.search(x, y, chessboard)

	# Search all the patterns (x, y) can be matched.
	def search(self, x, y, chessboard):
		result = 0
		for i in range(4):
			for j in range(len(self.types)):
				seq = self.getSubSeq(i, j, x, y, chessboard)
				if seq:
					score = self.match(seq, j)
					if score:
						result += score
						break
		return result

	# Find all the sub sequences containing (x, y) and matches index of types
	def getSubSeq(self, direction, index, x, y, chessboard):
		length = len(self.types[index])
		if direction == 0:  # In a row
			starty = max(0, y - length + 1)
			endy = min(self.chessboard_size, y + length)
			if endy - starty < length:
				return []
			else:
				return [chessboard[x, starty + i:starty + i + length].tolist() for i in range(endy - starty - length + 1)]
		elif direction == 1:    # In a column
			startx = max(0, x - length + 1)
			endx = min(self.chessboard_size, x + length)
			if endx - startx < length:
				return []
			else:
				return [chessboard[startx + i:startx + i + length, y].tolist() for i in range(endx - startx - length + 1)]
		elif direction == 2:    # In a diagonal
			startx = max(0, x - length + 1)
			endx = min(self.chessboard_size, x + length)
			starty = max(0, y - length + 1)
			endy = min(self.chessboard_size, y + length)
			if endx - startx < length or endy - starty < length:
				return []
			else:
				return [[chessboard[startx+j+i][starty+j+i] for i in range(length)] for j in range(min(endx - startx - length + 1, endy - starty - length + 1))]
		else:   # In a back-diagonal
			startx = x
			starty = y
			cur = length - 1
			while startx and starty and cur:
				startx += 1
				starty -= 1
				cur -= 1
			endx = max(-1, x - length - 1)
			endy = min(self.chessboard_size, y + length + 1)
			if x + y + 1 < length:
				return []
			else:
				return [[chessboard[startx-i-j][starty+i+j] for i in range(length)] for j in range(min(startx - endx - length, endy - starty - length))]

	# Verify whether a sequence matches index of types
	def match(self, seq, index):
		if self.types[index] == seq or self.types[index].reverse() == seq:
			return self.weight[str(self.types[index])]
		return 0

	# Check if chessboard is empty
	def isEmpty(self, chessboard):
		for i in range(self.chessboard_size):
			for j in range(self.chessboard_size):
				if chessboard[i][j] != 0:
					return False
		return True
