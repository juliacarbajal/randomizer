import random
import math

# LOAD THE LISTS
# List A
listA = []
with open('listA.txt') as f:
	for line in f:
		listA.append(line.strip())
nItemsA = 23#len(listA)
# List B
listB = []
with open('listB.txt') as f:
	for line in f:
		listB.append(line.strip())
nItemsB = 23#len(listB)
if nItemsA != nItemsB:
	print 'Warning: Number of items not equal! Cannot compute randomization.'

# CONSTRAINTS
# Max number of same kind in a row:
maxRep = 3

# Balance every K trials:
maxAperBlock = maxRep+1
balanceK = float(maxAperBlock*2)

# Number of blocks
nBlocks = 2*nItemsA/balanceK
nBlocksFloor = math.floor(nBlocks)

# First shuffle of lists
random.shuffle(listA)
random.shuffle(listB)

# This function checks how many repetitions of A and B appeared last in a sequence:
def CheckLastSequence(sequence):
	lastIsA = sequence[-1].count('A')
	same = True
	nsame = 1
	item = 2
	while item <= maxRep and same == True:
		if sequence[-item].count('A') == lastIsA:
			nsame +=1
		else:
			same = False
		item +=1
	if lastIsA == 1:
		nAlast = nsame
		nBlast = 0
	else:
		nAlast = 0
		nBlast = nsame
	return nAlast, nBlast
	
def InitializeBlock(nAlast, nBlast, maxRep, nAleft, nBleft):
	blockList = ''
	if nAlast >0:
		addA = random.choice(range(0,maxRep-nAlast+1))
		addB = random.choice(range(1,maxRep+1))
		blockList += ('A'*addA)+('B'*addB)
	elif nBlast >0:
		addA = 0
		addB = random.choice(range(0,maxRep-nBlast+1))
		blockList += ('B'*addB)
	else: # This case is the first block
		addA = 0
		addB = random.choice([0,1]) # Random chance of starting with A or B
		if addB == 1:
			addB = random.choice(range(1,maxRep+1))
		blockList += ('B'*addB)
	nAleft -= addA
	nBleft -= addB
	return blockList, nAleft, nBleft
	
# RANDOMIZE
nAlast = 0
nBlast = 0
	
for block in range(1,int(nBlocksFloor)+1):
	nAleft = maxAperBlock
	nBleft = nAleft
	# Initialize the block taking into account the last items of previous block:
	blockList, nAleft, nBleft = InitializeBlock(nAlast, nBlast, maxRep, nAleft, nBleft)
	while (nAleft>0 or nBleft>0):
		addA = min(nAleft,random.choice(range(1,maxRep+1)))
		addB = min(nBleft,random.choice(range(1,maxRep+1)))
		blockList += ('A'*addA) # Add 1 or 2 elements from list A
		blockList += ('B'*addB) # Add 1 or 2 elements from list B
		nAleft -= addA
		nBleft -= addB
	print blockList
	nAlast, nBlast = CheckLastSequence(blockList)


# Last block, if incomplete:
if nBlocks > nBlocksFloor:
	nAleft = nItemsA - block*maxAperBlock
	nBleft = nAleft
	maxRepFinal = min(maxRep,math.ceil(nAleft))
	blockList, nAleft, nBleft = InitializeBlock(nAlast, nBlast, maxRepFinal, nAleft, nBleft)
	while (nAleft>0 or nBleft>0):
		addA = min(nAleft,random.choice(range(1,maxRepFinal+1)))
		addB = min(nBleft,random.choice(range(1,maxRepFinal+1)))
		blockList+=('A'*addA)
		blockList+=('B'*addB)
		nAleft -= addA
		nBleft -= addB
	print blockList