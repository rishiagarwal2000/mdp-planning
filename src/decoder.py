import argparse
parser = argparse.ArgumentParser()
import numpy as np


def decodeMDP(g,vp):
	grid = np.loadtxt(g)
	value_policy = np.loadtxt(vp)
	v = value_policy[:,0]
	p = value_policy[:,1].astype(int)
	#print(p)
	S = 0
	st = -1
	end = []
	x = -1
	y = -1

	to_move = ['N','E','W','S']
	label_grid = - np.ones(grid.shape).astype(int)
	for i in range(grid.shape[0]):
		for j in range(grid.shape[1]):
			if grid[i,j] == 0:
				label_grid[i,j] = S
				S += 1
			elif grid[i,j] == 2:
				label_grid[i,j] = S
				st = S
				S += 1
				x = j
				y = i
				grid[i,j] = 0
			elif grid[i,j] == 3:
				label_grid[i,j] = S
				end.append(S)
				S += 1
				grid[i,j] = 0
	moves = []
	cur = st
	#print(end)
	while cur not in end:
		#print(cur, y, x)
		moves.append(to_move[p[cur]])
		if p[cur] == 0:
			y -= 1
		elif p[cur] == 1:
			x += 1
		elif p[cur] == 2:
			x -= 1
		elif p[cur]==3:
			y += 1
		else:
			print('No such move')
		cur = label_grid[y,x]
		if grid[y,x] == 1:
			print('Invalid move')
	print(" ".join(moves))
	return

if __name__ == "__main__":
	parser.add_argument("--grid",type=str)
	parser.add_argument("--value_policy",type=str)

	args = parser.parse_args()
	gridfile = args.grid
	vpfile = args.value_policy
	decodeMDP(gridfile, vpfile)