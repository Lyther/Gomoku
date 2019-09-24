def simply():
	f = open("test", 'r')
	while True:
		string = f.readline()
		if string == '':
			break
		string = string.split("':")
		str1 = string[0]
		str2 = string[1]
		for i in str1:
			if i == '2':
				print('-1', end='')
			else:
				print(i, end='')
		print("':", str2, end='')

if __name__ == "__main__":
	simply()