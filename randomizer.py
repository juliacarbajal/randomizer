import random
import math

# LOAD THE LISTS
# List A
listA = []
with open('listA.txt') as f:
	for line in f:
		listA.append(line.strip())

# List B
listB = []
with open('listB.txt') as f:
	for line in f:
		listB.append(line.strip())

# Shuffle the lists
random.shuffle(listA)
random.shuffle(listB)

# NUMBER OF ITEMS
nItemsA = 20#len(listA)
nItemsB = 30#len(listB)


# DEFINE CONSTRAINTS
# Max number of same kind in a row:
maxRep = 2

if nItemsA == nItemsB:
	# Number of blocks:
	nBlocks = nItemsA/float(maxRep)
	nBlocksFloor = math.floor(nBlocks)
	maxAperBlock = maxRep
	maxBperBlock = maxRep
else:
	# Note: if length of lists is unequal, behavior is for the moment unreliable (work in progress)
	if max(nItemsA,nItemsB)/float(min(nItemsA,nItemsB)) - math.floor(max(nItemsA,nItemsB)/float(min(nItemsA,nItemsB))) <=0.5:
		nBlocks = min(float(nItemsA),float(nItemsB),min(nItemsA/float(maxRep),nItemsB/float(maxRep)))
	else:
		nBlocks = min(float(nItemsA),float(nItemsB),max(nItemsA/float(maxRep),nItemsB/float(maxRep)))
	nBlocksFloor = math.floor(nBlocks)
	maxAperBlock = max(1,int(math.floor(nItemsA/nBlocks)))
	maxBperBlock = max(1,int(math.floor(nItemsB/nBlocks)))

maxAstart = maxAperBlock
maxBstart = maxBperBlock
if maxAperBlock < maxBperBlock:
	maxAstart = maxAstart - 1
elif maxAperBlock > maxBperBlock:
	maxBstart = maxBstart -1
		
print nBlocks
print nBlocksFloor
print maxAperBlock
print maxBperBlock

# FUNCTIONS
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

# This function initializes a block based on constraints and previous blocks.
def InitializeBlock(nAlast, nBlast, maxRep, nAleft, nBleft):
	blockList = ''
	# If last block finished with A sequence:
	if nAlast >0:
		addA = random.choice(range(0,max(maxRep-nAlast+1,1)))
		addB = random.choice(range(1,maxRep+1))
		blockList += ('A'*addA)+('B'*addB)
	# If last block finished with B sequence:
	elif nBlast >0:
		addA = 0
		addB = random.choice(range(0,max(maxRep-nBlast+1,1)))
		blockList += ('B'*addB)
	# If it is the first block:
	else:
		addA = 0
		addB = random.choice([0,1]) # Random chance of starting with A or B
		if addB == 1:
			addB = random.choice(range(1,maxRep+1))
		blockList += ('B'*addB)
	nAleft -= addA
	nBleft -= addB
	# Correction to make sure we don't run out of B when initializing list:
	if len(blockList)>0 and addB>0 and addB == 0:
		nBleft += len(blockList)-maxBstart
		blockList = 'B'*min(len(blockList),maxBstart)
	return blockList, nAleft, nBleft

def Randomize(nAlast, nBlast, maxRep, nAleft, nBleft):
	blockList, nAleft, nBleft = InitializeBlock(nAlast, nBlast, maxRep, nAleft, nBleft)		
	while (nAleft>0 or nBleft>0):
		if len(blockList) == 0:
			# Correction to make sure we don't run out of A when initializing list:
			addA = min(nAleft,random.choice(range(1,maxAstart+1)))
		else:
			addA = min(nAleft,random.choice(range(1,maxRep+1)))
		addB = min(nBleft,random.choice(range(1,maxRep+1)))
		blockList += ('A'*addA) # Add 1 or 2 elements from list A
		blockList += ('B'*addB) # Add 1 or 2 elements from list B
		nAleft -= addA
		nBleft -= addB
	return blockList, nAleft, nBleft
	
# RANDOMIZE
# if nItemsA != nItemsB:
	# print 'Error: Number of items in lists is not equal! Cannot compute randomization.'
# else:
nAlast = 0
nBlast = 0
randomizedList = ''

# Complete blocks:
for block in range(1,int(nBlocksFloor)+1):
	nAleft = maxAperBlock
	nBleft = maxBperBlock
	blockList, nAleft, nBleft = Randomize(nAlast, nBlast, maxRep, nAleft, nBleft)
	randomizedList += blockList
	print blockList
	nAlast, nBlast = CheckLastSequence(blockList)

# Last block (only applies if list incomplete due to constraints):
if len(randomizedList) < nItemsA + nItemsB:
	nAleft = nItemsA - block*maxAperBlock
	nBleft = nItemsB - block*maxBperBlock
	maxRepFinal = int(min(maxRep,max(math.ceil(nAleft),math.ceil(nBleft))))
	finalBlock, nAleft, nBleft = Randomize(nAlast, nBlast, maxRepFinal, nAleft, nBleft)
	randomizedList += finalBlock
	
print randomizedList
print len(randomizedList)
	
	# # Assign values from lists:
	# A = 0
	# B = 0
	# randomizedItems = []
	# for item in randomizedList:
		# if item == 'A':
			# randomizedItems.append(listA[A])
			# A += 1
		# else:
			# randomizedItems.append(listB[B])
			# B += 1
	# print randomizedItems