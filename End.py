import collections

def isFull(board):
    for row in board.board:
        for col in row:
            if col[-1] == 0:
                return False
    return True

def outOfPieces(board):
    pC = board.countTotalPieces()
    return (pC[1] + pC[2] == board.pieces and pC[3] == board.capstones) or (pC[-1] + pC[-2] == board.pieces and pC[-3] == board.capstones)

def end(board):
    en = False
    if outOfPieces(board):
        en = True
    elif isFull(board):
        en = True
    elif road(board)[0] or road(board)[1]:
        en = True
    return en

def isRoadPiece(board, loc, player):
    mod = -1*((-1)**player)
    return board.getTop(loc) == 1*mod or board.getTop(loc) == 3*mod

def isGoal(board, start, loc):
    return (start[0] == 0 and loc[0] == board.size-1) or (start[1] == 0 and loc[1] == board.size-1)

def checkRow(board, start, player):
    return isRoadPiece(board, [start, 0], player) and roadSearch(board, [start, 0], player)

def checkCol(board, start, player):
    return isRoadPiece(board, [0, start], player) and roadSearch(board, [0, start], player)

def roadSearch(board, start, player):
    visited = [[False for i in range(board.size)] for j in range(board.size)]
    locations = [start]
    visited[start[0]][start[1]] = True
    while len(locations) > 0:
        check = locations.pop(-1)
        adj = board.adjacent(check)
        for loc in adj:
            if not visited[loc[0]][loc[1]] and isGoal(board, start, loc) and isRoadPiece(board, loc, player):
                return True
            elif not visited[loc[0]][loc[1]] and isRoadPiece(board, loc, player):
                locations.append(loc)
                visited[loc[0]][loc[1]] = True
    return False

def road(board):
    p1road, p2road = False, False
    for i in range(board.size):
        if checkRow(board, i, 1) or checkCol(board, i, 1):
            p1road = True
        elif checkRow(board, i, 2) or checkCol(board, i, 2):
            p2road = True
    return p1road, p2road

def points(board, player):
    win = player
    piecesLeft = board.capstones + board.pieces
    if win == 1:
        piecesLeft = piecesLeft - (board.countTotalPieces()[1] + board.countTotalPieces()[3])
    else:
        piecesLeft = piecesLeft - (board.countTotalPieces()[-1] + board.countTotalPieces()[-3])
    return (board.size**2) + piecesLeft

def winRoad(board, player=1):
    rd = road(board)
    if rd[0] and rd[1]:
        return player
    elif rd[0] == True:
        return 1
    elif rd[1] == True:
        return 2
    return False

def flatStones(board, player):
    flatCount = 0
    for i in range(board.size):
        for j in range(board.size):
            if isRoadPiece(board, [i,j], player):
                flatCount += 1
    return flatCount

def winFlat(board):
    if flatStones(board, 1) > flatStones(board, 2):
        return 1
    else:
        return 2

def winner(board, player=1):
    if winRoad(board, player):
        return winRoad(board, player)
    else:
        return winFlat(board)
