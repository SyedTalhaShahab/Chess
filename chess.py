import pygame
import pygame  # type: ignore
import os
import subprocess
import sys
from io import BytesIO


def check_and_install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name])


check_and_install_package("pygame")
check_and_install_package("subprocess")
check_and_install_package("sys")


pygame.init()

WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess Game')

font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

timer = pygame.time.Clock()
fps = 60

white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []

turn_step = 0
selection = 100
valid_moves = []


def load_and_scale(image_name, size):
    image = pygame.image.load(os.path.join("img", image_name))
    return pygame.transform.scale(image, size)


the_black_pieces = [
    load_and_scale("BlackQueen.png", (80, 80)),
    load_and_scale("BlackKing.png", (80, 80)),
    load_and_scale("BlackRook.png", (80, 80)),
    load_and_scale("BlackBishop.png", (80, 80)),
    load_and_scale("BlackKnight.png", (80, 80)),
    load_and_scale("BlackPawn.png", (65, 65))
]

the_black_pieces_small = [
    pygame.transform.scale(the_black_pieces[0], (45, 45)),
    pygame.transform.scale(the_black_pieces[1], (45, 45)),
    pygame.transform.scale(the_black_pieces[2], (45, 45)),
    pygame.transform.scale(the_black_pieces[3], (45, 45)),
    pygame.transform.scale(the_black_pieces[4], (45, 45)),
    pygame.transform.scale(the_black_pieces[5], (45, 45))
]

the_white_pieces = [
    load_and_scale("WhiteQueen.png", (80, 80)),
    load_and_scale("WhiteKing.png", (80, 80)),
    load_and_scale("WhiteRook.png", (80, 80)),
    load_and_scale("WhiteBishop.png", (80, 80)),
    load_and_scale("WhiteKnight.png", (80, 80)),
    load_and_scale("WhitePawn.png", (65, 65))
]

the_white_pieces_small = [
    pygame.transform.scale(the_white_pieces[0], (45, 45)),
    pygame.transform.scale(the_white_pieces[1], (45, 45)),
    pygame.transform.scale(the_white_pieces[2], (45, 45)),
    pygame.transform.scale(the_white_pieces[3], (45, 45)),
    pygame.transform.scale(the_white_pieces[4], (45, 45)),
    pygame.transform.scale(the_white_pieces[5], (45, 45))
]

black_queen = the_black_pieces[0]
black_queen_small = the_black_pieces_small[0]


black_king = the_black_pieces[1]
black_king_small = the_black_pieces_small[1]


black_rook = the_black_pieces[2]
black_rook_small = the_black_pieces_small[1]


black_bishop = the_black_pieces[3]
black_bishop_small = the_black_pieces_small[1]


black_knight = the_black_pieces[4]
black_knight_small = the_black_pieces_small[1]


black_pawn = the_black_pieces[5]
black_pawn_small = the_black_pieces_small[1]


white_queen = the_white_pieces[0]
white_queen_small = the_white_pieces_small[0]


white_king = the_white_pieces[1]
white_king_small = the_white_pieces_small[1]


white_rook = the_white_pieces[2]
white_rook_small = the_white_pieces_small[2]


white_bishop = the_white_pieces[3]
white_bishop_small = the_white_pieces_small[3]


white_knight = the_white_pieces[4]
white_knight_small = the_white_pieces_small[4]


white_pawn = the_white_pieces[5]
white_pawn_small = the_white_pieces_small[5]

white_images = [white_pawn, white_queen, white_king,
                white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king,
                black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small,
                      black_knight_small, black_rook_small, black_bishop_small]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

counter = 0
winner = ''
game_over = False


def draw_board():
    counterV1 = 0
    while counterV1 < 32:
        column = counterV1 % 4
        row = counterV1 // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [
                             600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [
                             700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(
            status_text[turn_step], True, 'black'), (20, 820))

        counterV2 = 0
        while counterV2 < 9:
            pygame.draw.line(screen, 'black', (0, 100 *
                             counterV2), (800, 100 * counterV2), 2)
            pygame.draw.line(screen, 'black', (100 * counterV2,
                             0), (100 * counterV2, 800), 2)
            counterV2 += 1

        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))
        counterV1 += 1

def draw_pieces():
    counterV1 = 0
    while counterV1 < (len(white_pieces)):
        index = piece_list.index(white_pieces[counterV1])
        if white_pieces[counterV1] == 'pawn':
            screen.blit(
                white_pawn, (white_locations[counterV1][0] * 100 + 22, white_locations[counterV1][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[counterV1]
                                              [0] * 100 + 10, white_locations[counterV1][1] * 100 + 10))
        if turn_step < 2:
            if selection == counterV1:
                pygame.draw.rect(screen, 'red', [white_locations[counterV1][0] * 100 + 1, white_locations[counterV1][1] * 100 + 1,
                                                 100, 100], 2)
        counterV1 += 1

    counterV2 = 0
    while counterV2 < (len(black_pieces)):
        index = piece_list.index(black_pieces[counterV2])
        if black_pieces[counterV2] == 'pawn':
            screen.blit(
                black_pawn, (black_locations[counterV2][0] * 100 + 22, black_locations[counterV2][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[counterV2]
                                              [0] * 100 + 10, black_locations[counterV2][1] * 100 + 10))
        if turn_step >= 2:
            if selection == counterV2:
                pygame.draw.rect(screen, 'blue', [black_locations[counterV2][0] * 100 + 1, black_locations[counterV2][1] * 100 + 1,
                                                  100, 100], 2)
        counterV2 += 1

#  check all pieces valid options on board


def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []

    counterV1 = 0
    while counterV1 < (len(pieces)):
        location = locations[counterV1]
        piece = pieces[counterV1]

        match piece:
            case  'pawn':
                moves_list = check_pawn(location, turn)
            case 'rook':
                moves_list = check_rook(location, turn)
            case  'knight':
                moves_list = check_knight(location, turn)
            case  'bishop':
                moves_list = check_bishop(location, turn)
            case  'queen':
                moves_list = check_queen(location, turn)
            case  'king':
                moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
        counterV1 += 1

    return all_moves_list

def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0),
               (-1, 1), (-1, -1), (0, 1), (0, -1)]
    counterV1 = 0
    while counterV1 < 8:
        target = (position[0] + targets[counterV1][0],
                  position[1] + targets[counterV1][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
        counterV1 += 1
    return moves_list


def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)

    counterV1 = 0
    while counterV1 < (len(second_list)):
        moves_list.append(second_list[counterV1])
        counterV1 += 1

    return moves_list

def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    counterv1 = 0
    while counterv1 < 4:
        path = True
        chain = 1
        match counterv1:
            case 0:
                x = 1
                y = -1
            case  1:
                x = -1
                y = -1
            case 2:
                x = 1
                y = 1
            case _:
                x = -1
                y = 1

        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
        counterv1 += 1
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    counterV1 = 0
    while counterV1 < 4:
        # down, up, right, left
        path = True
        chain = 1
        match counterV1:
            case  0:
                x = 0
                y = 1
            case  1:
                x = 0
                y = -1
            case  2:
                x = 1
                y = 0
            case _:
                x = -1
                y = 0

        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
        counterV1 += 1
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    # using a set makes the time complexity of o(1) when using the keyword "in"
    white_locations_local_copy = set(white_locations)
    # using a set makes the time complexity of o(1) when using the keyword "in"
    black_locations_local_copy = set(black_locations)

    # (position[0], position[1] + 1) not in black_locations_local_copy

    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations_local_copy and (position[0], position[1] + 1) not in black_locations_local_copy and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations_local_copy and (position[0], position[1] + 2) not in black_locations_local_copy and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations_local_copy:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations_local_copy:
            moves_list.append((position[0] - 1, position[1] + 1))
    elif color == 'black':
        if (position[0], position[1] - 1) not in white_locations_local_copy and (position[0], position[1] - 1) not in black_locations_local_copy and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations_local_copy and (position[0], position[1] - 2) not in black_locations_local_copy and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations_local_copy:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations_local_copy:
            moves_list.append((position[0] - 1, position[1] - 1))

    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        friends_list = white_locations
    else:
        friends_list = black_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

    counterV1 = 0
    while counterV1 < 8:
        target = (position[0] + targets[counterV1]
                  [0], position[1] + targets[counterV1][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
        counterV1 += 1
    return moves_list

# check valid knight moves


def check_knight(position, color):
    moves_list = []
    if color == 'white':
        friends_list = white_locations
    else:
        friends_list = black_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    counterV1 = 0

    while counterV1 < (8):
        target = (position[0] + targets[counterV1][0],
                  position[1] + targets[counterV1][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
        counterV1 += 1
    return moves_list

# check for valid moves for just selected piece


def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'

    counterV1 = 0
    while counterV1 < (len(moves)):
        pygame.draw.circle(
            screen, color, (moves[counterV1][0] * 100 + 50, moves[counterV1][1] * 100 + 50), 5)
        counterV1 += 1


# draw captured pieces on side of screen
def draw_captured():
    counterV1 = 0
    while counterV1 < len(captured_pieces_white):
        captured_piece = captured_pieces_white[counterV1]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * counterV1))
        counterV1 += 1

    counterV2 = 0
    while counterV2 < len(captured_pieces_black):
        captured_piece = captured_pieces_black[counterV2]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * counterV2))
        counterV2 += 1


# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]

            counterv1 = 0
            while counterv1 < len(black_options):
                if king_location in black_options[counterv1]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
                counterv1 += 1
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]

            counterv2 = 0
            while counterv2 < len(white_options):
                if king_location in white_options[counterv2]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)
                counterv2 += 1


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(
        f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!',
                            True, 'white'), (210, 240))


def doThis_action1():
    global game_over
    global winner
    global white_pieces
    global white_locations
    global black_pieces 
    global black_locations 
    global captured_pieces_white
    global captured_pieces_black
    global turn_step
    global selection
    global valid_moves
    global black_options
    global white_options

    game_over = False
    winner = ''
    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                       (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                       (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    captured_pieces_white = []
    captured_pieces_black = []
    turn_step = 0
    selection = 100
    valid_moves = []
    black_options = check_options(
        black_pieces, black_locations, 'black')
    white_options = check_options(
        white_pieces, white_locations, 'white')


def doThis_action2():
    global turn_step

    global game_over
    global winner
    global white_pieces
    global white_locations
    global black_pieces
    global black_locations

    global captured_pieces_white
    global captured_pieces_black
    global turn_step
    global selection
    global valid_moves
    global black_options
    global white_options

    x_coord = event.pos[0] // 100
    y_coord = event.pos[1] // 100
    click_coords = (x_coord, y_coord)
    if turn_step <= 1:
        if click_coords == (8, 8) or click_coords == (9, 8):
            winner = 'black'
        if click_coords in white_locations:
            selection = white_locations.index(click_coords)
            if turn_step == 0:
                turn_step = 1
        if click_coords in valid_moves and selection != 100:
            white_locations[selection] = click_coords
            if click_coords in black_locations:
                black_piece = black_locations.index(click_coords)
                captured_pieces_white.append(black_pieces[black_piece])
                if black_pieces[black_piece] == 'king':
                    winner = 'white'
                black_pieces.pop(black_piece)
                black_locations.pop(black_piece)
            black_options = check_options(
                black_pieces, black_locations, 'black')
            white_options = check_options(
                white_pieces, white_locations, 'white')
            turn_step = 2
            selection = 100
            valid_moves = []
    if turn_step > 1:
        if click_coords == (8, 8) or click_coords == (9, 8):
            winner = 'white'
        if click_coords in black_locations:
            selection = black_locations.index(click_coords)
            if turn_step == 2:
                turn_step = 3
        if click_coords in valid_moves and selection != 100:
            black_locations[selection] = click_coords
            if click_coords in white_locations:
                white_piece = white_locations.index(click_coords)
                captured_pieces_black.append(white_pieces[white_piece])
                if white_pieces[white_piece] == 'king':
                    winner = 'black'
                white_pieces.pop(white_piece)
                white_locations.pop(white_piece)
            black_options = check_options(
                black_pieces, black_locations, 'black')
            white_options = check_options(
                white_pieces, white_locations, 'white')
            turn_step = 0
            selection = 100
            valid_moves = []


# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            doThis_action2()

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                doThis_action1()

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()

pygame.quit()
