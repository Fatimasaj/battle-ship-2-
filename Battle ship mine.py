from random import randint

SIZE = 10
SHIPSYMBOL = "@#&$%" #Carrier, Battleship, Cruiser, Submarine, Destroyer
SHIPLENGTH = [5,4,3,3,2]

def printBoard(board):
    #print header
    print("  ",end="")
    for i in range(SIZE):
        print(chr(i+65)+" ",end="")
    print()
    
    for i in range(SIZE):
        print(chr(i+48)+" ",end="")
        for j in range(SIZE):
            print(board[10*i+j],end=" ")
        print(""+chr(i+48))

    print("  ",end="")
    for i in range(SIZE):
        print(chr(i+65)+" ",end="")
    print()

def convertToIndex(choice):
    return int(choice[1])*SIZE+(ord(choice[0])-65)
def convertToCoord(choice):
    return chr(choice%10+65)+str(choice//10)
def convertToShipH(choice):
    return SHIPSYMBOL.index(choice)

def placeShip(x, y, o, size, board, symbol):
    if(size == 0):
        return True
    t = (y+o*(size-1))*SIZE+(x+(size-1)*(1-o))
    if( t<0 or t>=SIZE*SIZE or (o==0 and size>1 and (t-1)%SIZE > t%SIZE)):
        return False
    if(board[t]=="·" and placeShip(x,y,o,size-1,board,symbol)):
        board[t] = symbol
        return True
    return False

def randPlaceShip(board):
    for i in range(5):
        while(True):
            x = randint(0,SIZE-1)
            y = randint(0,SIZE-1)
            o = randint(0,1)
            if(placeShip(x,y,o,SHIPLENGTH[i],board, SHIPSYMBOL[i])):
                break

def getValidInput(board):
    while(True):
        user = input("Enter a position to test: ").upper()
        if(len(user)==2):
            if("A"<=user[0] and user[0]<="J" and "0"<=user[1] and user[1]<="9"):
                t = convertToIndex(user)
                if(board[t]=="·"):
                    return t
                else:
                    print("...that position has already been tested\n")
            else:
                print("...coordinates out of bounds\n")
        else:
            print("...invalid inputs\n")
            
def compChoose(board, last):
    while(True):
        t = randint(0,SIZE*SIZE-1)
        if(board[t]=="·"):
            return t

def isHit(board, target):
    return board[target] in SHIPSYMBOL
    
comp = ["·"]*(SIZE**2)
compMove = ["·"]*(SIZE**2)
compShipHealth = [x for x in SHIPLENGTH]
compShips = 5
cp = -1
randPlaceShip(comp)

mine = ["·"]*(SIZE**2)
mineMove = ["·"]*(SIZE**2)
mineShipHealth = [x for x in SHIPLENGTH]
mineShips = 5
my = -1
randPlaceShip(mine)

while(True):
    print(" "*7 + "OPPONENT"+"\t\tships sunk: "+str(5-compShips))
    printBoard(mineMove)
    print()
    printBoard(mine)
    print(" "*9 + "MINE"+"\t\tships left: "+str(mineShips))
    print()

    printBoard(comp)
    
    #code for my move
    my = getValidInput(mineMove)
    if isHit(comp, my):
        ship = convertToShipH(comp[my])
        print("...that was a HIT!")
        mineMove[my] = "X"
        comp[my] = "X" 
        compShipHealth[ship]-=1
        if compShipHealth[ship] == 0:
            compShips -= 1
            if compShips == 0: 
                print("YOU HAVE WON THE GAME!")
                input()
                print("Computers board:")
                printBoard(comp)
                exit() 
            else:
                 print("you have sunk one of the computers ships!")
        
            
    else:
        print("...splash")
        mineMove[my] = " "
        comp[my] = " "
        print()
        
    input()
    
    #code for computer move
    cp = compChoose(comp,cp)
    print("The computer has chosen: ",convertToCoord(cp))
    if isHit(mine, cp):
        ship = convertToShipH(mine[cp])
        print("...HIT!")
        compMove[cp] = "X"
        mineShipHealth[ship] -= 1
        if mineShipHealth[ship] == 0:
            print("Computer has sunk your ship!")
            mineShips -= 1
        mine[cp] = "X" 
        
    else:
        print("...miss")
        compMove[cp] = " " 
        mine[cp] = " " 
        print()
        
        if mineShips == 0:
            print("You Lost")
            printBoard(mine)
            exit() 
