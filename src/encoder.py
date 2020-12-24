import argparse
parser = argparse.ArgumentParser()
import numpy as np


# 0->N, 1->E, 2->W, 3->S
def generateMDP(f):
	grid = np.loadtxt(f)
	S = 0
	A = 4
	end = []
	st = -1
	y = -1
	x = -1
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
				grid[i,j] = 0
			elif grid[i,j] == 3:
				label_grid[i,j] = S
				end.append(S)
				S += 1
				grid[i,j] = 0
				y = i
				x = j

	T = - np.ones((S,A)).astype(int)
	for i in range(grid.shape[0]):
		for j in range(grid.shape[1]):
			if grid[i,j] == 0 and label_grid[i,j] not in end:
				if i+1 < grid.shape[0] and grid[i+1,j] == 0:
					T[label_grid[i,j],3] = label_grid[i+1,j]
				else:
					T[label_grid[i,j],3] = label_grid[i,j]
				if j+1 < grid.shape[1] and grid[i,j+1] == 0:
					T[label_grid[i,j],1] = label_grid[i,j+1]
				else:
					T[label_grid[i,j],1] = label_grid[i,j]
				if i-1 >= 0 and grid[i-1,j] == 0:
					T[label_grid[i,j],0] = label_grid[i-1,j]
				else:
					T[label_grid[i,j],0] = label_grid[i,j]
				if j-1 >= 0 and grid[i,j-1] == 0:
					T[label_grid[i,j],2] = label_grid[i,j-1]
				else:
					T[label_grid[i,j],2] = label_grid[i,j]

	r = -1 # for all transitions, because we want the shortest path
	gamma = 1
	print('numStates {}'.format(S))
	print('numActions {}'.format(A))
	print('start {}'.format(st))
	print('end {}'.format(" ".join([str(ed) for ed in end])))
	for s1 in range(S):
		for a in range(A):
			if T[s1,a] != -1:
				print('transition {} {} {} {} {}'.format(s1,a,T[s1,a],r,1.0))
	print('mdptype continuing')
	print('discount {}'.format(gamma))

	return


if __name__ == "__main__":
	parser.add_argument("--grid",type=str)
	
	args = parser.parse_args()
	infile = args.grid
	generateMDP(infile)