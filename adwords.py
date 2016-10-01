import numpy as np
import sys
import random
import math
random.seed(0)

# User input for the method to use
if len(sys.argv) != 2:
    print "python adwords.py <method>"
    sys.exit(1)
method = sys.argv[1]

def main():
    queries, bidder = load_data()

    if method == 'greedy':
        revenve, ratio = greedy(queries, bidder)
        print revenve, ratio
    elif method == 'msvv':
        revenve, ratio = msvv(queries, bidder)
        print revenve, ratio
    elif method == 'balance':
        revenve, ratio = balance(queries, bidder)
        print revenve, ratio

def load_data():
	"""
	load the queries.txt file
	"""
	with open("queries.txt",'r') as f:
		queries = f.read()[:-1].split('\n')

	bidder = np.genfromtxt('bidder_dataset.csv',delimiter = ",",skip_header=1,dtype = "|S40")

	return queries, bidder

def sub_sub_greedy(x, key_AB, budgets):
	highbid = 0.0
	index  = -1
	for ad in key_AB[x]:
		if budgets[ad[0]] >= ad[1] and highbid < ad[1]:
			highbid = ad[1]
			index = ad[0]
	if index != -1:
		budgets[index] = budgets[index] - highbid
	return highbid

def sub_greedy(x, key_AB, bidder,queries):
    budgets = [float(x[3]) for x in bidder if x[3]!='']
    revenve = map(lambda x: sub_sub_greedy(x,key_AB,budgets), queries)
    random.shuffle(queries)
    total = sum(revenve)
    return total

def greedy(queries,bidder):
    key_AB = {}
    # create a dictionary with the key is the keyword in the bidder file and the value is the (Advertiser, Bid Value) tuple
    for x in bidder:
        if x[1] not in key_AB:
            key_AB[x[1]] = [(int(x[0]),float(x[2]))]
        else:
            key_AB[x[1]].append((int(x[0]),float(x[2])))

    revenves = map(lambda x: sub_greedy(x, key_AB, bidder,queries), range(100))
    budgets = [float(x[3]) for x in bidder if x[3]!='']
    totalrevenve = sum(revenves)/100
    totalBudgets = sum(budgets)
    return revenves[0],totalrevenve/totalBudgets

def sub_sub_msvv(x, key_AB, budgets, spent_budgets, Psi, original_budgets):
	highChance = -100
	highbid = 0.0
	index = -1
	for ad in key_AB[x]:
		if budgets[ad[0]] >= ad[1] and (highChance < (ad[1] * Psi[ad[0]])):
			highChance = ad[1] * Psi[ad[0]]
			highbid = ad[1]
			index  = ad[0]
	if index != -1:
		budgets[index] = budgets[index] - highbid
		spent_budgets[index] = spent_budgets[index] + highbid
		Psi[index] = 1.0 - math.exp( spent_budgets[index]/original_budgets[index]- 1)
	return highbid

def sub_msvv(x, key_AB, bidder, queries):
	budgets = [float(x[3]) for x in bidder if x[3]!='']
	original_budgets = budgets[:]
	spent_budgets = [0.0] * len(budgets)
	Psi = [1.0 - math.exp(-1)] * len(budgets)
	revenve = map(lambda x: sub_sub_msvv(x, key_AB, budgets, spent_budgets, Psi, original_budgets), queries)
	random.shuffle(queries)
	total = sum(revenve)
	return total

def msvv(queries,bidder):
	key_AB = {}
    # create a dictionary with the key is the keyword in the bidder file and the value is the (Advertiser, Bid Value) tuple
	for x in bidder:
		if x[1] not in key_AB:
			key_AB[x[1]] = [(int(x[0]),float(x[2]))]
		else:
			key_AB[x[1]].append((int(x[0]),float(x[2])))

	revenves = map(lambda x: sub_msvv(x, key_AB, bidder, queries), range(100))
	budgets = [float(x[3]) for x in bidder if x[3]!='']
	totalrevenve = sum(revenves)/100
	totalBudgets = sum(budgets)
	return revenves[0],totalrevenve/totalBudgets

def sub_sub_balance(x, key_AB, budgets):
	highbid = 0.0
	highBudget = 0.0
	index = -1
	for ad in key_AB[x]:
		if budgets[ad[0]] >= ad[1] and highBudget < budgets[ad[0]]:
			highBudget = budgets[ad[0]]
			highbid = ad[1]
			index  = ad[0]
	if index != -1:
		budgets[index] = budgets[index] - highbid
	return highbid

def sub_balance(x, key_AB, bidder, queries):
	budgets = [float(x[3]) for x in bidder if x[3]!='']
	revenve = map(lambda x: sub_sub_balance(x, key_AB, budgets), queries)
	random.shuffle(queries)
	total = sum(revenve)
	return total

def balance(queries,bidder):
	key_AB = {}
    # create a dictionary with the key is the keyword in the bidder file and the value is the (Advertiser, Bid Value) tuple
	for x in bidder:
		if x[1] not in key_AB:
			key_AB[x[1]] = [(int(x[0]),float(x[2]))]
		else:
			key_AB[x[1]].append((int(x[0]),float(x[2])))

	revenves = map(lambda x: sub_balance(x, key_AB, bidder, queries), range(100))
	budgets = [float(x[3]) for x in bidder if x[3]!='']
	totalrevenve = sum(revenves)/100
	totalBudgets = sum(budgets)
	return revenves[0],totalrevenve/totalBudgets	

if __name__ == "__main__":
    main()
