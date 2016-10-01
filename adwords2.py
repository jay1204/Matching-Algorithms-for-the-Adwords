import numpy as np
import sys
import pandas as pd
import random
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

def load_data():
	"""
	load the queries.txt file
	"""
	with open("queries.txt",'r') as f:
		queries = f.read()[:-1].split('\n')

	bidder = pd.read_csv("bidder_dataset.csv")

	return queries, bidder

def sub_sub_greedy(x, key_AB, budgets):
	highbid = 0
	index  = -1
	for ad in key_AB[x]:
		if budgets['Budget'][ad[0]] >= ad[1] and highbid < ad[1]:
			highbid = ad[1]
			index = ad[0]
	if index != -1:
		budgets['Budget'][index] = budgets['Budget'][index] - highbid
	return highbid

def sub_greedy(x, key_AB, bidder,queries):
	budgets = bidder[['Advertiser','Budget']].groupby('Advertiser').sum()
	revenve = map(lambda x: sub_sub_greedy(x,key_AB,budgets), queries)
	random.shuffle(queries)


def greedy(queries,bidder):

	# create a dictionary with the key is the keyword in the bidder file and the value is the (Advertiser, Bid Value) tuple
	key_AB = {}
	for i in range(len(bidder)):
		if bidder['Keyword'][i] not in key_AB:
			key_AB[bidder['Keyword'][i]] = [(bidder['Advertiser'][i],round(bidder['Bid Value'][i],2))]
		else:
			key_AB[bidder['Keyword'][i]].append((bidder['Advertiser'][i],round(bidder['Bid Value'][i],2)))


	budgets = bidder[['Advertiser','Budget']].groupby('Advertiser').sum()
	totalBudgets = sum(budgets['Budget'])

	revenves = map(lambda x: sub_greedy(x, key_AB, bidder,queries), range(100))
	totalrevenve = sum(revenves)/100
	return revenves[0], 

	"""
	for count in range(100):
		#for query in queries:
		revenves = map(lambda x: sub_greedy(x,key_AB,budgets), queries)	
		revenve = sum(revenves)
		#revenve =  revenve + highbid
		if count == 0:
			original_revenve = revenve
		totalrevenve = totalrevenve + revenve
			# random shuffle
		random.shuffle(queries)
		budgets = bidder[['Advertiser','Budget']].groupby('Advertiser').sum()
		print count
	"""

	#totalrevenve = totalrevenve/100
	#return original_revenve, totalrevenve/totalBudgets

if __name__ == "__main__":
    main()














