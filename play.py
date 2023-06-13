import pygame
from game import Game
import mancalaBoard
from time import sleep
import sys
from copy import deepcopy


class Play():
    def computer1(self,game):
        didbestmove,move=game.state.bestmove(game,1)
        if didbestmove == 0:
            bestValue, bestPit = self.MinMax(game, 1, 5, 1)
            n=game.state.board[bestPit]
            player,plusgain=game.state.doMove(bestPit,1)
            update(game,bestPit,n,1,plusgain)
            return player
        else : # we did best move so now computer will play for another round
            update(game,move,4,1,0)
            self.computer1(game)
    
    def computer2(self,game):
        didbestmove,move=game.state.bestmove(game,2)
        if didbestmove == 0:
            bestValue, bestPit = self.MinMax(game, 1, 5, 2)
            n=game.state.board[bestPit]
            player,plusgain=game.state.doMove(bestPit, 2)
            update(game,bestPit,n,2,plusgain)
            return player
        else : # we did best move so now computer will play for another round
            update(game,move,4,2,0)
            self.computer2(game)

    def MinMax(self,game,player,depth,playerSide):
        #Initially depth == 5
        if game.gameOver(playerSide) or depth==1:
            if player ==1:
                bestValue = game.evaluate(playerSide)
            else:
                bestValue = game.evaluate3(playerSide)
                
            bestPit = None
            if player == -1:
                bestValue = - bestValue
            return bestValue, bestPit
        bestValue = -99999
        bestPit = None
        for pit in game.state.possibleMoves(playerSide):
            child_game = deepcopy(game)
            nextplayer=child_game.state.doMove(pit,playerSide)
            if playerSide==1 :
                value, _ = self.MinMax (child_game, -player, depth-1, 2)
            else :
                value, _ = self.MinMax (child_game, -player, depth-1, 1)
            value = - value
            if value > bestValue:
                bestValue = value
                bestPit =pit
        return bestValue, bestPit


fosses_position=[(370, 400),(480, 400),(590, 400),(710, 400),(820, 400),(930, 400),(370, 250),(480, 250),(590, 250),(710, 250),(820, 250),(930, 250)]
magazins=[(1000, 200, 100,250),(200, 200, 100,250)]

grey = (150, 150, 150)  
white = (255, 255, 255) 
yellow = (200, 200, 0)  
red = (200,0,0) 
black = (0, 0, 0) 
blue = (50,50,160)
brown = (121, 96, 76)
brownlight = (171, 149, 132)

display_width = 1300
display_height = 650
radius = 20 # node size

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))

def get_font(size): 
    return pygame.font.SysFont('segoeuisymbol',size,italic=False,bold=True)

def printdata(data,position,size=20,color=black) :
    font = get_font(size)
    text= font.render(data,True, (color))
    textrect = text.get_rect(center=position)
    screen.blit(text, textrect)


def result (computer1score, computer2score, winner) :
    screen.fill(white) 
    printdata("Computer 1 score ",(325, 150),50,yellow)
    pygame.draw.circle(screen, grey, (325, 250), 50)
    printdata(str(computer1score),(325, 250),50,red)
    
    printdata("Computer 2 score ",(975, 150),50,yellow)
    pygame.draw.circle(screen, grey, (975, 250), 50)
    printdata(str(computer2score),(975, 250),50,red)

    pygame.draw.rect(screen, grey ,(300, 400, 700,100) )
    printdata(winner+" is the winner",(650, 450),50,red)

    while True:
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def get_graine_pos(nb,fosse_pos) : 
    if nb<3 : graine_pos=(fosse_pos[0]-25+nb*22,fosse_pos[1]-25)
    if 3<=nb<7 : graine_pos=(fosse_pos[0]-30+(nb-3)*22,fosse_pos[1]-3)
    if 7<=nb<10 : graine_pos=(fosse_pos[0]-25+(nb-7)*22,fosse_pos[1]+19)
    if 10<=nb<13 : graine_pos=(fosse_pos[0]-20+(nb-10)*22,fosse_pos[1]-20)
    if 13<=nb<17 : graine_pos=(fosse_pos[0]-25+(nb-13)*224,fosse_pos[1]+2)
    if 17<=nb<20 : graine_pos=(fosse_pos[0]-20+(nb-17)*22,fosse_pos[1]+24)
    return graine_pos

def mancala_board():
    screen.fill(white) 
    printdata("Mancala",(640, 50),100,brown)
    pygame.draw.rect(screen, brownlight,(150, 150, 1000,350) )

    for magasin in magazins :
        pygame.draw.rect(screen, brown,magasin )

    for position in fosses_position :
        pygame.draw.circle(screen, brown, position, (50))

    printdata("computer1",(1050, 475), 30,brown)
    printdata("computer2",(250, 475),30,brown)

def display (game) :
    mancala_board()    
    for fosse in game.state.board_player1 :
        for nb in range(game.state.board[fosse]) :
            pos=game.state.fosse_positions[fosse]
            pygame.draw.circle(screen, red, get_graine_pos(nb,pos), (10))
    for fosse in game.state.board_player2 :
        for nb in range(game.state.board[fosse]) :
            pos=game.state.fosse_positions[fosse]
            pygame.draw.circle(screen, red, get_graine_pos(nb,pos), (10))
    printdata(str(game.state.board[1]),(1050, 325),50,red)
    printdata(str(game.state.board[2]),(250, 325),50,red)
    pygame.display.update()
    sleep(4)

def update (game,move,n,player,plusgain) :
    if player==1:
            other=2
            playermagazin=(1000, 200, 100,250)
            playerscorepos=(1050, 325)
    else:
            other=1
            playermagazin=(200, 200, 100,250)
            playerscorepos=(250, 325)
    pos=game.state.fosse_positions[move]
    next=move  
    pygame.draw.circle(screen, blue, pos, 55, width=5)
    pygame.display.update()
    sleep(1)
    for nb in range(n) :
        next=game.state.next_case[next]
        pygame.draw.circle(screen, brown, get_graine_pos(nb,pos), (10))
        if(n>10 and nb<10):
            for i in range (10,n) :
                pygame.draw.circle(screen, blue, get_graine_pos(i,pos), (10))
        pygame.display.update()
        sleep(1)
        if(next==player) :
            pygame.draw.rect(screen, brown,playermagazin)
            printdata(str(game.state.board[player]),playerscorepos,50,red)
        else :
            if(next==other or next==move) :
                next=game.state.next_case[next]
            posnext=game.state.fosse_positions[next]
            nbnext=game.state.board[next]-1
            if(nbnext==-1):
                nbnext=nbnext+1
            if(nbnext<10):
                pygame.draw.circle(screen, red, get_graine_pos(nbnext,posnext), (10))
            else :
                pygame.draw.circle(screen, blue, get_graine_pos(nbnext,posnext), (10))
        
        pygame.display.update()
        sleep(1)
    if plusgain==1 : #the last move was empty
        posfrant=game.state.fosse_positions[game.state.frant[next]]
        pygame.draw.circle(screen, yellow, posnext, 55, width=5)
        pygame.draw.circle(screen, yellow, posfrant, 55, width=5)
        pygame.display.update()
        sleep(2)
        pygame.draw.circle(screen, brown, posnext, 50)
        pygame.draw.circle(screen, brown, posfrant, 50)
        #update score
        pygame.draw.rect(screen, brown,playermagazin)
        printdata(str(game.state.board[player]),playerscorepos,50,red)
        pygame.draw.circle(screen, brownlight, posnext, 55, width=5)
        pygame.draw.circle(screen, brownlight, posfrant, 55, width=5)
    pygame.draw.circle(screen, brownlight, pos, 55, width=5)
    pygame.display.update()
    sleep(2)

def startplay():


        mancalaboard=mancalaBoard.Mancalaboard(mancalaBoard.initial_board)
        game=Game(mancalaboard)
        play=Play()
        player=1
        display (game)
        while(not game.gameOver(player)):
            if(player==1):
                player=play.computer1(game)     
            else :
                player=play.computer2(game)  
                
        display (game)

        if(game.findWinner() == 1):
            winner="Computer 1"
        else :
            winner="Computer 2"
        computer1score=game.state.board[1]
        computer2score=game.state.board[2]
        result(computer1score, computer2score, winner)