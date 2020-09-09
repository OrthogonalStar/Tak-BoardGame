import pygame, os, sys, itertools
import Tak

#display setup
pygame.init()
#basic settings to use
resolution = (800, 1000)
width, height = 800, 800
colors = {'white':(255, 255, 255), 'black':(0, 0, 0), 'lightBrown':(251, 196, 117), 'darkBrown':(139, 69, 0),
            'lightGrey':(150, 150, 150), 'darkGrey':(100, 100, 100)}
win = pygame.display.set_mode(resolution)
pygame.display.set_caption("Tak")
font = pygame.font.SysFont('Arial', 18)
background = pygame.Surface(resolution)
background.fill(colors['black'])
pieceImages = {'lightflat':pygame.image.load('2D pieces/flat-light.png'), 'lightwall':pygame.image.load('2D pieces/wall-light.png'),
                'lightcapstone':pygame.image.load('2D pieces/capstone-light.png'), 'darkflat':pygame.image.load('2D pieces/flat-dark.png'),
                'darkwall':pygame.image.load('2D pieces/wall-dark.png'), 'darkcapstone':pygame.image.load('2D pieces/capstone-dark.png'),}

#board and button classes
class board(object):
    def __init__(self, size):
        self.width, self.height = 800, 800
        self.size = size
        self.squareSize = self.width/size
        self.bd = pygame.Surface((self.width, self.height))
        self.squareCentres = []
        self.color = [colors['lightBrown'], colors['darkBrown']]
        self.index = 1
        for row in range(size):
            for column in range(size):
                Square = (row*self.squareSize, column*self.squareSize, self.squareSize, self.squareSize)
                if Square not in self.squareCentres:
                    self.squareCentres.append(Square)
                pygame.draw.rect(self.bd, self.color[self.index], Square)
                if not (size%2 == 0 and column == size-1):
                    self.index = (self.index+1)%2

    def checkSquare(self, coordinate):
        for i in range(len(self.squareCentres)):
            square = self.squareCentres[i]
            if square[0] < coordinate[0] < square[0] + square[2] and square[1] < coordinate[1] < square[1] + square[3]:
                return [i//self.size, i%self.size]

class button(object):
    def __init__(self, x, y, text, width = 110, height = 40):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.disp = renderStandard(text)

#move has to be built in multiple steps and needs the object to hold and output the data in the correct
#format for the move command in game
class buildMove(object):
    def __init__(self, start):
        self.start = start
        self.dropLocations = []
        self.hand = 0
        self.current = start
        self.direction = None

    def pickup(self, loc):
        if self.same(self.start, loc) and game.checkLegalPickup(loc, self.hand+1):
            self.hand += 1

    def next(self, loc):
        return loc[0] == self.current[0] + self.direction[0] and loc[1] == self.current[1] + self.direction[1]

    def same(self, loc1, loc2):
        return loc1[0] == loc2[0] and loc1[1] == loc2[1]

    def drop(self, loc):
        if game.board.isAdjacent(loc, self.start) and self.direction is None and game.checkLegalDrop(loc, game.board.getLocation(self.start)[-self.hand]):
            self.direction = [loc[0]-self.start[0], loc[1] - self.start[1]]
            self.dropLocations.append(loc)
            self.hand -= 1
            self.current = loc

        elif self.direction is not None and (self.same(self.current, loc) or self.next(loc)) and self.hand > 0 and game.checkLegalDrop(loc, game.board.getLocation(self.start)[-self.hand]):
            self.dropLocations.append(loc)
            self.hand -= 1
            self.current = loc

    def dropArray(self):
        array = []
        count = 0
        current = self.dropLocations[0]
        for location in self.dropLocations:
            if self.same(current, location):
                count += 1
            else:
                array.append(count)
                count = 1
                current = location
        array.append(count)
        return array

    def getEnd(self):
        return self.dropLocations[-1]

#get correct image to draw onto the board for each piece
def selectPieceImage(value):
    key = ''
    if value > 0:
        key += 'light'
    else:
        key += 'dark'
    if abs(value) == 3:
        key += 'capstone'
    elif abs(value) == 2:
        key += 'wall'
    else:
        key += 'flat'
    return pieceImages[key]

#render the board as a printable set to show pieces
def renderPieces(game, board):
    for i in range(game.board.size):
        for j in range(game.board.size):
            pieceStack = game.board.getLocation([i, j])
            boardSquare = board.squareCentres[i*board.size+j]
            coordinate = boardSquare[:2]
            for x in range(len(pieceStack)):
                if pieceStack[x] is not 0:
                    if abs(pieceStack[x]) == 2:
                        image = pygame.transform.scale(selectPieceImage(pieceStack[x]), (int(board.squareSize*0.2), int(board.squareSize*0.6)))
                    else:
                        image = pygame.transform.scale(selectPieceImage(pieceStack[x]), (int(board.squareSize*0.6), int(board.squareSize*0.6)))
                    win.blit(image, (coordinate[0]+int(board.squareSize*(0.05*(x+1))), coordinate[1]+int(board.squareSize*(0.05*(x+1)))))

#check to see what button has been pressed
def checkButtons(coordinate):
    for butt in buttons:
        if butt.x < coordinate[0] < butt.x + butt.width and butt.y < coordinate[1] < butt.y + butt.height:
            return butt.text

#render standard font
def renderStandard(text):
    return font.render(text, True, colors['white'])

#display game results
def displayResults():
    results = game.getEndResults()
    block = pygame.Surface((250, 160))
    block.fill(colors['white'])
    winText = pygame.font.SysFont('Arial', 40).render('Winner!', True, colors['black'])
    winnerText = pygame.font.SysFont('Arial', 30).render('Player ' + str(results[0]), True, colors['black'])
    pointText = font.render('Points scored: ' + str(results[1]), True, colors['black'])
    win.blit(block, (275, 300))
    win.blit(winText, (320, 310))
    win.blit(winnerText, (335, 370))
    win.blit(pointText, (320, 430))

#display current action
def displayAction():
    actionText = [renderStandard("Current Action:")]
    if move is not None:
        actionText.append(renderStandard('Moving'))
        actionText.append(renderStandard('Holding ' + str(move.hand) + ' from ' + str(move.start)))
        if move.direction is not None:
            actionText.append(renderStandard('Dropping'))
            dropArray = move.dropArray()
            direction = move.direction
            for i in range(len(dropArray)):
                location = move.start[0] + i*direction[0], move.start[1] + i*direction[1]
                actionText.append(renderStandard(str(dropArray[i]) + ' at ' + str(location)))
    elif type is not 0:
        actionText.append(renderStandard('Placing'))
        if type is 1:
            actionText.append(renderStandard('Flat stone'))
        elif type is 2:
            actionText.append(renderStandard('Wall'))
        elif type is 3:
            actionText.append(renderStandard('Capstone'))
    else:
        actionText.append(renderStandard('No current action'))
    start = (270, 820)
    for i in range(len(actionText)):
        win.blit(actionText[i], (start[0], start[1] + i*20))

#initialize components
table = board(5)
game = Tak.TakGame(5)
pastGames = []

turnLabel = renderStandard('Current Turn: ')
playerLabel = renderStandard('Current Player: ')
sizeLabel = renderStandard('Select game size (will reset game):')
piecesLabel = renderStandard('Pieces left:')
capstonesLabel = renderStandard('Capstones left:')

flatButton = button(20, 820, 'Flat')
wallButton = button(20, 880, 'Wall')
capButton = button(20, 940, 'Capstone')
moveButton = button(150, 820, 'Move')
cancelButton = button(150, 880, 'Cancel')
undoButton = button(150, 940, 'Undo')
threeButton = button(500, 940, '3', 40, 40)
fourButton = button(560, 940, '4', 40, 40)
fiveButton = button(620, 940, '5', 40, 40)
sixButton = button(680, 940, '6', 40, 40)
eightButton = button(740, 940, '8', 40, 40)

buttons = [flatButton, wallButton, capButton, moveButton, undoButton, cancelButton, threeButton, fourButton,
            fiveButton, sixButton, eightButton]

#game loop and initilize game specific settings
fps = 60
clock = pygame.time.Clock()
run = True
type = 0
location = None
buildingMove = False
move = None
player = 1

while run:
    clock.tick(fps)
    player = 2-(game.turnCount%2)
    #draw out all the features
    win.blit(background, (0,0))
    win.blit(table.bd, table.bd.get_rect())
    win.blit(turnLabel, (480, 820))
    win.blit(renderStandard(str(game.turnCount)), (600, 820))
    win.blit(playerLabel, (640, 820))
    win.blit(renderStandard(str(player)), (780, 820))
    win.blit(piecesLabel, (480, 860))
    win.blit(renderStandard(str(game.piecesLeft(player)[0])), (580, 860))
    win.blit(capstonesLabel, (640, 860))
    win.blit(renderStandard(str(game.piecesLeft(player)[1])), (780, 860))
    win.blit(sizeLabel, (480, 900))
    renderPieces(game, table)

    #actions on events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            selection = checkButtons(mouse)
            location = table.checkSquare(mouse)
            if selection == 'Flat':
                type = 1
            elif selection == 'Wall' and game.turnCount > 2:
                type = 2
            elif selection == 'Capstone' and game.turnCount > 2:
                type = 3
            elif selection == 'Cancel':
                if move is None:
                    type = 0
                else:
                    move = None
                    buildingMove = False
            elif selection == 'Undo':
                if game.turnCount > 1:
                    game.undo()
                elif len(pastGames) > 0:
                    last = pastGames.pop()
                    game = last[0]
                    table = last[1]
            elif selection == 'Move':
                buildingMove = True
            elif selection is not None and selection.isdigit():
                pastGames.append((game, table))
                game = Tak.TakGame(int(selection))
                table = board(int(selection))
            elif type is not 0 and location is not None and game.checkLegalPlacement(location):
                game.actPlace(player, location, type)
                location = None
                type = 0
            elif move is not None and buildingMove:
                if move.same(move.start, location):
                    move.pickup(location)
                elif move.hand > 0:
                    move.drop(location)
                else:
                    game.actMove(move.start, move.getEnd(), move.dropArray())
                    move = None
                    buildingMove = False
            elif buildingMove and location is not None and game.checkLegalMoveStart(player, location):
                move = buildMove(location)
                move.pickup(location)

    #track if we are hovering over buttons and draw them in the correct color
    mouse = pygame.mouse.get_pos()
    for butt in buttons:
        if butt.x < mouse[0] < butt.x + butt.width and butt.y < mouse[1] < butt.y + butt.height:
            pygame.draw.rect(win, colors['lightGrey'], [butt.x, butt.y, butt.width, butt.height])
        else:
            pygame.draw.rect(win, colors['darkGrey'], [butt.x, butt.y, butt.width, butt.height])
        win.blit(butt.disp, (butt.x + 10, butt.y + (butt.height/4)))
    if game.end():
        displayResults()
    displayAction()
    pygame.display.update()

pygame.quit()
sys.exit()
