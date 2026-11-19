import chess
import pygame

pygame.init()
FONT=pygame.font.SysFont("arial",48)
screen=pygame.display.set_mode((640,640))
pygame.display.set_caption("Chess")


SQUARE=80
LIGHT=(240,217,181)
DARK=(181,136,99)
def draw_board():
      for row in range(8):
            for col in range(8):
                  if (row+col)%2==0:
                        color=LIGHT
                  else:
                        color=DARK
                  pygame.draw.rect(screen,color,(col*SQUARE,row*SQUARE,SQUARE,SQUARE))

def draw_piece():
      for row in range(8):
            for col in range(8):
                  square=chess.square(col,7-row)
                  piece=board.piece_at(square)

                  if piece is not None:
                        if piece.color==chess.WHITE:
                              color=(0,0,220)
                        else:
                              color=(0,0,0)
                        text=FONT.render(piece.symbol().upper(),True,color)
                        x=col*SQUARE+SQUARE//2
                        y=row*SQUARE+SQUARE//2
                        screen.blit(text,text.get_rect(center=(x,y)))
board=chess.Board()
running=True
while running and not board.is_game_over():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    draw_board()
    draw_piece()
    pygame.display.flip()
pygame.quit()


if board.turn==chess.WHITE:
        print("White's Move")
else:
        print("Black's Move")

move=input("Last move:")

try:
        board.push_san(move)
except(ValueError):
        print("Illegal move")

print()
print(board)
print()

result=board.result()


if result=="1-0" and board.is_checkmate() is True :
    print("White won","Checkmate")
elif result=="0-1" and board.is_checkmate() is True:
    print("Black won","Checkmate")
elif board.is_stalemate() is True:

    print("Stalemate")


