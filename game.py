class Game():
    def __init__(self,state) :
        self.state=state
        
    def gameOver(self,player):
        cpt=0
        add=0
        if player == 1 :
            for move in self.state.board_player1 :
                if self.state.board[move]==0:
                    cpt=cpt+1
            if cpt==6:
                for move in self.state.board_player2:
                    add=add+self.state.board[move]
                    self.state.board[move]=0
                self.state.board[2]=self.state.board[2]+add
                return True
            else : return False
        else :
            for move in self.state.board_player2 :
                if self.state.board[move]==0:
                    cpt=cpt+1
            if cpt==6:
                for move in self.state.board_player1:
                    add=add+self.state.board[move]
                    self.state.board[move]=0
                self.state.board[1]=self.state.board[1]+add
                return True
            else : return False

    def findWinner(self):
        if self.state.board[1] > self.state.board[2]:
            return 1
        else:
            return 2
    
    def evaluate(self,player):
        return self.state.board[player]-self.state.board[player]
    
    def evaluate1(self,player):
        h= self.evaluate(player)
        heur =0
        diff=0
        if player == 1:
            liste1=self.state.board_player1
            liste2=self.state.board_player2
        else:
            liste1=self.state.board_player2
            liste2=self.state.board_player1
            
        for i in range(6):
            diff = diff + self.state.board[liste2[i]]
            heur=heur + self.state.board[liste1[i]]
            
        h1= (heur - diff)*2+h
        
        return h1
    
    def evaluate2(self,player):
        heur=[]
        h1= self.evaluate1(player)
        h2=0
        heur.append(h1)
        
        if player == 1:
            moves=self.state.board_player1
        else:
            moves=self.state.board_player2
            moves.reverse()
            
        for x in moves:
            pos = 6 - moves.index(x)
            if self.state.board[x] == pos :
                h2=1
                break 
        
        return h2*3+h1
    
    def evaluate3(self,player):
        h3=0
        h2= self.evaluate2(player)
        nill_moves=[]
        if player == 1:
            moves=self.state.board_player1
        else:
            moves=self.state.board_player2
            moves.reverse()
        
        for x in moves:
            if self.state.board[x] == 0 :
                nill_moves.append(x)
        
        if len(nill_moves)!=0:
            nill_move=nill_moves[0]
            pos =moves.index(nill_move)
            j=pos
            for i in range(pos-1):
                j=pos-i
                if self.state.board[moves[i]] == j:
                    h3=self.state.frant[nill_move]
                    
        return h3*2+h2
                
