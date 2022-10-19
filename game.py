import pygame
import sys
from math import *
from Grid import Grid


# Initialization of Pygame
pygame.init()

window_width = 400
window_height = 400
display = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# Colors
background = (0, 0, 0)
border = (208, 211, 212)
red = (255, 0, 0)
white = (255, 255, 255)
violet = (0, 0, 255)
yellow = (255, 255, 255)
green = (0, 255, 0)

playerColor = [red, green, violet, yellow]

font = pygame.font.SysFont("Times New Roman", 30)

cell_side = 50
noPlayers = 4

pygame.display.set_caption("Molecules %d Player" % noPlayers)

score = []
for i in range(noPlayers):
    score.append(0)

players = []
players_playing = set()

for i in range(noPlayers):
    players_playing.add(i)

for i in range(noPlayers):
    players.append(playerColor[i])

d = cell_side // 2 - 2

cols = int(window_width // cell_side)
rows = int(window_height // cell_side)


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

    grid = Grid(rows, cols)
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
def showPresentGrid():
    r = -cell_side
    c = -cell_side
    padding = 2
    for i in range(rows):
        r += cell_side
        c = -cell_side
        for j in range(cols):
            c += cell_side
            if grid.matrix[i][j].noAtoms == 0:
                grid.matrix[i][j].color = border
            elif grid.matrix[i][j].noAtoms == 1:
                pygame.draw.ellipse(display, grid.matrix[i][j].color,
                                    (c + cell_side / 2 - d / 2, r + cell_side / 2 - d / 2 + grid.matrix[i][j].vibrate(), d, d))
            elif grid.matrix[i][j].noAtoms == 2:
                pygame.draw.ellipse(display, grid.matrix[i][j].color, (c + cell_side / 2 - d / 2 - grid.matrix[i][j].vibrate(), r + 5, d, d))
                pygame.draw.ellipse(display, grid.matrix[i][j].color,
                                    (c + cell_side / 2 - d / 2, r + d / 2 + cell_side / 2 - d / 2 + grid.matrix[i][j].vibrate(), d, d))
            elif grid.matrix[i][j].noAtoms == 3:
                angle = 90
                y = r + (d / 2) * cos(radians(angle)) + cell_side / 2 - d / 2
                x = c + (d / 2) * sin(radians(angle)) + cell_side / 2 - d / 2
                pygame.draw.ellipse(display, grid.matrix[i][j].color, (x - grid.matrix[i][j].vibrate(), y, d, d))
                y = r + (d / 2) * cos(radians(angle + 90)) + cell_side / 2 - d / 2
                x = c + (d / 2) * sin(radians(angle + 90)) + 5
                pygame.draw.ellipse(display, grid.matrix[i][j].color, (x + grid.matrix[i][j].vibrate(), y, d, d))
                y = r + (d / 2) * cos(radians(angle - 90)) + cell_side / 2 - d / 2
                x = c + (d / 2) * sin(radians(angle - 90)) + 5
                pygame.draw.ellipse(display, grid.matrix[i][j].color, (x - grid.matrix[i][j].vibrate(), y, d, d))

    pygame.display.update()


# Increase the Atom when Clicked
def addAtom(i, j, color):
    grid.matrix[i][j].noAtoms += 1
    grid.matrix[i][j].color = color
    if grid.matrix[i][j].noAtoms >= len(grid.matrix[i][j].neighbors):
        overFlow(grid.matrix[i][j], color)


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
    print('remove')
    global score
    playerScore = [0 for _ in range(noPlayers)]
    for i in range(rows):
        for j in range(cols):
            for k in range(noPlayers):
                if grid.matrix[i][j].color == players[k]:
                    # playerScore[k] += grid.matrix[i][j].noAtoms
                    playerScore[k] += 1
    for i, score in enumerate(playerScore):
        if score == 0 and i in players_playing:
            players_playing.remove(i)
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

                print(f'grid  :{grid.matrix[i][j].color}')
                print(f'player:{players[currentPlayer]}')

                if grid.matrix[i][j].color == players[currentPlayer] or grid.matrix[i][j].color == border:

                    turns += 1

                    addAtom(i, j, players[currentPlayer])
                    if turns >= noPlayers:
                        isPlayerInGame()
                    print(players_playing)
                    flag = False
                    for i, player in enumerate(players_playing):
                        print(player)
                        if player == currentPlayer:
                            flag = True
                            if i == len(players_playing) - 1:
                                currentPlayer = 0
                        elif flag:
                            currentPlayer = player
                            break

                # print('remove')

        display.fill(background)

        drawGrid(currentPlayer)
        showPresentGrid()

        pygame.display.update()

        res = checkWon()
        if res < 9999:
            gameOver(res)

        clock.tick(20)


gameLoop()
