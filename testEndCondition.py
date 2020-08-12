import pytest, AuxiliaryTestingMethods as aux

def testEndPieces(takGame):
	aux.resetBoard(takGame)
	correct = True
	aux.fillBoardEndPiece(takGame)
	if not takGame.end():
		correct = False
	assert correct

def testEndFull(takGame):
	aux.resetBoard(takGame)
	correct = True
	aux.fillBoardEndFull(takGame)
	if not takGame.end():
		correct = False
	assert correct

def testEndRoad(takGame):
	aux.resetBoard(takGame)
	aux.fillCol(takGame, 1, 1)
	assert takGame.end()

def testNotEnd(takGame):
	aux.resetBoard(takGame)
	assert not takGame.end()

@pytest.fixture(scope='module')
def takGame():
	import Tak
	return Tak.TakGame(5)
