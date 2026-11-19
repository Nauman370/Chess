import chess
import pygame

pygame.init()
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

board=chess.Board()
running=True
while running and not board.is_game_over():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    draw_board()
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


