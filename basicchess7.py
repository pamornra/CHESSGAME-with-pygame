import pygame

pygame.init()
pygame.display.set_caption("CHESSGAME")
white = (225,225,225)
black = (0,0,0)
blue = (0,0,225)
red = (255,0,0)
darkgreen = (25,51,40)
Amber = (255,191,0)
yellow = (255,225,0)
screen_w = 900
screen_h = 640
screen = pygame.display.set_mode((screen_w,screen_h))
clock = pygame.time.Clock()
square_size = 80
game_started = False

font = pygame.font.Font("Font/Coiny.ttf",50)
start_text = font.render("START",True,white)
start_button = pygame.Rect(0,0,220,70)
start_button.center = (screen_w // 2, screen_h // 2)
start_rect = start_text.get_rect(center = start_button.center)
play_again_button = pygame.Rect(190, 330, 260, 70)
time_font = pygame.font.Font("Font/Coiny.ttf", 30)


white_king = pygame.image.load("chess/Chess · White King.png").convert_alpha()
white_king = pygame.transform.smoothscale(white_king, (60,60))
white_queen = pygame.image.load("chess/Chess · White Queen.png").convert_alpha()
white_queen = pygame.transform.smoothscale(white_queen, (60,60))
white_knight = pygame.image.load("chess/Chess · White Knight.png").convert_alpha()
white_knight = pygame.transform.smoothscale(white_knight, (60,60))
white_bishop = pygame.image.load("chess/Chess · White Bishop.png").convert_alpha()
white_bishop = pygame.transform.smoothscale(white_bishop, (60,60))
white_pawn = pygame.image.load("chess/Chess · White Pawn.png").convert_alpha()
white_pawn = pygame.transform.smoothscale(white_pawn, (60,60))
white_rook = pygame.image.load("chess/Chess · White Rook.png").convert_alpha()
white_rook = pygame.transform.smoothscale(white_rook, (60,60))
black_king = pygame.image.load("chess/Chess · Black King.png").convert_alpha()
black_king = pygame.transform.smoothscale(black_king, (60,60))
black_queen = pygame.image.load("chess/Chess · Black Queen.png").convert_alpha()
black_queen = pygame.transform.smoothscale(black_queen, (60,60))
black_knight = pygame.image.load("chess/Chess · Black Knight.png").convert_alpha()
black_knight = pygame.transform.smoothscale(black_knight, (60,60))
black_bishop = pygame.image.load("chess/Chess · Black Bishop.png").convert_alpha()
black_bishop = pygame.transform.smoothscale(black_bishop, (60,60))
black_pawn = pygame.image.load("chess/Chess · Black Pawn.png").convert_alpha()
black_pawn = pygame.transform.smoothscale(black_pawn, (60,60))
black_rook = pygame.image.load("chess/Chess · Black Rook.png").convert_alpha()
black_rook = pygame.transform.smoothscale(black_rook, (60,60))

board = [
    ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
    ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
    ["",  "",  "",  "",  "",  "",  "",  ""],
    ["",  "",  "",  "",  "",  "",  "",  ""],
    ["",  "",  "",  "",  "",  "",  "",  ""],
    ["",  "",  "",  "",  "",  "",  "",  ""],
    ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
    ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]]

starting_board = [
    ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
    ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
    ["",  "",  "",  "",  "",  "",  "", ""],
    ["",  "",  "",  "",  "",  "",  "", ""],
    ["",  "",  "",  "",  "",  "",  "", ""],
    ["",  "",  "",  "",  "",  "",  "", ""],
    ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
    ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]]
board = [row[:] for row in starting_board]

pieces = {"WK": white_king,"WQ": white_queen,"WR": white_rook,"WB": white_bishop,"WN": white_knight,"WP": white_pawn,
        "BK": black_king,"BQ": black_queen,"BR": black_rook,"BB": black_bishop,"BN": black_knight,"BP": black_pawn}

selected_row = -1
selected_col = -1
selected_piece = None
start_row = -1
start_col = -1
turn = "W"
timer_started = False
game_over = False
winner = ""
promotion = False
promotion_row = -1
promotion_col = -1
promotion_color = ""

def is_valid_pawn_move(board, start_row, start_col,clicked_row, clicked_col, turn):
    if turn == "W":
        direction = -1
        starting_row = 6
    else:
        direction = 1
        starting_row = 1
    row_diff = clicked_row - start_row
    col_diff = clicked_col - start_col
    target_piece = board[clicked_row][clicked_col]
    # เดิน 1 ช่อง
    if col_diff == 0 and row_diff == direction:
        if target_piece == "":
            return True
    # เดิน 2 ช่องครั้งแรก
    elif col_diff == 0 and row_diff == 2 * direction and start_row == starting_row:
        intermediate_row = start_row + direction

        if board[intermediate_row][start_col] == "" and target_piece == "":
            return True
    # กินทแยง
    elif abs(col_diff) == 1 and row_diff == direction:
        if target_piece != "" and target_piece[0] != turn:
            return True
    return False
    
def is_valid_knight_move(start_row, start_col, clicked_row, clicked_col):
    row_diff = abs(clicked_row - start_row)
    col_diff = abs(clicked_col - start_col)
    # เงื่อนไขรูปตัว L:
    if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
        return True  
    return False

def is_valid_bishop_move(board, start_row, start_col, clicked_row, clicked_col):
    #เช็คว่าเป็นแนวทแยงมุมหรือไม่
    row_diff = abs(clicked_row - start_row)
    col_diff = abs(clicked_col - start_col)
    if row_diff != col_diff:
        return False 
    #หาข้อกำหนดทิศทางการเดิน 
    row_step = 1 if clicked_row > start_row else -1
    col_step = 1 if clicked_col > start_col else -1
    #ตรวจสอบหมากขวางทางระหว่างทางเดิน
    current_row = start_row + row_step
    current_col = start_col + col_step
    while current_row != clicked_row and current_col != clicked_col:
        if board[current_row][current_col] != "":
            return False
        # ขยับไปช่องถัดไปในแนวทแยง
        current_row += row_step
        current_col += col_step
    return True

def is_valid_rook_move(board, start_row, start_col, clicked_row, clicked_col):
    #เช็คว่าเป็นการเดินแนวตรงหรือไม่
    if start_row != clicked_row and start_col != clicked_col:
        return False
    #หาข้อกำหนดทิศทางการเดิน
    if clicked_row == start_row:
        row_step = 0
    else:
        row_step = 1 if clicked_row > start_row else -1
    if clicked_col == start_col:
        col_step = 0
    else:
        col_step = 1 if clicked_col > start_col else -1
    #ตรวจสอบหมากขวางทางระหว่างทางเดิน
    current_row = start_row + row_step
    current_col = start_col + col_step

    while current_row != clicked_row or current_col != clicked_col:
        if board[current_row][current_col] != "":
            return False
        current_row += row_step
        current_col += col_step
    return True

def is_valid_queen_move(board, start_row, start_col, clicked_row, clicked_col):
    if is_valid_rook_move(board, start_row, start_col, clicked_row, clicked_col) or \
       is_valid_bishop_move(board, start_row, start_col, clicked_row, clicked_col):
        return True    
    return False

def is_valid_king_move(start_row, start_col, clicked_row, clicked_col):
    row_diff = abs(clicked_row - start_row)
    col_diff = abs(clicked_col - start_col)
    if row_diff <= 1 and col_diff <= 1:
        if not (row_diff == 0 and col_diff == 0):
            return True          
    return False

def is_square_attacked(board, target_row, target_col, attacker_color):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == "" or piece[0] != attacker_color:
                continue
            piece_type = piece[1]
            row_diff = target_row - row
            col_diff = target_col - col

            # Pawn
            if piece_type == "P":
                if attacker_color == "W":
                    direction = -1
                else:
                    direction = 1
                if row_diff == direction and abs(col_diff) == 1:
                    return True

            # Knight
            elif piece_type == "N":
                if (abs(row_diff), abs(col_diff)) in [(2, 1), (1, 2)]:
                    return True

            # King
            elif piece_type == "K":
                if max(abs(row_diff), abs(col_diff)) == 1:
                    return True

            # Bishop, Rook, Queen
            elif piece_type in ("B", "R", "Q"):
                diagonal = abs(row_diff) == abs(col_diff) and row_diff != 0
                straight = (row_diff == 0) != (col_diff == 0)

                if piece_type == "B" and not diagonal:
                    continue
                if piece_type == "R" and not straight:
                    continue
                if piece_type == "Q" and not (diagonal or straight):
                    continue
                step_row = 0 if row_diff == 0 else row_diff // abs(row_diff)
                step_col = 0 if col_diff == 0 else col_diff // abs(col_diff)
                check_row = row + step_row
                check_col = col + step_col
                blocked = False

                while (check_row, check_col) != (target_row, target_col):
                    if board[check_row][check_col] != "":
                        blocked = True
                        break

                    check_row += step_row
                    check_col += step_col

                if not blocked:
                    return True
    return False

def is_in_check(board, color):
    king = color + "K"
    king_row = -1
    king_col = -1
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                king_row = row
                king_col = col
                break
        if king_row != -1:
            break
    if king_row == -1:
        return False
    if color == "W":
        attacker_color = "B"
    else:
        attacker_color = "W"
    return is_square_attacked(board, king_row, king_col, attacker_color)
def is_in_checkmate(board, color):
    if not is_in_check(board, color):
        return False

    for start_row in range(8):
        for start_col in range(8):
            piece = board[start_row][start_col]
            if piece == "" or piece[0] != color:
                continue

            for clicked_row in range(8):
                for clicked_col in range(8):
                    if start_row == clicked_row and start_col == clicked_col:
                        continue

                    valid = False
                    moving_piece = piece
                    target_piece = board[clicked_row][clicked_col]

                    if target_piece != "" and target_piece[0] == color:
                        continue
                        
                    if moving_piece[1] == "P":
                        valid = is_valid_pawn_move(board, start_row, start_col, clicked_row, clicked_col, color)
                    elif moving_piece[1] == "N":
                        valid = is_valid_knight_move(start_row, start_col, clicked_row, clicked_col)
                    elif moving_piece[1] == "B":
                        valid = is_valid_bishop_move(board, start_row, start_col, clicked_row, clicked_col)
                    elif moving_piece[1] == "R":
                        valid = is_valid_rook_move(board, start_row, start_col, clicked_row, clicked_col)
                    elif moving_piece[1] == "Q":
                        valid = is_valid_queen_move(board, start_row, start_col, clicked_row, clicked_col)
                    elif moving_piece[1] == "K":
                        valid = is_valid_king_move(start_row, start_col, clicked_row, clicked_col)
                        
                    if valid:
                        temp_board = [r[:] for r in board]
                        temp_board[clicked_row][clicked_col] = moving_piece
                        temp_board[start_row][start_col] = ""
                        
                        if not is_in_check(temp_board, color):
                            return False 

    return True

possible_moves = []
captured_by_white = [] #หมากดำที่สีขาวกิน
captured_by_black = [] #หมากขาวที่สีดำกิน
running = True
white_time = 10*60
black_time = 10*60
last_time = pygame.time.get_ticks()
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

def draw_play_again_button():
    pygame.draw.rect(screen, Amber, play_again_button)

    button_font = pygame.font.Font("Font/Coiny.ttf", 30)

    text = button_font.render(
        "PLAY AGAIN",
        True,
        black
    )

    text_x = play_again_button.centerx - text.get_width() // 2
    text_y = play_again_button.centery - text.get_height() // 2

    screen.blit(text, (text_x, text_y))

promotion_buttons = [
    pygame.Rect(50,300,125,125),
    pygame.Rect(185,300,125,125),
    pygame.Rect(320,300,125,125),
    pygame.Rect(455,300,125,125)
]

while running:
    if timer_started and game_over == False:
        current_time = pygame.time.get_ticks()
        if current_time - last_time >= 1000:
            if turn == "W":
                white_time -= 1
            else:
                black_time -= 1
            last_time = current_time
            if white_time <= 0:
                white_time = 0
                game_over = True
                winner = "BLACK"
            elif black_time <= 0:
                black_time = 0
                game_over = True
                winner = "WHITE"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if promotion:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]

                if promotion_buttons[0].collidepoint(mouse_x, mouse_y):
                    if promotion_color == "W":
                        board[promotion_row][promotion_col] = "WQ"
                    else:
                        board[promotion_row][promotion_col] = "BQ"
                    promotion = False

                    if turn == "W":
                        turn = "B"
                    else:
                        turn = "W"
                    if is_in_checkmate(board,turn):
                        game_over = True
                        winner = "BLACK" if turn == "W" else"WHITE"

                elif promotion_buttons[1].collidepoint(mouse_x, mouse_y):
                    if promotion_color == "W":
                        board[promotion_row][promotion_col] = "WR"
                    else:
                        board[promotion_row][promotion_col] = "BR"
                    promotion = False

                    if turn == "W":
                        turn = "B"
                    else:
                        turn = "W"
                    if is_in_checkmate(board,turn):
                        game_over = True
                        winner = "BLACK" if turn == "W" else"WHITE"

                elif promotion_buttons[2].collidepoint(mouse_x, mouse_y):
                    if promotion_color == "W":
                        board[promotion_row][promotion_col] = "WB"
                    else:
                        board[promotion_row][promotion_col] = "BB"
                    promotion = False

                    if turn == "W":
                        turn = "B"
                    else:
                        turn = "W"
                    if is_in_checkmate(board,turn):
                        game_over = True
                        winner = "BLACK" if turn == "W" else"WHITE"
                elif promotion_buttons[3].collidepoint(mouse_x, mouse_y):
                    if promotion_color == "W":
                        board[promotion_row][promotion_col] = "WN"
                    else:
                        board[promotion_row][promotion_col] = "BN"
                    promotion = False

                    if turn == "W":
                        turn = "B"
                    else:
                        turn = "W"
                    if is_in_checkmate(board,turn):
                        game_over = True
                        winner = "BLACK" if turn == "W" else"WHITE"
            if game_over:
                if play_again_button.collidepoint(event.pos):
                    game_over = False
                    winner = ""
                    board = [row[:] for row in starting_board]
                    captured_by_white = []
                    captured_by_black = []
                    white_time = 10 * 60
                    black_time = 10 * 60
                    timer_started = False
                    last_time = pygame.time.get_ticks()
                    turn = "W"
                    selected_row = -1
                    selected_col = -1
                    selected_piece = None
                    start_row = -1
                    start_col = -1
                    possible_moves = []
                    print("PLAY AGAIN!")

            elif game_started == False:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    print("GAME STARTED!")

            else:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                if event.pos[0] >= 640 or event.pos[1] >= 640:
                    continue
                selected_col = mouse_x // square_size
                selected_row = mouse_y // square_size
                print(selected_row, ',', selected_col)
                if 0 <= selected_row < 8 and 0 <= selected_col < 8:
                    piece = board[selected_row][selected_col]
                    print(piece)

                if selected_piece is None:
                    if piece != "":
                        if piece[0] == turn:
                            selected_piece = piece
                            start_row = selected_row
                            start_col = selected_col
                            print("It's",turn,"turn") 
                            print("Selected piece:", selected_piece, "at" ,start_row, start_col)
                            if piece[1] == "P": #Pawn move with sq
                                if turn == "W":
                                    direction = -1
                                    starting_row = 6
                                else:
                                    direction = 1
                                    starting_row = 1
                                next_row = selected_row + direction
                                if 0 <= next_row < 8:
                                    if board[next_row][selected_col] == "":
                                        possible_moves.append((next_row, selected_col))   
                                next_row = selected_row +2* direction
                                if selected_row == starting_row:
                                    if 0 <= next_row < 8:
                                        if board[selected_row + direction][selected_col] == "":
                                            if board[next_row][selected_col] == "":
                                                possible_moves.append((next_row,selected_col))
                                next_row = selected_row + direction
                                next_col = selected_col - 1
                                if 0 <= next_row < 8 and 0 <= next_col < 8:
                                    if board[next_row][next_col] != "":
                                        if board[next_row][next_col][0] != turn:
                                            possible_moves.append((next_row,next_col))
                                next_col = selected_col + 1
                                if 0 <= next_row < 8 and 0 <= next_col <8:
                                    if board[next_row][next_col] != "":
                                        if board[next_row][next_col][0] != turn:
                                            possible_moves.append((next_row,next_col))

                            elif piece[1] == "N": #knight move with sq
                                knight_moves = [(-2, -1), (-2, 1),(-1, -2), (-1, 2),(1, -2), (1, 2),(2, -1), (2, 1)]
                                for row_change, col_change in knight_moves:
                                    next_row = selected_row + row_change
                                    next_col = selected_col + col_change
                                    if 0 <= next_row < 8 and 0 <= next_col < 8:
                                        target_piece = board[next_row][next_col]
                                        if target_piece == "" or target_piece[0] != turn:
                                            possible_moves.append((next_row, next_col))

                            elif piece[1] == "B": #Bishop move with sq
                                directions = [(-1,-1),(-1,1),(1,-1),(1,1)]
                                for row_change,col_change in directions:
                                    next_row = selected_row + row_change
                                    next_col = selected_col + col_change
                                    while 0 <= next_row < 8 and 0 <= next_col < 8:
                                        target_piece = board[next_row][next_col]
                                        if target_piece == "":
                                            possible_moves.append((next_row,next_col))
                                        else:
                                            if target_piece[0] != turn:
                                                possible_moves.append((next_row,next_col))
                                            break
                                        next_row += row_change
                                        next_col += col_change

                            elif piece[1] == "R": #Rook move with sq
                                directions = [(-1,0),(1,0),(0,-1),(0,1)]
                                for row_change , col_change in directions:
                                    next_row = selected_row + row_change
                                    next_col = selected_col + col_change
                                    while 0 <= next_row < 8 and 0 <= next_col < 8:
                                        target_piece = board[next_row][next_col]
                                        if target_piece == "":
                                            possible_moves.append((next_row,next_col))
                                        else:
                                            if target_piece[0] != turn:
                                                possible_moves.append((next_row,next_col))
                                            break
                                        next_row += row_change
                                        next_col += col_change

                            elif piece[1] == "Q": #Queen move with sq
                                directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
                                for row_change, col_change in directions:
                                    next_row = selected_row + row_change
                                    next_col = selected_col + col_change
                                    while 0 <= next_row < 8 and 0 <= next_col < 8:
                                        target_piece = board[next_row][next_col]
                                        if target_piece == "":
                                            possible_moves.append((next_row,next_col))
                                        else:
                                            if target_piece[0] != turn:
                                                possible_moves.append((next_row,next_col))
                                            break
                                        next_row += row_change
                                        next_col += col_change

                            elif piece[1] == "K":#King move with sq
                                directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
                                for row_change,col_change in directions:
                                    next_row = selected_row + row_change
                                    next_col = selected_col + col_change
                                    if 0 <= next_row < 8 and 0 <= next_col < 8:
                                        target_piece = board[next_row][next_col]
                                        if target_piece == "" or target_piece[0] != turn:
                                            possible_moves.append((next_row,next_col))
                            
                        else:
                            print("It's not your turn!")
                else:
                    if selected_row == start_row and selected_col == start_col:
                        selected_piece = None
                        start_row = -1
                        start_col = -1
                        selected_row = -1
                        selected_col = -1
                        possible_moves = []
                        print("cancled selection")
                    else:
                        moving_piece = selected_piece
                        target_piece = board[selected_row][selected_col]
                        if target_piece != "" and target_piece[0] == moving_piece[0]:
                            print("Can't move to that square")
                        
                        else:
                            if target_piece != "":
                                print("Captured piece:",target_piece)
                        
                            if moving_piece[1] == "P":
                                valid_move = is_valid_pawn_move(board, start_row, start_col, selected_row, selected_col, turn)
                            elif moving_piece[1] == "N":
                                valid_move = is_valid_knight_move(start_row, start_col, selected_row, selected_col)
                            elif moving_piece[1] == "B":
                                valid_move = is_valid_bishop_move(board, start_row, start_col, selected_row, selected_col)
                            elif moving_piece[1] == "R":
                                valid_move = is_valid_rook_move(board, start_row, start_col, selected_row, selected_col)
                            elif moving_piece[1] == "Q":
                                valid_move = is_valid_queen_move(board, start_row, start_col, selected_row, selected_col)
                            elif moving_piece[1] == "K":
                                valid_move = is_valid_king_move(start_row, start_col, selected_row, selected_col)
                            else:
                                valid_move = False

                            if valid_move:
                                if target_piece != "":
                                    if turn == "W":
                                        captured_by_white.append(target_piece)
                                    else:
                                        captured_by_black.append(target_piece)
                                board[selected_row][selected_col] = moving_piece
                                board[start_row][start_col] = ""
                                print("It's",turn,"move to",(selected_row, selected_col))
                                if turn == "W" and timer_started == False:
                                    timer_started = True
                                    last_time = pygame.time.get_ticks()
                                if moving_piece == "WP" and selected_row == 0:
                                    promotion = True
                                    promotion_row = selected_row
                                    promotion_col = selected_col
                                    promotion_color = "W"
                                elif moving_piece == "BP" and selected_row == 7:
                                    promotion = True
                                    promotion_row = selected_row
                                    promotion_col = selected_col
                                    promotion_color = "B"
                                possible_moves = []
                                selected_piece = None
                                start_row = -1
                                start_col = -1
                                if promotion == False:
                                    if turn == "W":
                                        turn = "B"
                                    else:
                                        turn = "W"
                                    if is_in_checkmate(board,turn):
                                        print("CHECKMATE!")
                                        game_over = True
                                        winner = "BLACK" if turn == "W" else "WHITE"
                                    elif is_in_check(board,turn):
                                        print("CHECK")
                            else:
                                print("Invalid move")     

    if game_started == False:
        screen.fill(darkgreen)
        pygame.draw.rect(screen, Amber, start_button,border_radius=12)
        screen.blit(start_text, start_rect)
    else:
        panel_x = 650
        panel_width = 250
        pygame.draw.rect(screen,darkgreen,(panel_x, 0, panel_width, screen_h))
        title_font = pygame.font.Font("Font/Coiny.ttf", 22)
        label_font = pygame.font.Font("Font/Coiny.ttf", 16)
        timer_font = pygame.font.Font("Font/Coiny.ttf", 24)

        for row in range(8):
            for col in range(8):
                x = col * square_size 
                y = row * square_size 
                if (row + col) % 2 == 0:
                    color = darkgreen
                else:
                    color = Amber
                pygame.draw.rect(screen,color,(x, y, square_size, square_size))

                if row < len(board) and col<len(board[row]):
                    piece = board[row][col]

                if piece != "":
                    piece_x = x + (square_size - 60) // 2
                    piece_y = y + (square_size - 60) // 2
                    screen.blit(pieces[piece], (piece_x, piece_y))

        title = title_font.render("GAME INFO",True,Amber)
        screen.blit(title, (panel_x + 55, 12))

        white_label = label_font.render("WHITE TIME:", True, white)
        screen.blit(white_label, (panel_x + 12, 50))
        white_time_text = timer_font.render(format_time(white_time),True,white)
        screen.blit(white_time_text,(panel_x + 12,72))

        black_label = label_font.render("BLACK TIME", True, white)
        screen.blit(black_label, (panel_x + 130, 50))
        black_time_text = timer_font.render(format_time(black_time), True, white)
        screen.blit(black_time_text, (panel_x + 130, 72))
        pygame.draw.line(screen, Amber, (panel_x + 10, 115),(screen_w - 10, 115),2)

        white_captured_label = label_font.render("White captured", True, white)
        screen.blit(white_captured_label, (panel_x + 12, 130))
        for i, piece in enumerate(captured_by_white):
            image = pygame.transform.smoothscale(pieces[piece], (35, 35))
            x = panel_x + 10 + (i % 5) * 46
            y = 160 + (i // 5) * 42
            screen.blit(image, (x, y))
        pygame.draw.line(screen,Amber,(panel_x + 10, 330), (screen_w - 10, 330), 2)

        black_captured_label = label_font.render("Black captured", True, white)
        screen.blit(black_captured_label, (panel_x + 12, 345))
        for i, piece in enumerate(captured_by_black):
            image = pygame.transform.smoothscale(pieces[piece], (35, 35))
            x = panel_x + 10 + (i % 5) * 46
            y = 375 + (i // 5) * 42
            screen.blit(image, (x, y))

        if promotion:
            overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            panel = pygame.Rect(35, 165, 570, 290)
            pygame.draw.rect(screen, darkgreen, panel, border_radius=18)
            pygame.draw.rect(screen, Amber, panel, 4, border_radius=18)

            title_font = pygame.font.Font("Font/Coiny.ttf", 32)
            title = title_font.render("PAWN PROMOTION", True, Amber)
            screen.blit(title, title.get_rect(center=(320, 205)))

            subtitle_font = pygame.font.Font("Font/Coiny.ttf", 18)
            subtitle = subtitle_font.render("Choose a piece",True, white)
            screen.blit(subtitle, subtitle.get_rect(center=(320, 250)))
            promotion_names = ["QUEEN", "ROOK", "BISHOP", "KNIGHT"]
            if promotion_color == "W":
                promotion_pieces = ["WQ", "WR", "WB", "WN"]
            else:
                promotion_pieces = ["BQ", "BR", "BB", "BN"]
            mouse_pos = pygame.mouse.get_pos()

            for i in range(4):
                button = promotion_buttons[i]
                if button.collidepoint(mouse_pos):
                    button_color = yellow
                else:
                    button_color = Amber
                pygame.draw.rect(screen, button_color, button, border_radius=12)
                pygame.draw.rect(screen, white, button, 2, border_radius=12)

                piece_image = pieces[promotion_pieces[i]]
                image_rect = piece_image.get_rect()
                image_rect.center = (button.centerx, button.y + 43)
                screen.blit(piece_image, image_rect)

                name_font = pygame.font.Font("Font/Coiny.ttf", 17)
                name_text = name_font.render(
                    promotion_names[i], True, black)
                name_rect = name_text.get_rect()
                name_rect.center = (button.centerx, button.y + 98)
                screen.blit(name_text, name_rect)

        if game_over:
            win_font = pygame.font.Font("Font/Coiny.ttf",50)
            winner_text = win_font.render(winner + " WINS!",True,yellow)
            box = pygame.Rect(120,230,400,180)
            pygame.draw.rect(screen,white,box)
            text_x = box.centerx - winner_text.get_width() // 2
            text_y = box.top + 20
            screen.blit(winner_text,(text_x,text_y))
            draw_play_again_button()

        if selected_row != -1 and selected_col != -1:
            x = selected_col * square_size 
            y = selected_row * square_size
            pygame.draw.rect(screen,red,(x, y, square_size, square_size),5)

        for row, col in possible_moves:
            x = col * square_size
            y = row * square_size
            pygame.draw.rect(screen,blue,(x, y, square_size, square_size),5)
    
    pygame.display.update()
    clock.tick(60)
pygame.quit()

