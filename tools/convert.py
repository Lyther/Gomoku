import generate
SIZE = 15

def main(content):
	steps = []
	pre_index = 0
	index = 0
	for i in content:
		if i >= 'a' and i <= 'z':
			if index == 0:
				pass
			else:
				steps.append(content[pre_index:index])
				pre_index = index
		index += 1
	steps.append(content[pre_index:index])
	output(steps)

def output(steps):
	f = open('C:/Users/Enderaoe/Downloads/chess_log.txt', 'w')
	chess = []
	for i in steps:
		column = i[0]
		row = i[1:]
		column = int(ord(column) - ord('a'))
		row = SIZE - int(row)
		chess.append((row, column))
	color = -1
	for i in chess:
		f.write(str(i[0])+','+str(i[1])+','+str(color)+'\n')
		color = -color
	f.close()
	generate.init()

if __name__ == '__main__':
	while True:
		main(input())