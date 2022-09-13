'''
Main driver file. Responsable for user input and displaying the current state of the GameState object.
YT reference playlist : https://youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_
Current video count: 7
Left in: near the end
'''

import pygame as p
import ChessEngine

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global directory of images. So to call only once in main
'''
def load_images():
    pieces = ['bB',"bK",'bN','bp','bQ','bR','wB',"wK",'wN','wp','wQ','wR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('Chess/images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
    #We can access an image by saying IMAGES["wp"]

'''
The main driver for our code. Handles user input and updating the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    #flag variable for when a move is made
    move_made = False
    load_images()
    running = True
    #no square is selected. Meant to hold the tuple of the last click event
    sq_selected = ()
    #keep track of player clicks (two tuples [(6,4),(4,4)])
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                #(x, y) location of mouse
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE #(x)
                row = location[1]//SQ_SIZE #(y)
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row,col)
                    #append for 1st to 2sd clicks
                    player_clicks.append(sq_selected)
                    #print("position {sel[0]} {sel[1]}".format(sel = sq_selected))
                #after second click
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        #reset user clicks
                        sq_selected = ()
                        player_clicks = []
                    #this allows to select other piece while selecting the first piece
                    else:
                        player_clicks = [sq_selected]
            #this hanndles keys
            elif e.type == p.KEYDOWN:
                    #when pressing z
                    if e.key == p.K_z:
                        gs.undo_move()
                        move_made = True
        if move_made == True:
            valid_moves = gs.get_valid_moves()
            move_made = False
        draw_game_state(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsable of all the graphics
'''

def draw_game_state(screen, gs):
    # draw squares
    draw_board(screen)
    #highlight may be here.
    #draw images on top of the squares
    draw_pieces(screen, gs.board)

'''
Draw the squares on the board
'''
def draw_board(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(( r + c ) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


'''
Draw the pieces on the board using the current GameState.board
'''
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))






if __name__ == "__main__":
    main()





















