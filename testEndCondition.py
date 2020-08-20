import pytest, AuxiliaryTestingMethods as aux, End

def testEndPieces(takGame):
	aux.resetBoard(takGame)
	correct = True
	aux.fillBoardEndPiece(takGame)
	if not End.end(takGame.board, takGame.pieces, takGame.capstones):
		correct = False
	assert correct

def testEndFull(takGame):
	aux.resetBoard(takGame)
	correct = True
	aux.fillBoardEndFull(takGame)
	if not End.end(takGame.board, takGame.pieces, takGame.capstones):
		correct = False
	assert correct

def testEndRoad(takGame):
	aux.resetBoard(takGame)
	aux.fillCol(takGame, 1, 1)
	assert End.end(takGame.board, takGame.pieces, takGame.capstones)

def testNotEnd(takGame):
	aux.resetBoard(takGame)
	assert not End.end(takGame.board, takGame.pieces, takGame.capstones)

@pytest.fixture(scope='module')
def takGame():
	import Tak
	return Tak.TakGame(5)
