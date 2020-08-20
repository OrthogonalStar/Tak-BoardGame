import pytest, AuxiliaryTestingMethods as aux, End

def testPoints(takGame):
    aux.resetBoard(takGame)
    assert End.points(takGame.board, takGame.pieces, takGame.capstones) == takGame.pieces + takGame.capstones + (takGame.board.size**2)
    aux.fillRow(takGame, 0, 1)
    aux.fillSpace(takGame, [0, 0], 0)
    assert End.points(takGame.board, takGame.pieces, takGame.capstones) == takGame.pieces + takGame.capstones + (takGame.board.size**2) - (takGame.board.size-1)
    aux.fillRow(takGame, 1, -1)
    aux.fillRow(takGame, 2, -1)
    assert End.points(takGame.board, takGame.pieces, takGame.capstones) == takGame.pieces + takGame.capstones + (takGame.board.size**2) - (takGame.board.size*2)

def testWinnerRoad(takGame):
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, 1)
    assert End.winRoad(takGame.board) == 1
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, -1)
    assert End.winRoad(takGame.board) == 2
    aux.resetBoard(takGame)
    assert End.winRoad(takGame.board) == False

def testWinnerOther(takGame):
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, 1)
    aux.fillRow(takGame, 1, 1)
    aux.fillCol(takGame, takGame.board.size-1, 0)
    assert End.winner(takGame.board) == 1
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, -1)
    aux.fillRow(takGame, 1, -1)
    aux.fillCol(takGame, takGame.board.size-1, 0)
    assert End.winner(takGame.board) == 2
    aux.fillRow(takGame, 0, 1)
    aux.fillSpace(takGame, [0, takGame.board.size-1], 0)
    assert End.winner(takGame.board) == 2

@pytest.fixture(scope='module')
def takGame():
	import Tak
	return Tak.TakGame(5)
