import chess
import pygame

pygame.init()
small_FONT=pygame.font.SysFont("arial",48)
screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("Chess")
WIDTH,HEIGHT=screen.get_size()
STATUS_H=50
SQUARE=(HEIGHT-STATUS_H)//8
BOARD_SIZE=(SQUARE*8)
OFFSET_X=(WIDTH-BOARD_SIZE)//2
piece_font=pygame.font.SysFont("segoeuisymbol",int(SQUARE*0.8))

LIGHT=(240,217,181)
DARK=(181,136,99)
screen.fill((30,30,30))
def draw_board():
      for row in range(8):
            for col in range(8):
                  if (row+col)%2==0:
                        color=LIGHT
                  else:
                        color=DARK
                  pygame.draw.rect(screen,color,(OFFSET_X +col*SQUARE,row*SQUARE,SQUARE,SQUARE))

def draw_piece():
      for row in range(8):
            for col in range(8):
                  square=chess.square(col,7-row)
                  piece=board.piece_at(square)

                  if piece is not None:
                        symbol=piece.unicode_symbol(invert_color=(piece.color==chess.WHITE))
                        x=OFFSET_X+col*SQUARE+SQUARE//2
                        y=row*SQUARE+SQUARE//2
                        if piece.color==chess.WHITE:
                              fill=(255,255,255)
                        else:
                              fill=(0,0,0)
                        outline=(0,0,0)
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
                  pygame.draw.rect(screen,(220,40,40),(OFFSET_X+col*SQUARE,row*SQUARE,SQUARE,SQUARE))
def draw_status():
      pygame.draw.rect(screen,(50,50,50),(0,BOARD_SIZE,WIDTH,HEIGHT-BOARD_SIZE))
      if board.turn==chess.WHITE:
            message="WHITE'S Move"
      else:
            message="Black's move"
      if board.is_check():
            message=message+"-Check"
      text=small_FONT.render(message,True,(255,255,255))
      screen.blit(text,(OFFSET_X,BOARD_SIZE+12))
def selected_piece():
      if selected is not None:
            col=chess.square_file(selected)
            row=7-chess.square_rank(selected)
            pygame.draw.rect(screen,(246,246,105),(OFFSET_X+col*SQUARE , row*SQUARE,SQUARE,SQUARE),5)
board=chess.Board()
running=True
selected=None
flash_square=None
flash_time=0

while running and not board.is_game_over():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
              running=False  
        if event.type==pygame.MOUSEBUTTONDOWN:
              x,y=event.pos
              if y<BOARD_SIZE and OFFSET_X<=x<OFFSET_X+BOARD_SIZE:

                    
                  col=(x-OFFSET_X)//SQUARE
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
    screen.fill((30,30,30))
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
