'''
Responsable of storing all the information about the current state of a chess game.
It's also responsible for determining if a move is valid or not.
It must have a move log.
'''
class GameState():
    def __init__(self):
        #board is an 8x8 dimensional list which has 2 characters
        #first character is the side of the board white and black
        #second character has the type of piece: 'Q','K','B','N','R','p'
        #"--" represents blank spaces
        self.board = [
            ["bR","bN","bB","bQ","bK","bR","bN","bB"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wR","wN","wB"]]
        self.white_to_move = True
        self.move_log = []
    
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move #swap players
        
        
        
        
        
                
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
    
    def get_chess_notation(self):
        #Can be change to real chess notation
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
    
    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
        