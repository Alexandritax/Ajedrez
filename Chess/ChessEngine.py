class GameState():

    """
    Responsable of storing all the information about the current state of a chess game.
    It's also responsible for determining if a move is valid or not.
    It must have a move log.
    """
    def __init__(self):
        #board is an 8x8 dimensional list which has 2 characters
        #first character is the side of the board white and black
        #second character has the type of piece: 'Q','K','B','N','R','p'
        #"--" represents blank spaces
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.move_functions = {'p': self.get_pawn_moves,'R':self.get_rook_moves,'N':self.get_knight_moves,
                               'B':self.get_bishop_moves,'Q':self.get_queen_moves,'K':self.get_king_moves}

        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)
        #naive approcach
        # self.check_mate = False
        # self.stale_mate = False
        #advanced approach
        self.in_check = False
        self.pins = []
        self.checks = []

    '''
    Takes a move as a parameter and executes it (does not work for castling, promotion or en-passant)
    '''
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        #swap players
        self.white_to_move = not self.white_to_move
        #updating the piece location
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row,move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row,move.end_col)


    '''
    Undoing last movement
    '''
    def undo_move(self):
        # a move is necessary to execute this
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            #switch players
            self.white_to_move = not self.white_to_move

    '''
    All moves considering checks see naive approach for a simpler explanation. This one is an advanced one
    '''
    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.checks_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_all_moves()
                #to blick a check you must have a piece into one of the square between the enemy piece and king
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                #squares pieces can move to
                valid_squares = []
                #if knight, must capture knight or move the king
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1,8):
                        #check 2 and 3 are the directions
                        valid_square = (king_row + check[2]*i, king_col + check[3]*i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                #get rid of any moves that don't block the check or move king
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].piece_moved[1] != 'K':
                        if (moves[i].end_row, moves[i].end_col) not in valid_squares:
                            moves.remove(moves[i])
                #double check
            else:
                self.get_king_moves(king_row,king_col,moves)
        else:
            moves = self.get_all_moves()
        return moves

    def checks_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        #check outward for king for pins and checks, keep tacks of pins abd checksum
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1,8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1]
                        # 5. possiblilites
                        # when the enemy piece is orthogonally away and it's a rook
                        # when the enemy piece is diagonally away and it's a bishop
                        # 1 square away diagonally from the king and it's a pawn
                        # any direction when it's a queen
                        # any direction within 1 square and it's a king
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and \
                                ((enemy_color == 'w' and 6 <= j <= 7) or \
                                (enemy_color == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row,end_col,d[0],d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
        #checks for knight moves
        knight_moves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(2,-1),(2,1),(1,-2),(1,2))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_row + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0],m[1]))
        return in_check, pins, checks

    '''
    All moves wihtout considering checks
    '''
    def get_all_moves(self):
        moves = []
        #we go through the board
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece_color = self.board[r][c][0]
                if (piece_color == 'w' and self.white_to_move) or (piece_color == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r,c,moves)
        return moves

    '''Get all the pawn moves for the pawn at the r and c adding this to the list'''

    def get_pawn_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2],self.pins[i][3])
                self.pins.remove((self.pins[i]))
                break

        if self.white_to_move:
            if self.board[r-1][c] == '--':
                if not piece_pinned or pin_direction == (-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r==6 and self.board[r-2][c] == '--':
                        moves.append(Move((r,c),(r-2,c),self.board))

            #captures
            #captures to the left
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b' and not piece_pinned or pin_direction == (-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self.board))
            #captures to the right
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b' and not piece_pinned or pin_direction == (-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self.board))
        else:
            if self.board[r+1][c] == '--':
                if not piece_pinned or pin_direction == (1,0):
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r==1 and self.board[r+2][c] == '--':
                        moves.append(Move((r,c),(r+2,c),self.board))

            #captures
            #captures to the left
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w' and not piece_pinned or pin_direction == (1,-1):
                        moves.append(Move((r,c),(r+1,c-1),self.board))
            #captures to the right
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w' and not piece_pinned or pin_direction == (1,1):
                        moves.append(Move((r,c),(r+1,c+1),self.board))

    '''Get all the rook moves for the pawn at the r and c adding this to the list'''

    def get_rook_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove((self.pins[i]))
                break

        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                #on board
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction ==d or pin_direction == (-d[0],-d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--':
                            moves.append(Move((r,c),(end_row,end_col),self.board))
                        #enemy piece valid
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r,c),(end_row,end_col),self.board))
                            break
                        #friendly piece
                        else:
                            break
                #off boarder
                else:
                    break

    '''Get all the knight moves for the pawn at the r and c adding this to the list'''

    def get_knight_moves(self, r, c, moves):
        piece_pinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove((self.pins[i]))
                break

        directions = ((-2,-1),(-2,1),(-1,-2),(-1,2),(2,-1),(2,1),(1,-2),(1,2))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            #on board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    #enemy piece valid
                    if (end_piece[0] == enemy_color) or (end_piece == "--"):
                        moves.append(Move((r,c),(end_row,end_col),self.board))

    '''Get all the bishop moves for the pawn at the r and c adding this to the list'''

    def get_bishop_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove((self.pins[i]))
                break

        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                #on board
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction ==d or pin_direction == (-d[0],-d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--':
                            moves.append(Move((r,c),(end_row,end_col),self.board))
                        #enemy piece valid
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r,c),(end_row,end_col),self.board))
                            break
                        #friendly piece
                        else:
                            break
                #off boarder
                else:
                    break
    '''Get all the queen moves for the pawn at the r and c adding this to the list'''

    def get_queen_moves(self, r, c, moves):
        self.move_functions['R'](r,c,moves)
        self.move_functions['B'](r,c,moves)
    '''Get all the king moves for the pawn at the r and c adding this to the list'''

    def get_king_moves(self, r, c, moves):

        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            #on board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color or end_piece =='--':
                    if enemy_color == 'b':
                        self.white_king_location = (end_row,end_col)
                    else:
                        self.black_king_location = (end_row,end_col)
                    in_check, pins, checks = self.checks_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((r,c),(end_row,end_col), self.board))
                    if enemy_color == 'b':
                        self.white_king_location = (r,c)
                    else:
                        self.black_king_location = (r,c)

class Move():

    # maps keys to values

    # key : value

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3,
                     "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4,
                     "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        #print(self.move_id)

    '''
    Overriding the equal method
    '''
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        #Can be change to real chess notation
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]