'''
Main driver file. Responsable for user input and displaying the current state of the GameState object.
'''

import pygame as p
import ChessEngine

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = ()

'''
Initialize a global directory of images. So to call only once in main
'''
def load_images():
    pieces = ['bB',"bK",'bN','bp','bQ','bR','wB',"wK",'wN','wp','wQ','wR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE,SQ_SIZE))
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
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        
        clock.tick(MAX_FPS)
        p.display.flip()
        
'''
Responsable of all the graphics
'''

def drawGameState(screen, gs):
    draw_board(screen) # draw squares
    #highlight may be here.
    draw_pieces(screen, gs.board) #draw images on top of the squares


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
    pass
    
    
    
    
    
    
    
    
    
    
    

if __name__ == "__main__":    
    main()





















