import pygame
import sys
from math import *
from Cell import Cell


def print_grid():
    for i in range(rows):
        for j in range(cols):
            print(grid[i][j].noAtoms, end=" ")
        print()
    print()


# Initialization of Pygame
pygame.init()

window_width = 400
window_height = 400
display = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# Colors
background = (21, 67, 96)
border = (208, 211, 212)
red = (231, 76, 60)
white = (244, 246, 247)
violet = (136, 78, 160)
yellow = (244, 208, 63)
green = (88, 214, 141)

playerColor = [red, green, violet, yellow]

font = pygame.font.SysFont("Times New Roman", 30)

cell_side = 50
noPlayers = 4

pygame.display.set_caption("Molecules %d Player" % noPlayers)

score = []
for i in range(noPlayers):
    score.append(0)

players = []
player_in = [True for _ in range(noPlayers)]
for i in range(noPlayers):
    players.append(playerColor[i])

d = cell_side // 2 - 2

cols = int(window_width // cell_side)
rows = int(window_height // cell_side)

print(cols)
print(rows)

grid = []


# Quit or Close the Game Window
def close():
    pygame.quit()
    sys.exit()


# Initializing the Grid with "Empty or 0"
def initializeGrid():
    global grid, score, players
    score = []
    for i in range(noPlayers):
        score.append(0)

    players = []
    for i in range(noPlayers):
        players.append(playerColor[i])

    grid = [[] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            grid[i].append(Cell(border))
    for i in range(rows):
        for j in range(cols):
            grid[i][j].addNeighbors(grid, rows, cols, i, j)
    print()


# Draw the Grid in Pygame Window
def drawGrid(currentIndex):
    r = 0
    c = 0
    for i in range(window_width // cell_side):
        r += cell_side
        c += cell_side
        # TODO make the border color change with the player turn
        pygame.draw.line(display, [255, 255, 255], (c, 0), (c, window_height))
        pygame.draw.line(display, [255, 255, 255], (0, r), (window_width, r))


# Draw the Present Situation of Grid
def showPresentGrid(vibrate=1):
    r = -cell_side
    c = -cell_side
    padding = 2
    for i in range(rows):
        r += cell_side
        c = -cell_side
        for j in range(cols):
            c += cell_side
            if grid[i][j].noAtoms == 0:
                grid[i][j].color = border
            elif grid[i][j].noAtoms == 1:
                pygame.draw.ellipse(display, grid[i][j].color,
                                    (c + cell_side / 2 - d / 2, r + cell_side / 2 - d / 2 + vibrate, d, d))
            elif grid[i][j].noAtoms == 2:
                pygame.draw.ellipse(display, grid[i][j].color, (c + cell_side / 2 - d / 2 - vibrate, r + 5, d, d))
                pygame.draw.ellipse(display, grid[i][j].color,
                                    (c + cell_side / 2 - d / 2, r + d / 2 + cell_side / 2 - d / 2 + vibrate, d, d))
            elif grid[i][j].noAtoms == 3:
                angle = 90
                y = r + (d / 2) * cos(radians(angle)) + cell_side / 2 - d / 2
                x = c + (d / 2) * sin(radians(angle)) + cell_side / 2 - d / 2
                pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))
                y = r + (d / 2) * cos(radians(angle + 90)) + cell_side / 2 - d / 2
                x = c + (d / 2) * sin(radians(angle + 90)) + 5
                pygame.draw.ellipse(display, grid[i][j].color, (x + vibrate, y, d, d))
                y = r + (d / 2) * cos(radians(angle - 90)) + cell_side / 2 - d / 2
                x = c + (d / 2) * sin(radians(angle - 90)) + 5
                pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))

    pygame.display.update()


# Increase the Atom when Clicked
def addAtom(i, j, color):
    grid[i][j].noAtoms += 1
    grid[i][j].color = color
    if grid[i][j].noAtoms >= len(grid[i][j].neighbors):
        overFlow(grid[i][j], color)


# Split the Atom when it Increases the "LIMIT"
def overFlow(cell, color):
    showPresentGrid()
    cell.noAtoms = 0
    for m in range(len(cell.neighbors)):
        cell.neighbors[m].noAtoms += 1
        cell.neighbors[m].color = color
        if cell.neighbors[m].noAtoms >= len(cell.neighbors[m].neighbors):
            overFlow(cell.neighbors[m], color)


# Checking if Any Player has WON!
def isPlayerInGame():
    global score
    playerScore = [0 for _ in range(noPlayers)]
    for i in range(rows):
        for j in range(cols):
            for k in range(noPlayers):
                if grid[i][j].color == players[k]:
                    playerScore[k] += grid[i][j].noAtoms
    for i, score in enumerate(playerScore):
        if score == 0:
            player_in[i] = False
    score = playerScore[:]


# GAME OVER
def gameOver(playerIndex):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()

        text = font.render("Player %d Won!" % (playerIndex + 1), True, white)
        text2 = font.render("Press \'r\' to Reset!", True, white)

        display.blit(text, (window_width / 3, window_height / 3))
        display.blit(text2, (window_width / 3, window_height / 2))

        pygame.display.update()
        clock.tick(60)


def checkWon():
    num = 0
    for i in range(noPlayers):
        if score[i] == 0:
            num += 1
    if num == noPlayers - 1:
        for i in range(noPlayers):
            if score[i]:
                return i

    return 9999


# Main Loop
def gameLoop():
    initializeGrid()
    loop = True

    turns = 0

    currentPlayer = 0

    vibrate = .5

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = int(y / cell_side)
                j = int(x / cell_side)
                if grid[i][j].color == players[currentPlayer] or grid[i][j].color == border:
                    turns += 1
                    temp_currentPlayer = currentPlayer
                    for _ in range(noPlayers):
                        if player_in[(_ + temp_currentPlayer) % noPlayers]:
                            break
                        currentPlayer = (currentPlayer + 1) % noPlayers
                    addAtom(i, j, players[currentPlayer])
                    currentPlayer = (currentPlayer + 1) % noPlayers
                if turns >= noPlayers:
                    isPlayerInGame()
                print(player_in)
                print(currentPlayer)

        display.fill(background)
        # Vibrate the Atoms in their Cells
        vibrate *= -1

        drawGrid(currentPlayer)
        showPresentGrid(int(vibrate))

        pygame.display.update()

        res = checkWon()
        if res < 9999:
            gameOver(res)

        clock.tick(20)


gameLoop()
