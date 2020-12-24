import argparse
parser = argparse.ArgumentParser()
import numpy as np
import pulp as p

def readMDP(f):
	f1 = open(f, 'r') 
	S = 0
	A = 0
	T = []
	R = []
	gamma = -1
	st = -1
	end = []
	while True: 
		 
		line = f1.readline() 

		# if line is empty 
		# end of file is reached 
		if not line: 
			break
		cur_line = line.strip()
		cur_line_list = cur_line.split()

		if cur_line_list[0] == 'numStates':
			S = int(cur_line_list[1])
		if cur_line_list[0] == 'numActions':
			A = int(cur_line_list[1])
			T = np.zeros((S, A, S))
			R = np.zeros((S, A, S))
		if cur_line_list[0] == 'transition':
			s1 = int(cur_line_list[1])
			a = int(cur_line_list[2])
			s2 = int(cur_line_list[3])
			r = float(cur_line_list[4])
			p = float(cur_line_list[5])
			T[s1,a,s2] = p
			R[s1,a,s2] = r
		if cur_line_list[0] == 'discount':
			gamma = float(cur_line_list[1])
		if cur_line_list[0] == 'end':
			end = [int(x) for x in cur_line_list[1:]]
		if cur_line_list[0] == 'start':
			st = int(cur_line_list[1])
	f1.close()

	return S,A,T,R,gamma,st,end 

def plan(f, algo):
	S,A,T,R,gamma,st,end = readMDP(f)
	#print('{}, {}, {}, {}, {}, {}, {}'.format(S,A,T,R,gamma,st,end))
	v,p = [],[]
	if algo == 'vi':
		v,p = vi(S,A,T,R,gamma)
	elif algo == 'hpi':
		v, p = hpi(S,A,T,R,gamma)
	elif algo == 'lp':
		v, p = lp(S,A,T,R,gamma)	
	else:
		print("Algo not found")
		return
	
	for value,action in zip(v,p):
		print("{:.6f} {}".format(value, action))

	return

def vi(S,A,T,R,gamma):
	np.random.seed(747)
	v2 = np.random.rand(S)
	policy = [-1 for i in range(S)]
	while True:
		v1 = v2.copy()
		#print(v1)
		v2 = np.zeros(S)
		for s in range(S):
			q = np.zeros(A)
			for a in range(A):
				q[a] = np.sum(T[s,a,:]*(R[s,a,:] + (gamma*v1)))
			v2[s], policy[s] = np.max(q), np.argmax(q)
			#print(s,v1)
		if np.max(abs(v2-v1)) < 1e-10:
			break
	return v2,policy

def hpi(S,A,T,R,gamma):
	np.random.seed(747)
	M = np.zeros((S,S))
	y = np.zeros((S,1))
	p2 = [np.random.randint(A) for i in range(S)]

	while True:
		p1 = p2.copy()
		for s1 in range(S):
			for s2 in range(S):
				M[s1,s2] = gamma * T[s1,p1[s1],s2]
			M[s1,s1] -= 1
			y[s1] = - np.sum(T[s1,p1[s1],:]*R[s1,p1[s1],:])
		v1 = (np.linalg.inv(M) @ y).reshape(S,)
		for s in range(S):
			q = np.zeros(A)
			choices = []
			for a in range(A):
				q[a] = np.sum(T[s,a,:]*(R[s,a,:] + (gamma*v1)))
				if q[a] > v1[s]+1e-10 and a != p1[s]:
					choices.append(a)
			if choices:
				p2[s] = np.random.choice(choices)
			else:
				p2[s] = p1[s]

		if np.array_equal(p1,p2):
			return v1,p1

def lp(S,A,T,R,gamma):
	lp_prob = p.LpProblem('Problem', p.LpMinimize)
	v1 = []
	obj = []
	for s in range(S):
		v1.append(p.LpVariable(f"v_{s}"))
		obj.append((v1[s],1))
	lp_prob += p.LpAffineExpression(obj)
	for s in range(S):
		for a in range(A):
			constraint = []
			for s2 in range(S):
				if s != s2:
					constraint.append((v1[s2], - gamma * T[s,a,s2]))
				else:
					constraint.append((v1[s2], 1 - gamma * T[s,a,s2]))
			rhs = np.sum(T[s,a,:] * R[s,a,:])
			lp_prob += p.LpAffineExpression(constraint) >= rhs
	#print(lp_prob)
	status = lp_prob.solve(p.PULP_CBC_CMD(msg=0))
	for s in range(S):
		v1[s] = p.value(v1[s])
	policy = [-1 for i in range(S)]
	for s in range(S):
		q = np.zeros(A)
		for a in range(A):
			q[a] = np.sum(T[s,a,:]*(R[s,a,:] + (gamma*np.array(v1))))
		policy[s] = np.argmax(q)
	return v1,policy


if __name__ == "__main__":
	parser.add_argument("--mdp",type=str)
	parser.add_argument("--algorithm",type=str)

	args = parser.parse_args()
	infile = args.mdp
	algo = args.algorithm
	plan(infile, algo)