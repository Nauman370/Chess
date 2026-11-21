import chess
import pygame

pygame.init()
small_FONT=pygame.font.SysFont("arial",48)
info=pygame.display.Info()
screen=pygame.display.set_mode((info.current_w-100,info.current_h-120),pygame.RESIZABLE)
pygame.display.set_caption("Chess")
status_H=50
def new_layout():
      global screen,WIDTH,HEIGHT,SQUARE,BOARD,OFFSET_X,piece_font,BOARD_SIZE
      screen=pygame.display.get_surface()
      WIDTH,HEIGHT=screen.get_size()
      SQUARE=min(HEIGHT-status_H,WIDTH)//8
      BOARD_SIZE=SQUARE*8
      OFFSET_X=(WIDTH-BOARD_SIZE)//2
      piece_font=pygame.font.SysFont("segoeuisymbol",int(SQUARE*0.8))




new_layout()

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
PROMOTION_PIECES={
      "q":chess.QUEEN,
      "r":chess.ROOK,
      "n":chess.KNIGHT,
      "b":chess.BISHOP
}

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

      if pending_promotion is True:
            message="Q to queen,R to rook,B to bishop,N for knight"
      elif board.is_checkmate():

            pygame.draw.rect(screen,(50,50,50),(0,BOARD_SIZE,WIDTH,HEIGHT-BOARD_SIZE))
      if board.is_checkmate():

            if board.turn==chess.WHITE:
                  message="Black won,checkmate"
            else:
                  message="White won,checkmate"
      elif board.is_game_over():
            message= "Draw"
      else:
            if board.turn==chess.WHITE:
                  message="White's Move"
            else:
                  message="Black's Move"
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
pending_promotion=None
flash_square=None
flash_time=0

def piece_promotion(from_sq,to_sq,letter):
      if letter in PROMOTION_PIECES:
            return chess.Move(from_sq,to_sq,promotion=PROMOTION_PIECES[letter])
      return None


while running:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
              running=False  
        if event.type==pygame.VIDEORESIZE:
              new_layout()
        if event.type==pygame.KEYDOWN and pending_promotion is not None:
              letter=pygame.key.name(event.key)
              move=piece_promotion(pending_promotion[0],pending_promotion[1],letter)
              if move is not None and move in  board.legal_moves:
                    board.push(move)
                    pending_promotion=None
        if event.type==pygame.MOUSEBUTTONDOWN:
              x,y=event.pos
              if pending_promotion  is None  and not board.is_game_over() and y<BOARD_SIZE and OFFSET_X<=x<OFFSET_X+BOARD_SIZE:

                    
                  col=(x-OFFSET_X)//SQUARE
                  row=y//SQUARE
                  square=chess.square(col,7-row)


                  if selected is None:
                    piece=board.piece_at(square)
                    if piece is not None and piece.color==board.turn:
                          selected=square
                  else: 
                    moving_piece=board.piece_at(selected)
                    is_promotion=(moving_piece.piece_type==chess.PAWN and chess.square_rank(square) in (0,7))
                    if is_promotion and chess.Move(selected,square,promotion=chess.QUEEN) in board.legal_moves:
                          pending_promotion=(selected,square)
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
