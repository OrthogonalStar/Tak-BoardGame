import pytest, AuxiliaryTestingMethods as aux

def testTurn(takGame):
    assert takGame.turn()
    assert takGame.turnCount == 1

def testPlace(takGame):
    aux.resetBoard(takGame)
    takGame.place([1, 1], 1)
    assert takGame.board[1][1][0] == 1

def testMove(takGame):
    aux.resetBoard(takGame)
    takGame.place([1, 1], 1)
    takGame.place([1, 2], 1)
    takGame.move([1, 1], [1, 2], [1])
    assert takGame.board[1][2][0] == 1
    assert takGame.board[1][2][1] == 1
    assert takGame.board[1][1][0] == 0
    takGame.move([1, 2], [3, 2], [1,1])
    assert takGame.board[1][2][0] == 0
    assert takGame.board[2][2][0] == 1
    assert takGame.board[3][2][0] == 1

def testWall(takGame):
    aux.resetBoard(takGame)
    takGame.place([1, 1], 1)
    takGame.place([1, 2], 2)
    with pytest.raises(ValueError):
        takGame.move([1,1], [1,2], [1])

def testCapstone(takGame):
    aux.resetBoard(takGame)
    takGame.place([1, 1], 3)
    takGame.place([1, 2], 2)
    takGame.move([1, 1], [1, 2], [1])
    assert takGame.board[1][2][0] == 1
    assert takGame.board[1][2][1] == 3

@pytest.fixture(scope='module')
def takGame():
	import Tak
	return Tak.TakGame(5)
