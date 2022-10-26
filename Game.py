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
        self.pause_button_space = 50
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

        self.players = [Player(0, [255, 0, 0], "LynX"), Player(1, [0, 0, 255], "Prometheus")]
        self.no_Players = len(self.players)
        self.players_playing = set()
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

        self.menu_window_width = 860
        self.menu_window_height = 650

    # Quit or Close the Game Window
    def close(self):
        pygame.quit()
        sys.exit()

    # Initializing the Grid with "Empty or 0"
    def initialize_grid(self):

        self.cols = int(self.grid_window_width // self.cell_side)
        self.rows = int(self.grid_window_height // self.cell_side)

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

        for player in self.players:
            if player not in self.players_playing:
                self.players_playing.add(player)

        print(f'initialize_grid: players: {self.players}')

    # Draw the Grid in Pygame Window
    def draw_grid(self, currentIndex):

        r = 0
        c = 0
        for i in range(self.grid_window_width // self.cell_side + 1):
            # print(f'drawGrid: currentIndex: {currentIndex}')
            # print(f'drawGrid: players: {self.players}')
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
    def show_present_grid(self):
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
    def add_atom(self, i, j, player):
        self.grid.matrix[i][j].add_atoms()
        self.grid.matrix[i][j].color = player.color
        print(f'addAtom: [{i},{j}]: {self.grid.matrix[i][j].noAtoms}')

        if self.grid.matrix[i][j].noAtoms >= len(self.grid.matrix[i][j].neighbors):
            print(f'cell lmt: {self.grid.matrix[i][j].type}')
            if not self.overflow_manager(self.grid.matrix[i][j], player):

                self.grid = Grid(self.rows, self.cols)
                for row in self.grid.matrix:
                    for col in row:
                        col.noAtoms = col.type
                        col.color = player.color
                return False

        self.show_present_grid()
        return True

    def check_inf_condition(self, player):
        for row in self.grid.matrix:
            for col in row:
                if not col.color == player.color:
                    return False
        return True

    def overflow_manager(self, cell, player):
        q = queue.Queue()
        q.put(cell)
        while not q.empty():
            if self.check_inf_condition(player):
                return False
            c = q.get()
            cells = self.overflow(c, player)
            print(f'overflow_manager: cells : {cells}')
            if len(cells) > 0:
                for c in cells:
                    q.put(c)

        return True

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
    def is_player_in_game(self):
        print(f'isPlayerInGame')
        playerScore = [0 for p in self.players]
        for row in range(self.rows):
            for col in range(self.cols):
                for k in range(len(self.players)):
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
        print(f'is_player_in_game: players: {self.players_playing}')

    # GAME OVER
    def game_over(self, playerIndex):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.main_menu()
                        # return
                    if event.key == pygame.K_r:
                        self.game_loop()

            text = self.font.render(f"{self.players[playerIndex].name} Won!", True, self.white)
            text2 = self.font.render("Press \'r\' to Reset!", True, self.white)
            text3 = self.font.render("Press \'q\' to go to Main Menu", True, self.white)

            self.display.blit(text, (self.window_width / 3, self.window_height / 3))
            self.display.blit(text2, (self.window_width / 3, self.window_height / 2))
            self.display.blit(text3, (self.window_width / 3, self.window_height / 1.5))

            pygame.display.update()
            self.clock.tick(60)

    def check_won(self):
        num = 0
        for i in range(len(self.players)):
            if self.score[i] == 0:
                num += 1
        if num == len(self.players) - 1:
            for i in range(len(self.players)):
                if self.score[i]:
                    return i

        return 9999

    # Main Loop
    def game_loop(self):
        self.initialize_grid()

        print("Grid: ")
        self.grid.print_grid()
        print(f'\nnoPlayers : {len(self.players)}')

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
                            self.main_menu()

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

                        add_successful = self.add_atom(i, j, self.players[current_player])
                        if not add_successful:
                            break
                        if turns >= len(self.players):
                            self.is_player_in_game()
                        current_player = self.players[current_player].next_player

                    print(f'gameLoop: cp: {current_player}')

            # redrawing the grid again
            self.display.fill(self.background)
            self.draw_grid(current_player)
            self.show_present_grid()

            if not add_successful:
                self.game_over(current_player)
                return

            pygame.display.update()

            res = self.check_won()
            if res < 9999:
                self.game_over(res)
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

        print(f'main_menu: ')

        self.window_width = self.menu_window_width
        self.window_height = self.menu_window_height

        self.display = pygame.display.set_mode((self.window_width, self.window_height))

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
        user_text_x = ''
        user_text_y = ''

        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('lightskyblue2')

        active_players = False
        active_x = False
        active_y = False

        color_player = color_passive
        color_x = color_passive
        color_y = color_passive
        print(f'options: window dim: {self.window_width}, {self.window_height}')
        input_rect_players = pygame.Rect(2*self.window_width//3, self.window_height//5, self.window_width//20, self.window_height//20 + 10)
        input_rect_players_text = pygame.Rect(self.window_width//3 - 50, self.window_height//5, self.window_width//5 + 50, self.window_height//13)
        input_rect_x = pygame.Rect(2*self.window_width//3, self.window_height//5 + 75, self.window_width//20, self.window_height//20 + 10)
        input_rect_x_text = pygame.Rect(self.window_width//3 - 50, self.window_height//5 + 75, self.window_width//5 + 50, self.window_height//13)
        input_rect_y = pygame.Rect(2 * self.window_width // 3, self.window_height // 5 + 150, self.window_width // 20,
                                   self.window_height // 20 + 10)
        input_rect_y_text = pygame.Rect(self.window_width // 3 - 50, self.window_height // 5 + 150, self.window_width//5 + 50, self.window_height//13)
        next_rect = pygame.Rect(self.window_width//2 - 100, self.window_height // 5 + 250, self.window_width//5 + 50, self.window_height//13)

        esc_button_pressed = False
        while True:

            for event in pygame.event.get():
                # print(f'{pygame.event.get()}')

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # print("options: esc pressed")
                    esc_button_pressed = True
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if active_players:
                        active_players = False
                        active_x = True
                    elif active_x:
                        active_x = False
                        active_y = True
                    elif active_y:
                        active_y = False

                elif active_players and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text_players = user_text_players[:-1]
                    else:
                        user_text_players += event.unicode

                elif active_x and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text_x = user_text_x[:-1]
                    else:
                        user_text_x += event.unicode
                elif active_y and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text_y = user_text_y[:-1]
                    else:
                        user_text_y += event.unicode

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    active_players = False
                    active_x = False
                    active_y = False
                    if input_rect_players.collidepoint(event.pos):
                        active_players = True
                    elif input_rect_x.collidepoint(event.pos):
                        active_x = True
                    elif input_rect_y.collidepoint(event.pos):
                        active_y = True
                    elif next_rect.collidepoint(event.pos):
                        if user_text_players == '' or user_text_players.isspace() or user_text_x == '' or \
                                user_text_x.isspace() or user_text_y == '' or user_text_y.isspace():
                            continue
                        if not user_text_players.isdigit() or not user_text_x.isdigit() or not user_text_y.isdigit():
                            continue
                        self.no_Players = int(user_text_players)
                        self.grid_window_width = (self.cell_side * (int(user_text_x)))
                        self.grid_window_height = (self.cell_side * (int(user_text_y)))

                        self.window_width = self.grid_window_width + 100
                        self.window_height = self.grid_window_height + self.player_name_space + self.pause_button_space + 3 * self.padding_v

                        self.options2(self.no_Players)
            self.screen.fill((133, 255, 255))

            color_player = color_passive
            if active_players:
                color_player = color_active

            color_x = color_passive
            if active_x:
                color_x = color_active

            color_y = color_passive
            if active_y:
                color_y = color_active

            pygame.draw.rect(self.screen, color_player, input_rect_players)
            text_surface = self.font2.render(user_text_players, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_rect_players.x + 8, input_rect_players.y))
            # input_rect_players.w = max(50, text_surface.get_width() + 10)

            text_surface = self.font2.render('Number of Players : ', True, (255, 0, 0))
            self.screen.blit(text_surface, input_rect_players_text)

            text_surface = self.font2.render('X - Dimension : ', True, (255, 0, 0))
            self.screen.blit(text_surface, input_rect_x_text)

            pygame.draw.rect(self.screen, color_x, input_rect_x)
            text_surface = self.font2.render(user_text_x, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_rect_x.x + 8, input_rect_x.y))

            text_surface = self.font2.render('Y - Dimension : ', True, (255, 0, 0))
            self.screen.blit(text_surface, input_rect_y_text)

            pygame.draw.rect(self.screen, color_y, input_rect_y)
            text_surface = self.font2.render(user_text_y, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_rect_y.x + 8, input_rect_y.y))

            pygame.draw.rect(self.screen, (255, 0, 0), next_rect)
            # self.draw_text('Next', self.font2, (133, 255, 255), self.screen, self.window_width//5 + 50 +
            #                (self.window_width//5 + 50)//2, self.window_height//13 + (self.window_height//13)//2)
            self.draw_text('Next', self.font2, (133, 255, 255), self.screen, next_rect.x + next_rect.w//2 - 35, next_rect.y + next_rect.h//2 - 20)
            pygame.display.flip()
            self.clock.tick(60)

            if esc_button_pressed:
                break

        if esc_button_pressed:
            self.main_menu()

    def options2(self, n):

        self.players = [Player(_) for _ in range(n)]
        print(f'options2: players: {self.players}')

        pygame.init()

        user_names = ['' for player in self.players]
        user_color = ['' for _ in self.players]

        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('lightskyblue2')

        active_players = [False for _ in self.players]
        active_colors = [False for _ in self.players]

        color_player = [color_passive for _ in self.players]
        color_color = [color_passive for _ in self.players]

        input_rect_players_name = []
        input_rect_players_name_text = []
        input_rect_players_color = []
        input_rect_players_color_text = []

        in_player_space = 170
        right_shift = 390

        for i in range(n):
            if i >= 3:
                input_rect_players_color_text.append(pygame.Rect(50 + right_shift, 100 + in_player_space * (i - 3), 200, 50))
                input_rect_players_name.append(pygame.Rect(250 + right_shift, 30 + in_player_space * (i - 3), 200, 50))
                input_rect_players_name_text.append(pygame.Rect(50 + right_shift, 30 + in_player_space * (i - 3), 200, 50))
                input_rect_players_color.append(pygame.Rect(250 + right_shift, 100 + in_player_space * (i - 3), 200, 50))
            else:
                input_rect_players_color_text.append(pygame.Rect(50, 100 + in_player_space * i, 200, 50))
                input_rect_players_name.append(pygame.Rect(250, 30 + in_player_space * i, 200, 50))
                input_rect_players_name_text.append(pygame.Rect(50, 30 + in_player_space * i, 200, 50))
                input_rect_players_color.append(pygame.Rect(250, 100 + in_player_space * i, 200, 50))


        enter_button_dim_x = 200
        enter_button_dim_y = 50
        enter_button_pos_x = (self.menu_window_width - enter_button_dim_x) // 2
        enter_button_pos_y = 560
        button_enter = pygame.Rect(enter_button_pos_x, enter_button_pos_y, enter_button_dim_x, enter_button_dim_y)

        esc_button_pressed = False

        while True:
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    esc_button_pressed = True
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if button_enter.collidepoint((mx, my)):

                        for i in range(n):
                            user_color[i] = user_color[i].strip().split(' ')
                            temp = []
                            for a in user_color[i]:
                                color = int(a)
                                temp.append(color)
                            user_color[i] = temp

                        self.players = []
                        for i in range(n):
                            self.players.append(Player(i, user_color[i], user_names[i]))

                        self.display = pygame.display.set_mode((self.window_width, self.window_height))

                        self.game_loop()

                for i in range(n):
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if active_players[i]:
                            active_players[i] = False
                            active_colors[i] = True
                        elif active_colors[i]:
                            active_colors[i] = False
                            if i != n-1:
                                active_players[i+1] = True

                    elif active_players[i] and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            user_names[i] = user_names[i][:-1]
                        else:
                            user_names[i] += event.unicode

                    elif active_colors[i] and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            user_color[i] = user_color[i][:-1]
                        else:
                            user_color[i] += event.unicode

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        active_players[i] = False
                        active_colors[i] = False
                        if input_rect_players_name[i].collidepoint(event.pos):
                            active_players[i] = True
                        elif input_rect_players_color[i].collidepoint(event.pos):
                            active_colors[i] = True
            self.screen.fill((133, 255, 255))

            for i in range(n):
                color_player[i] = color_passive
                if active_players[i]:
                    color_player[i] = color_active

                color_color[i] = color_passive
                if active_colors[i]:
                    color_color[i] = color_active

                text_surface = self.font2.render(user_names[i], True, (0, 0, 0))
                input_rect_players_name[i].w = max(50, text_surface.get_width() + 10)
                pygame.draw.rect(self.screen, color_player[i], input_rect_players_name[i])
                self.screen.blit(text_surface, (input_rect_players_name[i].x + 5, input_rect_players_name[i].y))

                text_surface = self.font2.render('Player Name: ', True, (255, 0, 0))
                self.screen.blit(text_surface, input_rect_players_name_text[i])

                text_surface = self.font2.render(user_color[i], True, (0, 0, 0))
                input_rect_players_color[i].w = max(50, text_surface.get_width() + 10)
                pygame.draw.rect(self.screen, color_color[i], input_rect_players_color[i])
                self.screen.blit(text_surface, (input_rect_players_color[i].x + 5, input_rect_players_color[i].y))

                text_surface = self.font2.render('Player Color: ', True, (255, 0, 0))
                self.screen.blit(text_surface, input_rect_players_color_text[i])

            pygame.draw.rect(self.screen, (255, 0, 0), button_enter)
            self.draw_text('ENTER', self.font2, (133, 255, 255), self.screen, enter_button_pos_x + 50, enter_button_pos_y)

            pygame.display.flip()
            self.clock.tick(60)

            if esc_button_pressed:
                break

        if esc_button_pressed:
            self.main_menu()


game = Game()
game.main_menu()
