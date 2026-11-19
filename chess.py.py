import chess
import pygame

pygame.init()
screen=pygame.display.set_mode(640,640)
pygame.display.set_caption("Chess")


board=chess.Board()
running=True
while running and not board.is_game_over():
    print()
    print(board)
    print()


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


