import queue
from queue import Queue

import pygame
import sys
from math import *
from Grid import Grid
from Player import Player
import copy

# Initialization of Pygame
pygame.init()

grid_window_width = 400
grid_window_height = 400

cell_side = 100

window_width = grid_window_width + 100
window_height = grid_window_height + 200

padding_v = 50
padding_h = 50

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

players = [Player([255, 0, 0], "LynX"), Player([0, 0, 255], "Prometheus")]
noPlayers = len(players)
for i in range(noPlayers):
    if i < noPlayers - 1:
        players[i].next_player = players[i + 1].id
    else:
        players[i].next_player = players[0].id
for i in range(noPlayers - 1, -1, -1):
    if i > 0:
        players[i].prev_player = players[i - 1].id
    else:
        players[i].prev_player = players[noPlayers - 1].id
print(players)

players_playing = set()
for player in players:
    players_playing.add(player)

font = pygame.font.SysFont("Times New Roman", 30)

pygame.display.set_caption("Molecules %d Player" % noPlayers)

score = []
for i in range(noPlayers):
    score.append(0)

d = cell_side // 2 - 2

cols = int(grid_window_width // cell_side)
rows = int(grid_window_height // cell_side)


# Quit or Close the Game Window
def close():
    pygame.quit()
    sys.exit()


# Initializing the Grid with "Empty or 0"
def initializeGrid():
    global grid, score, players
    score = [0 for _ in range(noPlayers)]
    grid = Grid(rows, cols)
    print(grid)


# Draw the Grid in Pygame Window
def drawGrid(currentIndex):
    r = 0
    c = 0
    for i in range(grid_window_width // cell_side + 1):
        pygame.draw.line(display, players[currentIndex].color, (padding_h + c, padding_v + 0),
                         (padding_h + c, padding_v + grid_window_height))
        c += cell_side

    for i in range(grid_window_height // cell_side + 1):
        pygame.draw.line(display, players[currentIndex].color, (padding_h + 0, padding_v + r),
                         (padding_h + grid_window_width, padding_v + r))
        r += cell_side

    player_indicator_height = min(grid_window_height, 50)
    player_indicator_width = min(grid_window_width, 300)
    pygame.draw.rect(display, players[currentIndex].color,
                     (padding_h + (grid_window_width - player_indicator_width) / 2, padding_v * 2 + grid_window_height,
                      player_indicator_width, player_indicator_height))

    text = font.render(f"{players[currentIndex].name}'s turn", True, [0, 0, 0])
    textRect = text.get_rect()
    textRect.center = (window_width // 2, padding_v * 2 + grid_window_height + player_indicator_height // 2)
    display.blit(text, textRect)


# Draw the Present Situation of Grid
def showPresentGrid(grid):
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
                                    (padding_h + c + cell_side / 2 - d / 2,
                                     padding_v + r + cell_side / 2 - d / 2 + grid.matrix[i][j].vibrate(), d, d))
            elif grid.matrix[i][j].noAtoms == 2:
                pygame.draw.ellipse(display, grid.matrix[i][j].color,
                                    (padding_h + c + cell_side / 2 - d / 2 - grid.matrix[i][j].vibrate(),
                                     padding_v + r + 5, d, d))
                pygame.draw.ellipse(display, grid.matrix[i][j].color,
                                    (padding_h + c + cell_side / 2 - d / 2,
                                     padding_v + r + d / 2 + cell_side / 2 - d / 2 + grid.matrix[i][j].vibrate(), d, d))
            elif grid.matrix[i][j].noAtoms == 3:
                angle = 90
                y = padding_v + r + (d / 2) * cos(radians(angle)) + cell_side / 2 - d / 2
                x = padding_h + c + (d / 2) * sin(radians(angle)) + cell_side / 2 - d / 2
                pygame.draw.ellipse(display, grid.matrix[i][j].color, (x - grid.matrix[i][j].vibrate(), y, d, d))
                y = padding_v + r + (d / 2) * cos(radians(angle + 90)) + cell_side / 2 - d / 2
                x = padding_h + c + (d / 2) * sin(radians(angle + 90)) + 5
                pygame.draw.ellipse(display, grid.matrix[i][j].color, (x + grid.matrix[i][j].vibrate(), y, d, d))
                y = padding_v + r + (d / 2) * cos(radians(angle - 90)) + cell_side / 2 - d / 2
                x = padding_h + c + (d / 2) * sin(radians(angle - 90)) + 5
                pygame.draw.ellipse(display, grid.matrix[i][j].color, (x - grid.matrix[i][j].vibrate(), y, d, d))

    pygame.display.update()


# Increase the Atom when Clicked
def addAtom(i, j, player):
    global grid_cpy
    grid_cpy = copy.deepcopy(grid)
    grid.matrix[i][j].add_atoms()
    grid.matrix[i][j].color = player.color

    if grid.matrix[i][j].noAtoms >= len(grid.matrix[i][j].neighbors):
        overFlow_manager(grid.matrix[i][j], player)
    showPresentGrid(grid)


def overFlow_manager(cell, player):
    all_cells = set()
    q = queue.Queue()
    q.put(cell)
    all_cells.add(cell)
    while not q.empty():
        if len(all_cells) == rows * cols:
            break
        c = q.get()
        all_cells.remove(c)
        cells = overFlow(c, player)
        if len(cells) > 0:
            for c in cells:
                q.put(c)
                all_cells.add(c)


# Split the Atom when it Increases the "LIMIT"
def overFlow(cell, player):
    cells = []
    cell.noAtoms = 0
    for cell_neighbor in cell.neighbors:
        cell_neighbor.add_atoms()
        cell_neighbor.color = player.color
        if cell_neighbor.noAtoms >= len(cell_neighbor.neighbors):
            cells.append(cell_neighbor)

    return cells


# Checking if Any Player has WON!
def isPlayerInGame():
    print('remove')
    global score
    playerScore = [0 for p in players]
    for row in range(rows):
        for col in range(cols):
            for k in range(noPlayers):
                if grid.matrix[row][col].color == players[k].color:
                    # playerScore[k] += grid.matrix[row][col].noAtoms
                    playerScore[k] += 1
    for i, score in enumerate(playerScore):
        if score == 0 and players[i] in players_playing:
            players_playing.remove(players[i])
            if players[players[i].next_player] in players_playing:
                players[players[i].prev_player].next_player = players[i].next_player
            if players[players[i].prev_player] in players_playing:
                players[players[i].next_player].prev_player = players[i].prev_player
    print(players)
    print(players_playing)

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

        text = font.render(f"{players[playerIndex].name} Won!", True, white)
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
                if x < padding_h or y < padding_v or x > padding_h + grid_window_width or \
                        y > padding_v + grid_window_height:
                    break
                x_grid = x - padding_h
                y_grid = y - padding_v

                i = int(y_grid / cell_side)
                j = int(x_grid / cell_side)

                print(f'x: {x}, y: {y}')
                print(f'x`: {x_grid}, y`: {y_grid}')

                print(f'grid  :{grid.matrix[i][j].color}')
                print(f'player:{players[currentPlayer].color}')

                if grid.matrix[i][j].color == players[currentPlayer].color or grid.matrix[i][j].color == border:

                    turns += 1

                    addAtom(i, j, players[currentPlayer])
                    if turns >= noPlayers:
                        isPlayerInGame()
                    currentPlayer = players[currentPlayer].next_player

                print(f'cp: {currentPlayer}')

        display.fill(background)

        drawGrid(currentPlayer)
        showPresentGrid(grid)

        pygame.display.update()

        res = checkWon()
        if res < 9999:
            gameOver(res)

        clock.tick(20)


gameLoop()
