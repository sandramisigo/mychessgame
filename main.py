import pygame
import sys

pygame.init()

#defining constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH//8

#my chess colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

#creating screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Chess Game")

#Chess piece class

class MyChessPiece:
    def __init__(self, color, type, image):
        self.color = color
        self.type = type
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.has_moved = False

#initialize the board

board = [[None for _ in range(8)] for _ in range(8)]

#THE current player

current_player = 'white'

#selected piece
selected_piece = None
selected_position = None

def init_board():
    #Pawns
    for col in range(8):
        board[1][col] = MyChessPiece('black', 'pawn', 'images/black_pawn.png')
        board[6][col] = MyChessPiece('white', 'pawn', 'images/white_pawn.png')
    #Rooks
    board[0][0] = board[0][7] = MyChessPiece('black', 'rook', 'images/black_rook.png')
    board[7][0] = board[7][7] = MyChessPiece('white', 'rook', 'images/white_rook.png')
    #Knights
    board[0][1] = board[0][6] = MyChessPiece('black', 'knight', 'images/black_knight.png')
    board[7][1] = board[7][6] = MyChessPiece('white', 'knight', 'images/white_knight.png')
   
    #Bishops
    board[0][2] = board[0][5] = MyChessPiece('black', 'bishop', 'images/black_bishop.png')
    board[7][2] = board[7][5] = MyChessPiece('white', 'bishop', 'images/white_bishop.png')
   
    #Queens
    board[0][3] = MyChessPiece('black', 'queen', 'images/black_queen.png')
    board[7][3] = MyChessPiece('white', 'queen', 'images/white_queen.png')
   
    #Kings
    board[0][4] = MyChessPiece('black', 'king', 'images/black_king.png')
    board[7][4] = MyChessPiece('white', 'king', 'images/white_king.png')

#function to draw the board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row+col)%2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    if selected_position:
        pygame.draw.rect(screen, YELLOW, (selected_position[1]*SQUARE_SIZE, selected_position[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


#function to draw chess pieces
def draw_pieces(): 
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                screen.blit(piece.image, (col*SQUARE_SIZE, row*SQUARE_SIZE))

#function for valid chess piece moves
def get_valid_moves(piece, row, col): 
    moves = []              
    if piece.type == 'pawn':
        direction = -1 if piece.color == 'white' else 1
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))
            if (piece.color == 'white' and row == 6) or (piece.color == 'black' and row == 1):
                if board[row + 2*direction][col] is None:
                    moves.append((row + 2*direction, col))
        for dc in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + dc < 8 and board[row + direction][col + dc] and board[row + direction][col + dc].color != piece.color:
                if board[row + direction][col + dc]:
                    moves.append((row + direction, col + dc))

    elif piece.type == 'rook':
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
            
    elif piece.type == 'knight':
        for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] is None or board[r][c].color != piece.color):
                moves.append((r, c))

    elif piece.type == 'bishop':
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc

    elif piece.type == 'queen':
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc

    elif piece.type == 'king':
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] is None or board[r][c].color != piece.color):
                    moves.append((r, c))
            
    return moves


#function to check whether the king is in check

def is_check(color):
    king_position = None
    for row in range(8):
        for col in range(8):
            if board[row][col] and board[row][col].color == color and board[row][col].type == 'king':
                king_position = (row, col)
                break
            if king_position:
                break

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color != color:
                if king_position in get_valid_moves(piece, row, col):
                    return True


    return False

#function to check whether there is a checkmate
def has_game_ended():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color == current_player:
               valid_moves = get_valid_moves(piece, row, col)
               for move in valid_moves:
                   #try move
                   temp = board[move[0]][move[1]]
                   board[move[0]][move[1]] = piece
                   board[row][col] = None
                   check = is_check(current_player)
                   #undo move
                   board[row][col] = piece
                   board[move[0]][move[1]] = temp
                   if not check:
                       return False
    return True

#function to handle mpouse clicks
def handle_mouse_click(position):
    global selected_piece, selected_position, current_player
    col = position[0]//SQUARE_SIZE
    row = position[1]//SQUARE_SIZE

    if selected_piece is None:
       piece = board[row][col]
       if piece and piece.color == current_player:
           selected_piece = piece
           selected_position = (row, col)
    else:
        if (row, col) in get_valid_moves(selected_piece, selected_position[0], selected_position[1]):
            #make the move
            board[row][col] = selected_piece
            board[selected_position[0]][selected_position[1]] = None
            selected_piece.has_moved = True

            #check pawn promotion
            if selected_piece.type == 'pawn' and (row == 0 or row == 7):
                board[row][col] = MyChessPiece(selected_piece.color, 'queen', f'images/{selected_piece.color}_queen.png')

            #switch player after move, regardless of piece type

            current_player = 'black' if current_player == 'white' else 'white'

                #check for game end
            if has_game_ended():
                if is_check(current_player):
                     print(f'Checkmate! {current_player.capitalize()} has lost.')
                else:
                    print('Stalemate! The game is a draw.')
                
        selected_piece = None
        selected_position = None

#main loop for the game
def main():
    init_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(pygame.mouse.get_pos())
        draw_board()
        draw_pieces()
        pygame.display.flip()

if __name__ == '__main__':
    main()

                        
