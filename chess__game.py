import chess
import pygame

pygame.init()
small_FONT=pygame.font.SysFont("arial",48)
piece_font=pygame.font.SysFont("segoeuisymbol",64)
screen=pygame.display.set_mode((640,680))
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
                        symbol=piece.unicode_symbol(invert_color=(piece.color==chess.WHITE))
                        x=col*SQUARE+SQUARE//2
                        y=row*SQUARE+SQUARE//2
                        if piece.color==chess.WHITE:
                              fill=(255,255,255)
                        else:
                              fill=(0,0,0)
                        outline=FONT_OUTLINE=(0,0,0)
                        for dx,dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                              shadow=piece_font.render(symbol,True,outline)
                              screen.blit(shadow,shadow.get_rect(center=(x+dx,y+dy)))
                        text=piece_font.render(symbol,True,fill)
                        screen.blit(text,text.get_rect(center=(x,y)))
def draw_flash():
      if flash_square is not None:
            if pygame.time.get_ticks()-flash_time<300:
                  col=chess.square_file(flash_square)
                  row=7-chess.square_rank(flash_square)
                  pygame.draw.rect(screen,(220,40,40),(col*SQUARE,row*SQUARE,SQUARE,SQUARE))
def draw_status():
      pygame.draw.rect(screen,(50,50,50),(0,640,640,40))
      if board.turn==chess.WHITE:
            message="WHITE'S Move"
      else:
            message="Black's move"
      if board.is_check():
            message=message+"-Check"
      text=small_FONT.render(message,True,(255,255,255))
      screen.blit(text,(10,648))
def selected_piece():
      if selected is not None:
            col=chess.square_file(selected)
            row=7-chess.square_rank(selected)
            pygame.draw.rect(screen,(246,246,105),(col*SQUARE,row*SQUARE,SQUARE,SQUARE),5)
board=chess.Board()
running=True
selected=None
flash_square=None
flash_time=0

while running and not board.is_game_over():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
              x,y=event.pos
              if y<640:
                    
                  col=x//SQUARE
                  row=y//SQUARE
                  square=chess.square(col,7-row)

              if selected is None:
                    piece=board.piece_at(square)
                    if piece is not None and piece.color==board.turn:
                          selected=square
              else:
                    move=chess.Move(selected,square)
                    if move in board.legal_moves:
                          board.push(move)
                    elif square!=selected:
                          flash_square=square
                          flash_time=pygame.time.get_ticks()
                    selected=None
              

    draw_board()
    draw_piece()
    selected_piece()
    draw_status()
    draw_flash()
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


