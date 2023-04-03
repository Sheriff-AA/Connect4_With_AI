import numpy as np
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

BLUE = (0,0,200)
BLACK= (0,0,0)
RED = (255, 0,0)
YELLOW = (255, 255, 0)

PLAYER_1 = 0
PLAYER_2 = 1


def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_selected_col_valid(board, col):
    # check if selected column filled up?
    return board[ROW_COUNT-1][col] == 0


def select_valid_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        

def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # check horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # check diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
            

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # position of the squares and the size of the rectangle
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)) 
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE/2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2), RADIUS)
            
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    pygame.display.update()


def player_move(board, turn):
    position_x = event.pos[0]
    col_selection = int(math.floor(position_x/SQUARESIZE))
    # col_selection = int(input("Player * make your selection (0-6): ")

    if is_selected_col_valid(board, col_selection):
        row = select_valid_row(board, col_selection)
        drop_piece(board, row, col_selection, turn)


def display_message(player):
    label = myfont.render(f"Player {player} wins!", 1, RED)
    screen.blit(label, (40, 10))


def set_piece(position):
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
    if player_turn == 0:
        pygame.draw.circle(screen, RED, (position, int(SQUARESIZE/2)), RADIUS)
    else:
        pygame.draw.circle(screen, YELLOW, (position, int(SQUARESIZE/2)), RADIUS)


            

board = create_board()  # initialize the board
print(board)
game_over = False   # has someone won or the game over?
player_turn = 0    # checks for players turns

pygame.init()

# Size of the game in pixels
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

RADIUS = int(SQUARESIZE/2-5)

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
myfont = pygame.font.SysFont("monospace", 75)
position_x = int(width / 2)

# game runs until someone wins
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            position_x = event.pos[0]
        # elif np.all(board==0):
        #     position_x = int(width / 2)
        
        set_piece(position_x)
        pygame.display.update()       

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # Player 1
            if player_turn == PLAYER_1:
                player_move(board, player_turn + 1)
                if winning_move(board, player_turn + 1):
                    display_message(player_turn + 1)
                    game_over = True

            # Player 2
            else:
                player_move(board, player_turn + 1)
                if winning_move(board, player_turn + 1):
                    display_message(player_turn + 1)
                    game_over = True

            print_board(board)
            draw_board(board)

            player_turn = (player_turn+1) % 2

            if game_over:
                pygame.time.wait(3000)