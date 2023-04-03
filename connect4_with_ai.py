import numpy as np
import pygame
import sys
import random
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

BLUE = (0,0,200)
BLACK= (0,0,0)
RED = (255, 0,0)
YELLOW = (255, 255, 0)

PLAYER_1 = 0
CONNECT4_AI = 1
WINDOW_LENGTH = 4
EMPTY = 0


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
            if board[r][c] == PLAYER_1 + 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == CONNECT4_AI + 1:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    pygame.display.update()


def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_1 + 1

    if piece == PLAYER_1 + 1:
        opponent_piece = CONNECT4_AI + 1

    if window.count(piece) == 4:    # IF THERE IS A CONNCT 4 ON THE BOARD
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 8
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5
    
    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 11
    
    return score

def player_move(board, turn):
    position_x = event.pos[0]
    col_selection = int(math.floor(position_x/SQUARESIZE))
    # col_selection = int(input("Player * make your selection (0-6): ")

    if is_selected_col_valid(board, col_selection):
        row = select_valid_row(board, col_selection)
        drop_piece(board, row, col_selection, turn)


def display_message(player):
    if player == PLAYER_1 + 1:
        label = myfont.render(f"Player {player} wins!", 1, RED)
    else:
        label = myfont.render(f"Player {player} wins!", 1, YELLOW)
    screen.blit(label, (40, 10))


def set_piece(position):
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

    if player_turn == PLAYER_1:
        pygame.draw.circle(screen, RED, (position, int(SQUARESIZE/2)), RADIUS)


def score_position(board, piece):
    # APPLY A SCORE TO THE POSITIONS
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 5

    # CHECKING HORIZONTAL POSITIONS
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])] # ROWS ON THE BOARD
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]   # GET 4 PIECES IN THE ROW
            score += evaluate_window(window, piece)

    # CHECK VERTICAL POSITIONS
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    
    ## SCORE DIAGONALS
    for r in range(ROW_COUNT-3):
        for c in range (COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range (COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def get_valid_locations(board):
    # COLUMNS THAT ARE NOT FULL
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_selected_col_valid(board, col):
            valid_locations.append(col)
    
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -1000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = select_valid_row(board, col)
        temp_board = board.copy()   # CREATE A COPY OF THE BOARD TO EVALUATE POSITIONS
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)   # SCORING THE POSITIONS
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def is_terminal_node(board):
    return winning_move(board, PLAYER_1+1) or winning_move(board, CONNECT4_AI+1) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, CONNECT4_AI+1):
                return (None, 100000)
            elif winning_move(board, PLAYER_1+1):
                return (None, -100000)
            else:
                return (None, 0)    #GAME OVER
        else:
            return (None, score_position(board, CONNECT4_AI+1))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = select_valid_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, CONNECT4_AI+1)
            new_score = minimax(board_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:   # Minimizing Player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = select_valid_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, PLAYER_1+1)
            new_score = minimax(board_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
            

board = create_board()  # INITIALIZE THE BOARD
print(board)
game_over = False   # HAS SOMEONE WON OR IS THE GAME OVER?
player_turn = random.randint(PLAYER_1, CONNECT4_AI)   # RANDOMIZE INITIAL PLAYER TURN

pygame.init()

# SIZE OF THE GAME IN PIXELS
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
                player_move(board, PLAYER_1+1)

                if winning_move(board, player_turn + 1):
                    display_message(player_turn + 1)
                    game_over = True

                player_turn = (player_turn+1) % 2
                print_board(board)
                draw_board(board)

    # AI
    if player_turn == CONNECT4_AI and not game_over:
        
        # col_selection = random.randint(0, COLUMN_COUNT-1)
        # col_selection = pick_best_move(board, CONNECT4_AI+1)
        col_selection, minimax_score = minimax(board, 4, -math.inf, math.inf, True)

        if is_selected_col_valid(board, col_selection):
            pygame.time.wait(500)
            row = select_valid_row(board, col_selection)
            drop_piece(board, row, col_selection, player_turn+1)
        # player_move(board, player_turn + 1)

            if winning_move(board, CONNECT4_AI+1):
                display_message(CONNECT4_AI+1)
                game_over = True

            print_board(board)
            draw_board(board)

            player_turn = (player_turn+1) % 2

    if game_over:
        pygame.time.wait(3000)