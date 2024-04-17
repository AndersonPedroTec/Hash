import pygame
import sys
import random

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

# Sons
VALID_MOVE_SOUND = pygame.mixer.Sound("valid_move.wav")
VICTORY_SOUND = pygame.mixer.Sound("victory.wav")
DRAW_SOUND = pygame.mixer.Sound("draw.wav")

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

def computer_move(difficulty):
    if difficulty == "easy":
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        while not available_square(row, col):
            row = random.randint(0, 2)
            col = random.randint(0, 2)
    elif difficulty == "hard":
        best_score = -float("inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if available_square(i, j):
                    board[i][j] = "O"
                    score = minimax(board, 0, False)
                    board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        row, col = best_move
    return row, col

def minimax(board, depth, is_maximizing):
    if check_win("X"):
        return -10 + depth
    elif check_win("O"):
        return 10 - depth
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

# Game Loop
player = "X"
game_over = False
difficulty = "hard"  # Escolha entre "easy" ou "hard"

draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == "X":
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                VALID_MOVE_SOUND.play()  # Efeito sonoro para movimento válido
                if check_win(player):
                    game_over = True
                    VICTORY_SOUND.play()  # Efeito sonoro para vitória
                else:
                    if is_board_full():
                        game_over = True
                        DRAW_SOUND.play()  # Efeito sonoro para empate
                    else:
                        player = "O"

                draw_figures()

        if not game_over and player == "O":
            if difficulty == "easy":
                row, col = computer_move("easy")
            elif difficulty == "hard":
                row, col = computer_move("hard")

            mark_square(row, col, player)
            VALID_MOVE_SOUND.play()  # Efeito sonoro para movimento válido
            if check_win(player):
                game_over = True
                VICTORY_SOUND.play()  # Efeito sonoro para vitória
            elif is_board_full():
                game_over = True
                DRAW_SOUND.play()  # Efeito sonoro para empate
            else:
                player = "X"
            draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = False
                player = "X"
                restart()

    pygame.display.update()
