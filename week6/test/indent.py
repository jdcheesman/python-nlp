import sys

indent = 0
f = open('training_tree.txt', 'r')
lines = f.readlines()


for line in lines:
		line = line.strip()
		for c in line:
			if c == '(':
				indent += 1
				tabs =  '\t' * indent
				sys.stdout.write('\n')
				sys.stdout.write(tabs)
				sys.stdout.write('(')
			elif c == ')':
				indent -= 1
				sys.stdout.write(')\n')
			else:
				sys.stdout.write(c)
