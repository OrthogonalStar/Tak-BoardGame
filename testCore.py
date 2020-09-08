import pytest, AuxiliaryTestingMethods as aux
from copy import deepcopy

def testLogAction(takGame):
    board = deepcopy(takGame.board.board)
    takGame.logAction()
    assert(takGame.history[-1] == board)

def testUndo(takGame):
    board = deepcopy(takGame.board.board)
    takGame.actPlace(1, [0,0], 1)
    assert (board != takGame.board.board)
    takGame.undo()
    assert(board == takGame.board.board)

def testGetEndResults(takGame):
    aux.fillRow(takGame, 0, 1)
    takGame.turnCount += 1
    assert(takGame.getEndResults() == (1, 42))

def testActPlace(takGame):
    aux.resetBoard(takGame)
    takGame.actPlace(1, [1,1], 1)
    assert(takGame.turnCount == 2)
    assert(takGame.board.board[1][1][0] == -1)

def testCheckLegalPlacement(takGame):
    aux.resetBoard(takGame)
    takGame.actPlace(1, [1,1], 1)
    assert(takGame.checkLegalPlacement([0,0]))
    assert(not takGame.checkLegalPlacement([1,1]))

def testActMove(takGame):
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, 1)
    takGame.actMove([0,0], [1,0], [1])
    assert(takGame.board.board[0][0][0] == 0)
    assert(takGame.board.board[1][0][0] == 1)
    assert(takGame.turnCount == 2)

def testCheckLegalMoveStart(takGame):
    aux.resetBoard(takGame)
    aux.fillSpace(takGame, [2,0], -1)
    assert(takGame.checkLegalMoveStart(2, [2,0]))
    assert(not takGame.checkLegalMoveStart(1, [2,0]))

def testCheckLegalDrop(takGame):
    aux.resetBoard(takGame)
    aux.fillSpace(takGame, [0,0], 3)
    aux.fillSpace(takGame, [0,1], 2)
    aux.fillSpace(takGame, [0,2], 1)
    assert(not takGame.checkLegalDrop([0,0], 1))
    assert(not takGame.checkLegalDrop([0,0], 2))
    assert(not takGame.checkLegalDrop([0,0], 3))
    assert(not takGame.checkLegalDrop([0,1], 1))
    assert(not takGame.checkLegalDrop([0,1], 2))
    assert(takGame.checkLegalDrop([0,1], 3))
    assert(takGame.checkLegalDrop([0,2], 1))

def testPiecesLeft(takGame):
    aux.resetBoard(takGame)
    aux.fillRow(takGame, 0, 1)
    assert(takGame.piecesLeft(1) == (16, 1))
    aux.fillSpace(takGame, [1,1], 3)
    assert(takGame.piecesLeft(1) == (16, 0))





@pytest.fixture(scope='module')
def takGame():
	import Tak
	return Tak.TakGame(5)
