import pytest

def testPieceCounts(takGame):
	size = takGame.board.size
	pieces = takGame.pieces
	capstones = takGame.capstones
	correct = False
	if size == 8 and pieces == 50 and capstones == 2:
		correct = True
	elif size == 7 and pieces == 40 and capstones == 2:
		correct = True
	elif size == 6 and pieces == 30 and capstones == 1:
		correct = True
	elif size == 5 and pieces == 21 and capstones == 1:
		correct = True
	elif size == 4 and pieces == 15 and capstones == 0:
		correct = True
	elif size == 3 and pieces == 10 and capstones == 0:
		correct = True
	assert correct

def testIsAdjacent(takGame):
	res = True
	size = takGame.board.size
	testLoc = [size//2, size//2]
	for i in range(size):
		for j in range(size):
			if (((i==size//2 and abs(j-size//2) ==1) or (j==size//2 and abs(i-size//2) == 1))
			 		is not takGame.board.isAdjacent(testLoc, [i, j])):
				res = False
	assert res

def testAdjacent(takGame):
	correct = True
	location = [1, 1]
	result = [[0, 1], [1, 0], [1, 2], [2, 1]]
	testRes = takGame.board.adjacent(location)
	for loc in result:
		if loc not in testRes:
			correct = False
	location = [0,0]
	result = [[0, 1], [1, 0]]
	testRes = takGame.board.adjacent(location)
	for loc in result:
		if loc not in testRes:
			correct = False
	assert correct

@pytest.fixture(scope='module')
def takGame():
	import Tak
	return Tak.TakGame(5)
