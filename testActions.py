import pytest, AuxiliaryTestingMethods as aux, Actions

def testPlace(takGame):
    aux.resetBoard(takGame)
    Actions.place(takGame.board, [1, 1], 1)
    assert takGame.board.board[1][1][0] == 1

def testMove(takGame):
    aux.resetBoard(takGame)
    Actions.place(takGame.board, [1, 1], 1)
    Actions.place(takGame.board, [1, 2], 1)
    Actions.move(takGame.board, [1, 1], [1, 2], [1])
    assert takGame.board.board[1][2][0] == 1
    assert takGame.board.board[1][2][1] == 1
    assert takGame.board.board[1][1][0] == 0
    Actions.move(takGame.board, [1, 2], [3, 2], [1,1])
    assert takGame.board.board[1][2][0] == 0
    assert takGame.board.board[2][2][0] == 1
    assert takGame.board.board[3][2][0] == 1

def testWall(takGame):
    aux.resetBoard(takGame)
    Actions.place(takGame.board, [1, 1], 1)
    Actions.place(takGame.board, [1, 2], 2)
    with pytest.raises(ValueError):
        Actions.move(takGame.board, [1,1], [1,2], [1])

def testCapstone(takGame):
    aux.resetBoard(takGame)
    Actions.place(takGame.board, [1, 1], 3)
    Actions.place(takGame.board, [1, 2], -2)
    Actions.move(takGame.board, [1, 1], [1, 2], [1])
    assert takGame.board.board[1][2][0] == -1
    assert takGame.board.board[1][2][1] == 3

def testCarryLimit(takGame):
    aux.resetBoard(takGame)
    takGame.board.board[1][1] = [1,1,1,1,1,1,1,1,1,1]
    with pytest.raises(ValueError):
        Actions.move(takGame.board, [1,1], [1,2], [9])

def testPiecesLeft(takGame):
    aux.resetBoard(takGame)
    Actions.place(takGame.board, [1,1], 3)
    with pytest.raises(ValueError):
        Actions.place(takGame.board, [0, 1], 3)

@pytest.fixture(scope='module')
def takGame():
	import Tak
	return Tak.TakGame(5)
