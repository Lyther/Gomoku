import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
DEPTH = 4   # 博弈树搜索的深度
PRIORITY_BONUS = 2  # 自己下子有先手优势，加成倍数
OBLIQUE_BONUS = 1.2 # 斜向连接比直接连接好，加成倍数
DIRECT_BONUS = 1.2  # 直接连接比跳子连接好，加成倍数

ONE = 10
TWO = 100
THREE = 1000
FOUR = 100000
FIVE = 10000000
B_ONE = 1
B_TWO = 10
B_THREE = 100
B_FOUR = 10000

# 全部的匹配模式，有一个问题是即便某点不能连成5子，依然会进行评估
# 修复方案是延长匹配列表，仅对能胜利的点给分
P_ONE = (0, 1, 0)
P_B_ONE = (0, 1, -1)
P_TWO = (0, 1, 1, 0)
P_TWO_2 = (0, 1, 0, 1, 0)
P_B_TWO = (0, 1, 1, -1)
P_B_TWO_2 = (0, 1, 0, 1, -1)
P_THREE = (0, 1, 1, 1, 0)
P_THREE_2 = (0, 1, 1, 0, 1, 0)
P_B_THREE = (0, 1, 1, 1, -1)
P_B_THREE_2 = (0, 1, 1, 0, 1, -1)
P_B_THREE_3 = (-1, 1, 1, 0, 1, 0)
P_FOUR = (0, 1, 1, 1, 1, 0)
P_B_FOUR = (1, 0, 1, 1, 1)
P_B_FOUR_2 = (1, 1, 0, 1, 1)
P_B_FOUR_3 = (0, 1, 1, 1, 1, -1)
P_FIVE = (1, 1, 1, 1, 1)

# 匹配模式的优先级表，在表前的先被匹配
PATTERN = {P_FIVE: FIVE * DIRECT_BONUS, P_FOUR: FOUR * DIRECT_BONUS,
           P_B_FOUR_3: B_FOUR * DIRECT_BONUS, P_B_FOUR: B_FOUR, P_B_FOUR_2: B_FOUR,
           P_THREE: THREE * DIRECT_BONUS, P_THREE_2: THREE,
           P_B_THREE: B_THREE * DIRECT_BONUS, P_B_THREE_3: B_THREE, P_B_THREE_2: B_THREE,
           P_TWO: TWO * DIRECT_BONUS, P_TWO_2: TWO, P_B_TWO: B_TWO * DIRECT_BONUS, P_B_TWO_2: B_TWO,
           P_ONE: ONE, P_B_ONE: B_ONE}


# 假定在(x, y)落子后，我能取得的收益
def earn(board, role, x, y, size, direction):
	earning = 0
	if role == 1:
		# 落子后黑棋（对手）取得收益的情况
		earning += evaluate(board, x, y, COLOR_BLACK, size, direction)
		# 落子后白棋（我）取得收益的情况，有先手优势额外加成
		earning += evaluate(board, x, y, COLOR_WHITE, size, direction) * PRIORITY_BONUS
	else:
		# 落子后黑棋（我）取得收益的情况，有先手优势额外加成
		earning += evaluate(board, x, y, COLOR_BLACK, size, direction) * PRIORITY_BONUS
		# 落子后白棋（对手）取得收益的情况
		earning += evaluate(board, x, y, COLOR_WHITE, size, direction)
	return earning


# 假定在(x, y)落子后，评估此点的得分
def evaluate(board, x, y, color, size, direction):
	radius = 6
	score = 0
	board[x, y] = color
	if direction == 1 or direction == 0:  # 横向判断
		left = max(0, y - radius)
		right = min(size, y + radius)
		pattern = board[x, left:right].tolist()
		score += match(color, pattern)
	if direction == 2 or direction == 0:  # 纵向判断
		top = max(0, x - radius)
		down = min(size, x + radius)
		pattern = board[top:down, y].tolist()
		score += match(color, pattern)
	if direction == 3 or direction == 0:  # 左下到右上
		left = right = y
		top = down = x
		for i in range(radius):
			if left <= 0 or down >= size - 1:
				break
			left -= 1
			down += 1
		for i in range(radius):
			if right >= size or top <= -1:
				break
			right += 1
			top -= 1
		pattern = []
		while left < right and down > top:
			pattern.append(board[down, left])
			left += 1
			down -= 1
		score += match(color, pattern) * OBLIQUE_BONUS
	if direction == 4 or direction == 0:  # 左上到右下
		left = right = y
		top = down = x
		for i in range(radius):
			if left <= 0 or top <= 0:
				break
			left -= 1
			top -= 1
		for i in range(radius):
			if right >= size or down >= size:
				break
			right += 1
			down += 1
		pattern = []
		while left < right and top < down:
			pattern.append(board[top, left])
			left += 1
			top += 1
		score += match(color, pattern) * OBLIQUE_BONUS
	board[x, y] = COLOR_NONE
	return score


# 在列表中找对应串进行匹配，返回匹配到的最大得分
def match(color, pattern):
	# 锁定当前落子的角色颜色为1，敌人为-1
	if color == -1:
		pattern = [-i for i in pattern]
	for i in PATTERN.keys():  # 后期考虑换为KMP加速搜索
		ri = i[::-1]  # 匹配模式逆序
		for j in range(len(pattern) - len(i) + 1):
			sub = tuple(pattern[j:j + len(i)])
			if sub == i or sub == ri:
				return PATTERN[i]
	return 0


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
		# 上一步的棋盘，用来获取最新的落子
		self.history_board = np.zeros((chessboard_size, chessboard_size), dtype=np.int)

	# The input is current chessboard.
	def go(self, chessboard):
		self.candidate_list.clear()

		if np.array_equal(self.history_board, chessboard):  # 如果棋盘为空，直接落子中央
			new_pos = (7, 7)
		else:
			# 获取棋盘上空白的位置
			idx = np.where(chessboard == COLOR_NONE)
			idx = list(zip(idx[0], idx[1]))
			# 获取上一步敌人落子的位置
			idx_recent = np.where(self.history_board == COLOR_NONE)
			idx_recent = list(zip(idx_recent[0], idx_recent[1]))
			recent = [i for i in idx_recent if i not in idx][0]
			self.history_board = chessboard  # 同步棋盘状态
			# 确定收益最大的点
			# 后期考虑只计算上一步落子为中心，米字形区域内点的收益
			max_earning = -1
			new_pos = idx[int(len(idx) / 2)]
			for i in idx:
				earning = earn(chessboard, self.color, i[0], i[1], self.chessboard_size, 0)
				if earning > max_earning:
					max_earning = earning
					new_pos = i

		# 判定落子位置是否为空，并落子
		assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
		self.candidate_list.append(new_pos)
