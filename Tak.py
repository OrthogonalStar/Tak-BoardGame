import collections
import Board as boa, End, Actions as act
from copy import deepcopy
#initialize board and pies
class TakGame(object):
    def __init__(self, boardsize):
        self.board = boa.Board(boardsize)
        self.pieces, self.capstones = self.board.getPieceCount(boardsize)
        self.turnCount = 1
        self.history = []

    def logAction(self):
        self.history.append(deepcopy(self.board.board))

    def undo(self):
        if len(self.history) > 0:
            self.board.board = self.history.pop()
            self.turnCount -= 1

    def end(self):
        return End.end(self.board)

    def getEndResults(self):
        player = 2-((self.turnCount+1)%2)
        winP = End.winner(self.board, player)
        pts = End.points(self.board, player)
        return (winP, pts)

    def actPlace(self, player, loc, value):
        self.logAction()
        piece = (-1) * ((-1)**player) * value
        if self.turnCount <= 2:
            piece = piece * (-1)//abs(piece)
        act.place(self.board, loc, piece)
        self.turnCount += 1

    def checkLegalPlacement(self, loc):
        return self.board.isEmpty(loc)

    def actMove(self, start, end, dropArray):
        self.logAction()
        act.move(self.board, start, end, dropArray)
        self.turnCount += 1

    def checkLegalMoveStart(self, player, loc):
        return (player == 1 and self.board.getTop(loc) > 0) or (player == 2 and self.board.getTop(loc) < 0)

    def checkLegalDrop(self, loc, held):
        return (abs(self.board.getTop(loc)) < 2) or (held == 3 and self.board.getTop(loc) < 3)

    def checkLegalPickup(self, loc, num):
        return num <= len(self.board.getLocation(loc))

    def piecesLeft(self, player):
        piecesUsed = self.board.countTotalPieces()
        if player == 1:
            piecesLeft = self.pieces - (piecesUsed[1] + piecesUsed[2])
            capstonesLeft = self.capstones - piecesUsed[3]
        else:
            piecesLeft = self.pieces - (piecesUsed[-1] + piecesUsed[-2])
            capstonesLeft = self.capstones - piecesUsed[-3]
        return (piecesLeft, capstonesLeft)
