import pytest, AuxiliaryTestingMethods as aux

def testPoints(takGame):
    aux.resetBoard(takGame)
    assert takGame.points() == takGame.pieces + takGame.capstones + (takGame.size**2)
    aux.fillRow(takGame, 0, 1)
    aux.fillSpace(takGame, [0, 0], 0)
    assert takGame.points() == takGame.pieces + takGame.capstones + (takGame.size**2) - (takGame.size-1)
    aux.fillRow(takGame, 1, -1)
    aux.fillRow(takGame, 2, -1)
    assert takGame.points() == takGame.pieces + takGame.capstones + (takGame.size**2) - (takGame.size*2)

def testWinnerRoad(takGame):
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, 1)
    assert takGame.winRoad() == 1
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, -1)
    assert takGame.winRoad() == 2
    aux.resetBoard(takGame)
    assert takGame.winRoad() == False

def testWinnerOther(takGame):
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, 1)
    aux.fillRow(takGame, 1, 1)
    aux.fillCol(takGame, takGame.size-1, 0)
    assert takGame.winner() == 1
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, -1)
    aux.fillRow(takGame, 1, -1)
    aux.fillCol(takGame, takGame.size-1, 0)
    assert takGame.winner() == 2
    aux.fillRow(takGame, 0, 1)
    aux.fillSpace(takGame, [0, takGame.size-1], 0)
    takGame.printBoard
    assert takGame.winner() == 2

@pytest.fixture(scope='module')
def takGame():
	import Tak
	return Tak.TakGame(5)
