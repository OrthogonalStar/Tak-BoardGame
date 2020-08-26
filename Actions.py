def piecesLeft(board, val):
    used = board.countTotalPieces()
    if val > 0:
        if val > 2 and used[3] >= board.capstones:
            return False
        elif used[1] + used[2] >= board.pieces:
            return False
    else:
        if abs(val) > 2 and used[-3] >= board.capstones:
            return False
        elif used[-1] + used[-2] >= board.pieces:
            return False
    return True

def place(board, loc, type):
    if not piecesLeft(board, type):
        raise ValueError('No more of those pieces left')
    elif abs(type) > 3 or type == 0:
        raise ValueError('Not a valid piece')
    elif board.isEmpty(loc):
        board.getLocation(loc)[-1] = type
    else:
        raise ValueError('This location has pieces you cant place here')

def getPieces(board, loc, num):
    hand = []
    for i in range(num):
        hand.append(board.getLocation(loc).pop())
        if board.countStack(loc) == 0:
            board.getLocation(loc).append(0)
    return hand

def pickup(board, start, dropArray):
    number = sum(dropArray)
    if number <= board.countStack(start):
        return getPieces(board, start, number)
    else:
        raise ValueError("You can't pick up more pieces than are in the space")

def getDirection(start, end):
    if start[0] == end[0]:
        return 0, (end[1] - start[1])//abs(end[1] - start[1])
    elif start[1] == end[1]:
        return (end[0] - start[0])//abs(end[0] - start[0]), 0
    else:
        raise ValueError("Must move in a straight line")

def dropPieces(board, loc, num, hand):
    for i in range(num):
        if board.isEmpty(loc):
            place(board, loc, hand.pop())
        elif abs(board.getTop(loc)) == 1:
            board.getLocation(loc).append(hand.pop())
        elif abs(board.getTop(loc)) == 2 and abs(hand[-1]) == 3:
            board.getLocation(loc)[-1] = board.getTop(loc)/2
            board.getLocation(loc).append(hand.pop())
        else:
            raise ValueError("This piece can't be placed on that piece")

def checkCarry(board, num):
    if num <= board.size:
        return None
    else:
        raise ValueError("You can't pick up that may pieces at once")

def move(board, start, end, dropArray):
    checkCarry(board, sum(dropArray))
    hand = pickup(board, start, dropArray)
    xdir, ydir = getDirection(start, end)
    current = start.copy()
    for element in dropArray:
        current = [current[0] + xdir, current[1] + ydir]
        dropPieces(board, current, element, hand)
