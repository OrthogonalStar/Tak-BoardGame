import pytest, AuxiliaryTestingMethods as aux, End

def testNoRoad(takGame):
	aux.resetBoard(takGame)
	ans = End.road(takGame.board)
	assert not ans[0] and not ans[1]

def testRoadVertical(takGame):
	correct = True
	aux.resetBoard(takGame)
	aux.fillCol(takGame, 1, 1)
	ans = End.road(takGame.board)
	assert ans[0] and not ans[1]
	aux.resetBoard(takGame)
	aux.fillCol(takGame, 1, -1)
	ans = End.road(takGame.board)
	assert ans[1] and not ans[0]

def testRoadHorizontal(takGame):
	correct = True
	aux.resetBoard(takGame)
	aux.fillRow(takGame, 1, 1)
	ans = End.road(takGame.board)
	assert ans[0] and not ans[1]
	aux.resetBoard(takGame)
	aux.fillRow(takGame, 1, -1)
	ans = End.road(takGame.board)
	assert ans[1] and not ans[0]

@pytest.fixture(scope='module')
def takGame():
	import Tak
	return Tak.TakGame(5)
