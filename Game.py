import queue

import pygame
from pygame.locals import *

import sys
from math import *

from Grid import Grid
from Player import Player


class Game:

    def __init__(self):

        self.grid_window_width = 600
        self.grid_window_height = 400

        self.cell_side = 100

        self.padding_v = 50
        self.padding_h = 50

        self.player_name_space = 100
        self.pause_button_space = 0
        self.window_width = self.grid_window_width + 100
        self.window_height = self.grid_window_height + self.player_name_space + self.pause_button_space + 3 * self.padding_v

        self.grid = None
        self.score = None

        # Colors
        self.background = (0, 0, 0)
        self.border = (208, 211, 212)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.violet = (0, 0, 255)
        self.yellow = (255, 255, 255)
        self.green = (0, 255, 0)

        self.players = [Player([255, 0, 0], "LynX"), Player([0, 0, 255], "Prometheus")]

        self.no_Players = len(self.players)

        self.players_playing = set()
        for player in self.players:
            self.players_playing.add(player)

        score = []
        for i in range(self.no_Players):
            score.append(0)

        self.d = self.cell_side // 2 - 2

        self.cols = int(self.grid_window_width // self.cell_side)
        self.rows = int(self.grid_window_height // self.cell_side)

        pygame.init()
        pygame.display.set_caption("Molecules %d Player" % self.no_Players)
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), 0, 32)
        self.mainClock = pygame.time.Clock()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        self.font = pygame.font.SysFont("Times New Roman", 30)
        self.font2 = pygame.font.SysFont("Comic Sans MS", 30)

    # Quit or Close the Game Window
    def close(self):
        pygame.quit()
        sys.exit()

    # Initializing the Grid with "Empty or 0"
    def initializeGrid(self):

        for i in range(self.no_Players):
            if i < self.no_Players - 1:
                self.players[i].next_player = self.players[i + 1].id
            else:
                self.players[i].next_player = self.players[0].id
        for i in range(self.no_Players - 1, -1, -1):
            if i > 0:
                self.players[i].prev_player = self.players[i - 1].id
            else:
                self.players[i].prev_player = self.players[self.no_Players - 1].id

        self.score = [0 for _ in range(self.no_Players)]
        self.grid = Grid(self.rows, self.cols)

    # Draw the Grid in Pygame Window
    def drawGrid(self, currentIndex):
        r = 0
        c = 0
        for i in range(self.grid_window_width // self.cell_side + 1):
            pygame.draw.line(self.display, self.players[currentIndex].color,
                             (self.padding_h + c, self.pause_button_space + 2 * self.padding_v + 0),
                             (self.padding_h + c,
                              2 * self.padding_v + self.pause_button_space + self.grid_window_height))
            c += self.cell_side

        for i in range(self.grid_window_height // self.cell_side + 1):
            pygame.draw.line(self.display, self.players[currentIndex].color,
                             (self.padding_h + 0, 2 * self.padding_v + self.pause_button_space + r),
                             (
                                 self.padding_h + self.grid_window_width,
                                 2 * self.padding_v + self.pause_button_space + r))
            r += self.cell_side

        player_indicator_height = min(self.grid_window_height, 50)
        player_indicator_width = min(self.grid_window_width, 300)
        pygame.draw.rect(self.display, self.players[currentIndex].color,
                         (self.padding_h + (self.grid_window_width - player_indicator_width) / 2,
                          self.pause_button_space + self.padding_v * 3 + self.grid_window_height,
                          player_indicator_width, player_indicator_height))

        self.button_pause = pygame.Rect(0, 0, self.pause_button_space, self.pause_button_space)
        self.button_pause.x = self.window_width - self.padding_h - self.pause_button_space
        self.button_pause.y = self.padding_v
        pygame.draw.rect(self.screen, self.players[currentIndex].color, self.button_pause)

        pause_len = 2
        pause1 = pygame.Rect(0, 0, self.pause_button_space // 5 - pause_len, self.pause_button_space // 2)
        pause1.x = self.window_width - self.padding_h - self.pause_button_space + self.pause_button_space // 5 + pause_len + 2
        pause1.y = self.padding_v + self.pause_button_space // 4
        pygame.draw.rect(self.screen, [0, 0, 0], pause1)

        pause2 = pygame.Rect(0, 0, self.pause_button_space // 5 - pause_len, self.pause_button_space // 2)
        pause2.x = self.window_width - self.padding_h - self.pause_button_space + 3 * self.pause_button_space // 5 + pause_len - 2
        pause2.y = self.padding_v + self.pause_button_space // 4
        pygame.draw.rect(self.screen, [0, 0, 0], pause2)

        text = self.font.render(f"{self.players[currentIndex].name}'s turn", True, [0, 0, 0])
        text_rect = text.get_rect()
        text_rect.center = (self.window_width // 2,
                            self.pause_button_space + self.padding_v * 3 + self.grid_window_height + player_indicator_height // 2)
        self.display.blit(text, text_rect)

    # Draw the Present Situation of Grid
    def showPresentGrid(self):
        r = -self.cell_side
        c = -self.cell_side
        padding = 2
        for i in range(self.rows):
            r += self.cell_side
            c = -self.cell_side
            for j in range(self.cols):
                c += self.cell_side
                if self.grid.matrix[i][j].noAtoms == 0:
                    self.grid.matrix[i][j].color = self.border
                elif self.grid.matrix[i][j].noAtoms == 1:
                    pygame.draw.ellipse(self.display, self.grid.matrix[i][j].color,
                                        (self.padding_h + c + self.cell_side / 2 - self.d / 2,
                                         self.pause_button_space + 2 * self.padding_v + r + self.cell_side / 2 - self.d / 2 +
                                         self.grid.matrix[i][j].vibrate(), self.d, self.d))
                elif self.grid.matrix[i][j].noAtoms == 2:
                    pygame.draw.ellipse(self.display, self.grid.matrix[i][j].color,
                                        (self.padding_h + c + self.cell_side / 2 - self.d / 2 - self.grid.matrix[i][
                                            j].vibrate(),
                                         self.pause_button_space + 2 * self.padding_v + r + 5, self.d, self.d))
                    pygame.draw.ellipse(self.display, self.grid.matrix[i][j].color,
                                        (self.padding_h + c + self.cell_side / 2 - self.d / 2,
                                         self.pause_button_space + 2 * self.padding_v + r + self.d / 2 + self.cell_side / 2 - self.d / 2 +
                                         self.grid.matrix[i][j].vibrate(), self.d, self.d))
                elif self.grid.matrix[i][j].noAtoms == 3:
                    angle = 90
                    y = self.pause_button_space + 2 * self.padding_v + r + (self.d / 2) * cos(
                        radians(angle)) + self.cell_side / 2 - self.d / 2
                    x = self.padding_h + c + (self.d / 2) * sin(radians(angle)) + self.cell_side / 2 - self.d / 2
                    pygame.draw.ellipse(self.display, self.grid.matrix[i][j].color,
                                        (x - self.grid.matrix[i][j].vibrate(), y, self.d, self.d))
                    y = self.pause_button_space + 2 * self.padding_v + r + (self.d / 2) * cos(
                        radians(angle + 90)) + self.cell_side / 2 - self.d / 2
                    x = self.padding_h + c + (self.d / 2) * sin(radians(angle + 90)) + 5
                    pygame.draw.ellipse(self.display, self.grid.matrix[i][j].color,
                                        (x + self.grid.matrix[i][j].vibrate(), y, self.d, self.d))
                    y = self.pause_button_space + 2 * self.padding_v + r + (self.d / 2) * cos(
                        radians(angle - 90)) + self.cell_side / 2 - self.d / 2
                    x = self.padding_h + c + (self.d / 2) * sin(radians(angle - 90)) + 5
                    pygame.draw.ellipse(self.display, self.grid.matrix[i][j].color,
                                        (x - self.grid.matrix[i][j].vibrate(), y, self.d, self.d))

        pygame.display.update()

    # Increase the Atom when Clicked
    def addAtom(self, i, j, player):
        # grid_cpy = copy.deepcopy(grid)
        self.grid.matrix[i][j].add_atoms()
        self.grid.matrix[i][j].color = player.color
        # print(f'addAtom: [{i},{j}]: {self.grid.matrix[i][j].noAtoms}')

        if self.grid.matrix[i][j].noAtoms >= len(self.grid.matrix[i][j].neighbors):
            # print(f'cell lmt: {self.grid.matrix[i][j].type}')
            if not self.overFlow_manager(self.grid.matrix[i][j], player):

                self.grid = Grid(self.rows, self.cols)
                for row in self.grid.matrix:
                    for col in row:
                        col.noAtoms = col.type
                        col.color = player.color
                return False

        self.showPresentGrid()
        return True

    def check_inf_condition(self, player):
        for row in self.grid.matrix:
            for col in row:
                if not col.color == player.color:
                    return False
        return True

    def overFlow_manager(self, cell, player):
        q = queue.Queue()
        q.put(cell)
        while not q.empty():
            if self.check_inf_condition(player):
                return False
            c = q.get()
            cells = self.overflow(c, player)
            # print(f'overflow_manager: cells : {cells}')
            if len(cells) > 0:
                for c in cells:
                    q.put(c)

        return True

    def queue_values(q):
        l = []
        while not q.empty:
            l.append(q.get())

        for i in l:
            q.put(i)

        return l

    # Split the Atom when it Increases the "LIMIT"
    def overflow(self, cell, player):
        cells = []
        cell.noAtoms = 0
        for cell_neighbor in cell.neighbors:
            cell_neighbor.add_atoms()
            cell_neighbor.color = player.color
            if cell_neighbor.noAtoms > cell_neighbor.type:
                cells.append(cell_neighbor)

        return cells

    # Checking if Any Player has WON!
    def isPlayerInGame(self):
        # print(f'isPlayerInGame')
        playerScore = [0 for p in self.players]
        for row in range(self.rows):
            for col in range(self.cols):
                for k in range(self.no_Players):
                    if self.grid.matrix[row][col].color == self.players[k].color:
                        # playerScore[k] += grid.matrix[row][col].noAtoms
                        playerScore[k] += 1
        for i, score in enumerate(playerScore):
            if score == 0 and self.players[i] in self.players_playing:
                self.players_playing.remove(self.players[i])
                if self.players[self.players[i].next_player] in self.players_playing:
                    self.players[self.players[i].prev_player].next_player = self.players[i].next_player
                if self.players[self.players[i].prev_player] in self.players_playing:
                    self.players[self.players[i].next_player].prev_player = self.players[i].prev_player

        self.score = playerScore[:]

    # GAME OVER
    def gameOver(self, playerIndex):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        # del grid
                        # self.main_menu()
                        return
                    if event.key == pygame.K_r:
                        self.gameLoop()

            text = self.font.render(f"{self.players[playerIndex].name} Won!", True, self.white)
            text2 = self.font.render("Press \'r\' to Reset!", True, self.white)
            text3 = self.font.render("Press \'q\' to go to Main Menu", True, self.white)

            self.display.blit(text, (self.window_width / 3, self.window_height / 3))
            self.display.blit(text2, (self.window_width / 3, self.window_height / 2))
            self.display.blit(text3, (self.window_width / 3, self.window_height / 1.5))

            pygame.display.update()
            self.clock.tick(60)

    def checkWon(self):
        num = 0
        for i in range(self.no_Players):
            if self.score[i] == 0:
                num += 1
        if num == self.no_Players - 1:
            for i in range(self.no_Players):
                if self.score[i]:
                    return i

        return 9999

    # Main Loop
    def gameLoop(self):
        self.initializeGrid()

        print(self.grid.print_grid())
        print(f'noPlayers : {self.no_Players}')

        pygame.display.set_caption('Molecules')
        loop = True
        turns = 0
        current_player = 0
        add_successful = True

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.main_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if self.button_pause.collidepoint((x, y)):
                        if self.click:
                            self.close()

                    if x < self.padding_h or y < 2 * self.padding_v + self.pause_button_space or x > self.padding_h + self.grid_window_width or \
                            y > 2 * self.padding_v + self.pause_button_space + self.grid_window_height:
                        break
                    x_grid = x - self.padding_h
                    y_grid = y - 2 * self.padding_v - self.pause_button_space

                    i = int(y_grid / self.cell_side)
                    j = int(x_grid / self.cell_side)

                    print(f'gameLoop: x: {x}, y: {y}')
                    print(f'gameLoop: x`: {x_grid}, y`: {y_grid}')

                    print(f'gameLoop: grid  :{self.grid.matrix[i][j].color}')
                    print(f'gameLoop: player:{self.players[current_player].color}')

                    if self.grid.matrix[i][j].color == self.players[current_player].color or self.grid.matrix[i][
                        j].color == self.border:

                        turns += 1

                        add_successful = self.addAtom(i, j, self.players[current_player])
                        if not add_successful:
                            break
                        if turns >= self.no_Players:
                            self.isPlayerInGame()
                        current_player = self.players[current_player].next_player

                    # print(f'gameLoop: cp: {currentPlayer}')

            # redrawing the grid again
            self.display.fill(self.background)
            self.drawGrid(current_player)
            self.showPresentGrid()

            if not add_successful:
                self.gameOver(current_player)
                return

            pygame.display.update()

            res = self.checkWon()
            if res < 9999:
                self.gameOver(res)
                return

            self.clock.tick(20)

        self.mainClock = pygame.time.Clock()

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect()
        surface.blit(text_obj, (x, y))

    # A variable to check for the status later
    click = False

    # Main container function that holds the buttons and game functions
    def main_menu(self):
        while True:

            self.screen.fill((133, 255, 255))
            self.draw_text('Main Menu', self.font2, (255, 0, 0), self.screen, (self.window_width - 135) // 2,
                           (self.window_height - 270) // 2)

            mx, my = pygame.mouse.get_pos()

            # creating buttons
            button_play = pygame.Rect(200, 100, 200, 50)
            button_play.x = (self.window_width - 200) // 2
            button_play.y = (self.window_height - 100) // 2
            button_options = pygame.Rect(200, 180, 200, 50)
            button_options.x = (self.window_width - 200) // 2
            button_options.y = (self.window_height - 100) // 2 + 100

            # defining functions when a certain button is pressed
            if button_play.collidepoint((mx, my)):
                if self.click:
                    self.options()
                    # self.gameLoop()
            if button_options.collidepoint((mx, my)):
                if self.click:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.screen, (255, 0, 0), button_play)
            pygame.draw.rect(self.screen, (255, 0, 0), button_options)

            # writing text on top of button
            self.draw_text('PLAY', self.font2, (102, 255, 255), self.screen, (self.window_width - 120) // 2 + 20,
                           (self.window_height - 95) // 2)
            self.draw_text('QUIT', self.font2, (102, 255, 255), self.screen, (self.window_width - 125) // 2 + 20,
                           (self.window_height + 105) // 2)

            self.click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            pygame.display.update()

    def options(self):
        pygame.init()

        user_text_players = ''
        user_text_grid = ''

        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('lightskyblue2')

        active_players = False
        active_grid = False

        color_player = color_passive
        color_grid = color_passive

        input_rect_players = pygame.Rect(250, 200, 200, 50)
        input_rect_players_text = pygame.Rect(50, 200, 200, 50)
        input_rect_grid = pygame.Rect(300, 300, 200, 50)
        input_rect_grid_text = pygame.Rect(50, 300, 200, 50)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if active_players:
                        active_players = False
                        active_grid = True
                    elif active_grid:
                        active_grid = False

                elif active_players and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text_players = user_text_players[:-1]
                    else:
                        user_text_players += event.unicode

                elif active_grid and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text_grid = user_text_grid[:-1]
                    else:
                        user_text_grid += event.unicode

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    active_players = False
                    active_grid = False
                    if input_rect_players.collidepoint(event.pos):
                        active_players = True
                    elif input_rect_grid.collidepoint(event.pos):
                        active_grid = True
            self.screen.fill((133, 255, 255))

            color_player = color_passive
            if active_players:
                color_player = color_active

            color_grid = color_passive
            if active_grid:
                color_grid = color_active

            pygame.draw.rect(self.screen, color_player, input_rect_players)
            text_surface = self.font2.render(user_text_players, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_rect_players.x + 5, input_rect_players.y))
            input_rect_players.w = max(50, text_surface.get_width() + 10)

            text_surface = self.font2.render('players: ', True, (0, 0, 0))
            self.screen.blit(text_surface, input_rect_players_text)

            pygame.draw.rect(self.screen, color_grid, input_rect_grid)
            text_surface = self.font2.render(user_text_grid, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_rect_grid.x + 5, input_rect_grid.y))
            input_rect_grid.w = max(50, text_surface.get_width() + 10)

            text_surface = self.font2.render('grid-dimensions: ', True, (0, 0, 0))
            self.screen.blit(text_surface, input_rect_grid_text)

            pygame.display.flip()
            self.clock.tick(60)


game = Game()
game.main_menu()
