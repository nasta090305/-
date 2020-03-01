import pygame
import random
THINGS = [None, (255, 192, 203), (255, 228, 181), (255, 127, 80), (175, 238, 238), (152, 251, 152)]


def join_int(l):   # функция join для типа int
    l = [str(i) for i in l]
    return ''.join(l)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
        self.radius = 25
        self.deleted = False
        self.chosen = None
        self.moves = self.width * self.height // 2 + 5
        self.board = [[0] * width for _ in range(height)]
        self.filled_cells = [[True] * width for _ in range(height)]
        self.count_of_filled_cells = self.height * self.width
        for i in range(height):
            for j in range(width):
                self.board[i][j] = random.randint(1, 5)
        self.delete()
        while self.deleted:
            for i in range(height):
                for j in range(width):
                    if self.board[i][j] == 0:
                        self.board[i][j] = random.randint(1, 5)
                        self.deleted = False
            self.delete()
        self.filled_cells = [[True] * width for _ in range(height)]
        self.count_of_filled_cells = self.width * self.height
        self.left = 100
        self.top = 100
        self.score = 0
        self.cell_size = 60

    def set_view(self, left, top, cell_size, radius):   # настройка параметров доски
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.radius = radius

    def get_cell(self, mouse_pos):   # возвращает координаты клетки по которой нажал пользователь
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            return y, x
        return None

    def render(self):   # рисует игровое поле
        font = pygame.font.Font(None, 25)
        text = font.render('Ходов осталось: ' + str(self.moves), 1, (0, 0, 0))
        text_x = 10
        text_y = 10
        screen.blit(text, (text_x, text_y))
        text = font.render('Счёт:' + str(self.score), 1, (0, 0, 0))
        screen.blit(text, (10, 35))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color('black'),
                                 (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                  self.cell_size, self.cell_size), 1)
                if self.filled_cells[j][i]:
                    pygame.draw.rect(screen, (210, 210, 210),
                                     (self.left + self.cell_size * i + 1, self.top + self.cell_size * j + 1,
                                      self.cell_size - 2, self.cell_size - 2))
                if self.board[j][i] != 0:
                    pygame.draw.circle(screen, THINGS[self.board[j][i]],
                                       (self.left + self.cell_size * i + self.cell_size // 2,
                                        self.top + self.cell_size * j + self.cell_size // 2), self.radius)
                    pygame.draw.circle(screen, pygame.Color('black'),
                                       (self.left + self.cell_size * i + self.cell_size // 2,
                                        self.top + self.cell_size * j + self.cell_size // 2), self.radius + 1, 1)
                    if (j, i) == self.chosen:
                        pygame.draw.circle(screen, pygame.Color('black'),
                                           (self.left + self.cell_size * i + self.cell_size // 2,
                                            self.top + self.cell_size * j + self.cell_size // 2), 5)
                else:
                    pygame.draw.circle(screen, pygame.Color('white'),
                                       (self.left + self.cell_size * i + self.cell_size // 2,
                                        self.top + self.cell_size * j + self.cell_size // 2), 21)

    def update(self):   # обновляет доску заполняя все пустые клетки
        for i in range(self.height - 1, -1, -1):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    self.fill(i, j)

    def on_click(self, mouse_pos):   # реагирует на нажатие на определенную клетку доски и меняет элементы местами
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            global game, end
            if self.chosen is None:
                self.chosen = cell
            elif self.chosen == cell:
                self.chosen = None
            else:
                if ((cell[0] == self.chosen[0] + 1 or cell[0] == self.chosen[0] - 1) and cell[1] == self.chosen[1]) or\
                 (cell[0] == self.chosen[0] and (cell[1] == self.chosen[1] - 1 or cell[1] == self.chosen[1] + 1)):
                    self.board[cell[0]][cell[1]], self.board[self.chosen[0]][self.chosen[1]] =\
                     self.board[self.chosen[0]][self.chosen[1]], self.board[cell[0]][cell[1]]
                    self.chosen = None
                    self.moves -= 1
                    if self.moves == 0:
                        game = False
                        end = True

    def delete(self):   # находит и удаляет все комбинации трех и более подряд одинаковых элементов
        global game, end
        lines = [join_int(i) for i in self.board]
        columns = []
        for i in range(self.width):
            columns.append(join_int([j[i] for j in self.board]))
        for i in range(1, len(THINGS) + 1):
            for j in range(self.height):
                if str(i) * 3 in lines[j]:
                    self.board[j][lines[j].index(str(i) + str(i) + str(i))] = 0
                    self.board[j][lines[j].index(str(i) + str(i) + str(i)) + 1] = 0
                    self.board[j][lines[j].index(str(i) + str(i) + str(i)) + 2] = 0
                    self.score += 30
                    if self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i))]:
                        self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i))] = False
                        self.count_of_filled_cells -= 1
                    if self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i)) + 1]:
                        self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i)) + 1] = False
                        self.count_of_filled_cells -= 1
                    if self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i)) + 2]:
                        self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i)) + 2] = False
                        self.count_of_filled_cells -= 1
                    if str(i) * 4 in lines[j]:
                        self.board[j][lines[j].index(str(i) + str(i) + str(i)) + 3] = 0
                        self.score += 20
                        if self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i)) + 3]:
                            self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i)) + 3] = False
                            self.count_of_filled_cells -= 1
                        if str(i) * 5 in lines[j]:
                            self.score += 30
                            self.board[j][lines[j].index(str(i) + str(i) + str(i)) + 4] = 0
                            if self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i)) + 4]:
                                self.filled_cells[j][lines[j].index(str(i) + str(i) + str(i)) + 4] = False
                                self.count_of_filled_cells -= 1
                    self.deleted = True
            for j in range(self.width):
                if str(i) * 3 in columns[j]:
                    self.board[columns[j].index(str(i) + str(i) + str(i))][j] = 0
                    self.board[columns[j].index(str(i) + str(i) + str(i)) + 1][j] = 0
                    self.board[columns[j].index(str(i) + str(i) + str(i)) + 2][j] = 0
                    self.score += 30
                    if self.filled_cells[columns[j].index(str(i) + str(i) + str(i))][j]:
                        self.filled_cells[columns[j].index(str(i) + str(i) + str(i))][j] = False
                        self.count_of_filled_cells -= 1
                    if self.filled_cells[columns[j].index(str(i) + str(i) + str(i)) + 1][j]:
                        self.filled_cells[columns[j].index(str(i) + str(i) + str(i)) + 1][j] = False
                        self.count_of_filled_cells -= 1
                    if self.filled_cells[columns[j].index(str(i) + str(i) + str(i)) + 2][j]:
                        self.filled_cells[columns[j].index(str(i) + str(i) + str(i)) + 2][j] = False
                        self.count_of_filled_cells -= 1
                    if str(i) * 4 in columns[j]:
                        self.score += 20
                        self.board[columns[j].index(str(i) + str(i) + str(i)) + 3][j] = 0
                        if self.filled_cells[columns[j].index(str(i) + str(i) + str(i)) + 3][j]:
                            self.filled_cells[columns[j].index(str(i) + str(i) + str(i)) + 3][j] = False
                            self.count_of_filled_cells -= 1
                        if str(i) * 5 in columns[j]:
                            self.score += 30
                            self.board[columns[j].index(str(i) + str(i) + str(i)) + 4][j] = 0
                            if self.filled_cells[columns[j].index(str(i) + str(i) + str(i)) + 4][j]:
                                self.filled_cells[columns[j].index(str(i) + str(i) + str(i)) + 4][j] = False
                                self.count_of_filled_cells -= 1
                    self.deleted = True
        if self.count_of_filled_cells == 0:
            end = True
            game = False

    def fill(self, x, y):   # заполняет указанную клетку
        global screen
        if x == 0:
            self.board[x][y] = random.randint(1, 5)
            self.render()
        else:
            pygame.init()
            if self.board[x - 1][y] == 0:
                self.fill(x - 1, y)
            center_x = self.left + self.cell_size * y + self.cell_size // 2
            center_y = self.top + self.cell_size * (x + 1) + self.cell_size // 2
            while center_y != self.top + self.cell_size * x + self.cell_size // 2:
                pygame.draw.circle(screen, pygame.Color('white'), (center_x, center_y), 20)
                pygame.draw.rect(screen, pygame.Color('black'),
                                 (self.left + self.cell_size * y, self.top + self.cell_size * x,
                                  self.cell_size, self.cell_size), 1)
                center_y -= 1
                pygame.draw.circle(screen, THINGS[self.board[x - 1][y]], (center_x, center_y), 20)
            self.board[x][y] = self.board[x - 1][y]
            self.board[x - 1][y] = 0


def draw_home_screen():   # Функция рисующая начальный экран
    font = pygame.font.Font(None, 50)
    text = font.render('Три в ряд', 1, (0, 0, 0))
    screen.blit(text, (160, 110))
    font = pygame.font.Font(None, 27)
    text = font.render('Меняйте элементы местами!', 1, (0, 0, 0))
    screen.blit(text, (120, 190))
    font = pygame.font.Font(None, 27)
    text = font.render('Составляйте комбинации!', 1, (0, 0, 0))
    screen.blit(text, (140, 225))
    font = pygame.font.Font(None, 27)
    text = font.render('Уничтожьте все закрашенные клетки!', 1, (0, 0, 0))
    screen.blit(text, (80, 260))
    font = pygame.font.Font(None, 25)
    text = font.render('[Нажмите чтобы начать]', 1, (0, 0, 0))
    screen.blit(text, (155, 380))


def draw_mode_screen():   # функция рисующая экран с выбором уровня сложности
    font = pygame.font.Font(None, 45)
    text = font.render('Выберите режим:', 1, (0, 0, 0))
    screen.blit(text, (120, 80))
    pygame.draw.rect(screen, (0, 0, 0), (125, 150, 250, 60), 1)
    pygame.draw.rect(screen, (150, 150, 150), (129, 154, 250, 60), 2)
    font = pygame.font.Font(None, 37)
    text = font.render('Простой', 1, (0, 0, 0))
    screen.blit(text, (195, 170))
    pygame.draw.rect(screen, (0, 0, 0), (125, 240, 250, 60), 1)
    pygame.draw.rect(screen, (150, 150, 150), (129, 244, 250, 60), 2)
    font = pygame.font.Font(None, 37)
    text = font.render('Нормальный', 1, (0, 0, 0))
    screen.blit(text, (170, 260))
    pygame.draw.rect(screen, (0, 0, 0), (125, 330, 250, 60), 1)
    pygame.draw.rect(screen, (150, 150, 150), (129, 334, 250, 60), 2)
    font = pygame.font.Font(None, 37)
    text = font.render('Сложный', 1, (0, 0, 0))
    screen.blit(text, (190, 350))


def draw_end_screen():   # функция рисующая экран окончания игры
    font = pygame.font.Font(None, 55)
    if board.count_of_filled_cells == 0:
        text = font.render('Победа!', 1, (0, 0, 0))
        screen.blit(text, (170, 120))
        font = pygame.font.Font(None, 45)
        text = font.render('Счёт: ' + str(board.score), 1, (0, 0, 0))
        screen.blit(text, (173, 200))
    else:
        text = font.render("Проигрыш!", 1, (0, 0, 0))
        screen.blit(text, (150, 120))
    font = pygame.font.Font(None, 25)
    text = font.render('[Нажмите чтобы вернуться на главный экран]', 1, (0, 0, 0))
    screen.blit(text, (70, 380))


pygame.init()
screen = pygame.display.set_mode((500, 500))
running = True
board = Board(5, 5)
home_screen = True
game = False
end = False
mode = False
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
while running:
    if home_screen:
        screen.fill((255, 255, 255))
        draw_home_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mode = True
                home_screen = False
    if mode:
        screen.fill((255, 255, 255))
        draw_mode_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 125 <= event.pos[0] <= 379 and 150 <= event.pos[1] <= 214:
                    board = Board(5, 5)
                    game = True
                    mode = False
                elif 125 <= event.pos[0] <= 379 and 240 <= event.pos[1] <= 304:
                    board = Board(7, 7)
                    board.set_view(75, 95, 50, 20)
                    game = True
                    mode = False
                elif 125 <= event.pos[0] <= 379 and 330 <= event.pos[1] <= 394:
                    board = Board(9, 9)
                    board.set_view(37, 60, 47, 18)
                    game = True
                    mode = False
    if game:
        board.delete()
        board.update()
        board.deleted = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 320 <= event.pos[0] <= 494 and 10 <= event.pos[1] <= 54:
                    game = False
                    home_screen = True
                board.on_click(event.pos)
        screen.fill((255, 255, 255))
        board.render()
        pygame.draw.rect(screen, (0, 0, 0), (320, 10, 170, 40), 1)
        pygame.draw.rect(screen, (150, 150, 150), (324, 14, 170, 40), 1)
        font = pygame.font.Font(None, 30)
        text = font.render('На главную', 1, (0, 0, 0))
        screen.blit(text, (347, 22))
    if end:
        screen.fill((255, 255, 255))
        draw_end_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                home_screen = True
                end = False
    pygame.display.flip()
