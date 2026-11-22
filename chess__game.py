import chess
import pygame
import chess.engine

pygame.init()
small_FONT=pygame.font.SysFont("arial",30)
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
      t=current_theme()
      for row in range(8):
            for col in range(8):
                  if (row+col)%2==0:
                        color=t["light"]
                  else:
                        color=t["dark"]
                  pygame.draw.rect(screen,color,(OFFSET_X +col*SQUARE,row*SQUARE,SQUARE,SQUARE))
PROMOTION_PIECES={
      "q":chess.QUEEN,
      "r":chess.ROOK,
      "n":chess.KNIGHT,
      "b":chess.BISHOP
}
PIECE_VALUE={
      chess.PAWN:1,
      chess.ROOK:5, 
      chess.QUEEN:9,
      chess.KNIGHT:3,
      chess.BISHOP:3,
      chess.KING:0
}
THEMES={
      "Classic":{"light":(240,217,181),"dark":(181,136,99),
                 "white":(255,255,255),"white_edge":(0,0,0),
                 "black":(90,90,90),"black_edge":(255,255,255)},
      "Green":{"light":(238,238,210),"dark":(118,150,86),
               "white":(255,255,255),"white_edge":(0,0,0),
               "black":(40,40,40),"black_edge":(255,255,255)},
      "Blue":{"light":(222,227,230),"dark":(140,162,173),
              "white":(255,255,255),"white_edge":(20,30,60),
              "black":(35,50,90),"black_edge":(230,240,255)},
      "Night":{"light":(120,120,140),"dark":(60,60,80),
               "white":(240,240,255),"white_edge":(0,0,0),
               "black":(20,20,30),"black_edge":(200,200,230)},
}
themes_name=list(THEMES)
theme_index=0

def current_theme():
      return THEMES[themes_name[theme_index]]
      
def draw_piece():
      t=current_theme()
      for row in range(8):
            for col in range(8):
                  square=chess.square(col,7-row)
                  piece=board.piece_at(square)

                  if piece is not None:
                        symbol=piece.unicode_symbol(invert_color=(piece.color==chess.WHITE))
                        x=OFFSET_X+col*SQUARE+SQUARE//2
                        y=row*SQUARE+SQUARE//2
                        if piece.color==chess.WHITE:
                              fill=t["white"]
                              outline=t["white_edge"]
                        else:
                              fill=t["black"]
                              outline=t["black_edge"]
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
def confirm_screen():
      if confirm_switch:
            overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            overlay.fill((0,0,0,170))
            screen.blit(overlay,(0,0))
            if bot_mode:

                  new_mode="2 players"
            else:
                  new_mode="Bot mode"

            lines=["Switch to"+ new_mode+"?","C=continue","R= Restart","C= Cancel"]
            for i, line in enumerate(lines):
                  text=small_FONT.render(line,True,(255,255,255))
                  screen.blit(text,text.get_rect(center=(WIDTH//2,HEIGHT//2-90+i*60)))


def draw_status():
      pygame.draw.rect(screen,(50,50,50),(0,BOARD_SIZE,WIDTH,HEIGHT-BOARD_SIZE))

      if pending_promotion is not None:
            message="Q to queen,R to rook,B to bishop,N for knight"
      elif board.is_checkmate():
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
      score=evaluate(board)
      if score>0:
            score_message="+"+str(score)
      else:
            score_message=str(score)
      score_text=small_FONT.render("Score:"+score_message,True,(255,255,255))
      screen.blit(score_text,score_text.get_rect(topright=(undo_button().left-20,BOARD_SIZE+12)))
      pygame.draw.rect(screen,(90,90,90),undo_button())
      label=small_FONT.render("Undo",True,(255,255,255))
      screen.blit(label,label.get_rect(center=undo_button().center))
      if bot_mode:
            mode_message="[Bot mode]"
      else:
            mode_message="[2 player]"
      text=small_FONT.render(message+mode_message,True,(255,255,255))
      screen.blit(text,(OFFSET_X,BOARD_SIZE+12))
def  do_undo():
      global selected
      if not confirm_switch and (not bot_mode or board.turn==chess.WHITE) and pending_promotion is None and len(board.move_stack)>0:
            board.pop()
            if bot_mode and not confirm_switch and board.turn==chess.BLACK and len(board.move_stack)>0:
                  board.pop()
            selected=None
def undo_button():
      return pygame.Rect(OFFSET_X+BOARD_SIZE-120,BOARD_SIZE+5,120,40)
def switch_mode(restart):
      global bot_mode,bot_wait,selected,pending_promotion,confirm_switch,board
      bot_mode=not bot_mode
      if restart:
            board=chess.Board()
      bot_wait=None
      selected=None
      pending_promotion=None
      confirm_switch=False

def draw_legal_moves():
      if selected is not None:
            for move in board.legal_moves:
                  if move.from_square==selected:

                        col=chess.square_file(move.to_square)
                        row=7-chess.square_rank(move.to_square)
                        cx=OFFSET_X+col*SQUARE+SQUARE//2
                        cy=row*SQUARE+SQUARE//2
                        if board.piece_at(move.to_square)is not None:
                              pygame.draw.circle(screen,(220,40,40),(cx,cy),SQUARE//2-4,5)
                        else:
                              pygame.draw.circle(screen,(70,70,70),(cx,cy),SQUARE//6)
                        

def selected_piece():
      if selected is not None:
            col=chess.square_file(selected)
            row=7-chess.square_rank(selected)
            pygame.draw.rect(screen,(246,246,105),(OFFSET_X+col*SQUARE , row*SQUARE,SQUARE,SQUARE),5)

def evaluate(b):
      score=0
      for square in chess.SQUARES:
            piece=b.piece_at(square)
            if piece is not None:
                  value=PIECE_VALUE[piece.piece_type]
                  if piece.color==chess.WHITE:
                        score=score+value
                  else:
                        score=score-value
      return score

board=chess.Board()
engine=chess.engine.SimpleEngine.popen_uci(r"stockfish.exe")
engine.configure({"Skill Level":5})
print (evaluate(board))
running=True
selected=None
pending_promotion=None
flash_square=None
flash_time=0
bot_wait=None
bot_mode=True
confirm_switch=False

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
        if event.type==pygame.KEYDOWN and event.key==pygame.K_u:
              do_undo()
        if event.type==pygame.KEYDOWN and event.key==pygame.K_m and pending_promotion is  None:
              confirm_switch=not confirm_switch
        if event.type==pygame.KEYDOWN and confirm_switch:
              if event.key==pygame.K_c:
                    switch_mode(False)
              elif event.key==pygame.K_r:
                    switch_mode(True)
        

        if event.type==pygame.VIDEORESIZE:
              new_layout()
        if event.type==pygame.KEYDOWN and pending_promotion is not None:
              letter=pygame.key.name(event.key)
              move=piece_promotion(pending_promotion[0],pending_promotion[1],letter)
              if move is not None and move in  board.legal_moves:
                    board.push(move)
                    pending_promotion=None
        if event.type==pygame.KEYDOWN and event.key==pygame.K_t:
              theme_index=(theme_index+1)%len(themes_name)
        if event.type==pygame.MOUSEBUTTONDOWN:
              x,y=event.pos
              if undo_button().collidepoint(event.pos):
                    do_undo()
              if (not  bot_mode or board.turn==chess.WHITE) and pending_promotion  is None  and not board.is_game_over() and y<BOARD_SIZE and OFFSET_X<=x<OFFSET_X+BOARD_SIZE:

                    
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
    if bot_mode and board.turn==chess.BLACK and not board.is_game_over() and pending_promotion is None:
          if bot_wait is None:
                bot_wait=pygame.time.get_ticks()
          elif pygame.time.get_ticks()-bot_wait>500:
               result=engine.play(board,chess.engine.Limit(time=0.1))
               board.push(result.move)
               bot_wait=None
    else:
          bot_wait=None
                
    screen.fill((30,30,30))
    draw_board()
    draw_piece()
    draw_legal_moves()
    selected_piece()
    draw_status()
    draw_flash()
    confirm_screen()
    pygame.display.flip()
pygame.quit()
engine.quit()
