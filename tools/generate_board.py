def main():
	f = open('chess_log.txt', 'r')
	rs1 = ''
	rs2 = ''
	while True:
		str = f.readline()
		if str == '':
			break
		ls = str.split(',')
		if ls[2] == '1\n':
			rs1 += 'board[' + ls[0] + ',' + ls[1] + ']='
		else:
			rs2 += 'board[' + ls[0] + ',' + ls[1] + ']='
	print(rs1, '1\n', rs2, '-1')

if __name__ == '__main__':
	main()
