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
        