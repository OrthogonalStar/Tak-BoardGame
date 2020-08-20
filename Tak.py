import collections, Board as boa, End, Actions
#initialize board and pies
class TakGame(object):
    def __init__(self, boardsize):
        self.board = boa.Board(boardsize)
        self.pieces, self.capstones = self.getPieceCount(boardsize)
        self.turnCount = 1

    def getPieceCount(self, size):
        if size == 8:
            cap, pie = 2, 50
        elif size == 7:
            cap, pie = 2, 40
        elif size == 6:
            cap, pie = 1, 30
        elif size == 5:
            cap, pie = 1, 21
        elif size == 4:
            cap, pie = 0, 15
        else:
            cap, pie = 0, 10
        return (pie, cap)

    #control flow for a turn
    def turn(self):
        inp = ('Place(p) or move(m)')

        return True
