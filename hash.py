import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Definições de tela
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# Cores
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Velha")
screen.fill(BG_COLOR)

# Tabuleiro
board = [["" for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Funções auxiliares
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                           int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS,
                                   CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == ""

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "":
                return False
    return True

def check_win(player):
    # Verifica linhas
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_win_line((row, 0), (row, 2))
            return True
    # Verifica colunas
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_win_line((0, col), (2, col))
            return True
    # Verifica diagonais
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_win_line((0, 0), (2, 2))
        return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_win_line((2, 0), (0, 2))
        return True
    return False

def draw_win_line(start, end):
    start_x = start[1] * SQUARE_SIZE + SQUARE_SIZE // 2
    start_y = start[0] * SQUARE_SIZE + SQUARE_SIZE // 2
    end_x = end[1] * SQUARE_SIZE + SQUARE_SIZE // 2
    end_y = end[0] * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, (255, 0, 0), (start_x, start_y), (end_x, end_y), 4)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = ""

# Game Loop
player = "X"
game_over = False

draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                else:
                    if is_board_full():
                        game_over = True
                    else:
                        player = "O" if player == "X" else "X"

                draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = False
                player = "X"
                restart()

    pygame.display.update()
