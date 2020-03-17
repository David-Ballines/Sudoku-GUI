import pygame, sys, json 

pygame.init()

#edit to start a different game
BOARDS = [
    [8, 9, 2, 0, 0, 3, 0, 1, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 6, 8, 0, 7, 0],
    [4, 5, 0, 0, 8, 0, 0, 0, 1],
    [0, 0, 8, 0, 0, 0, 2, 0, 0],
    [1, 0, 3, 7, 0, 0, 5, 0, 0],
    [0, 7, 1, 0, 0, 6, 0, 5, 0],
    [5, 0, 9, 2, 0, 0, 0, 8, 0],
    [6, 0, 0, 0, 0, 7, 0, 0, 9]
    ]

margin = 20
side = 50
width = margin*2 + side*9
height = margin*2 + side*9
window = pygame.display.set_mode((width,height + 100))

colors = [(255,255,255), (255,0,0),(0,255,0),(0,0,0),(200,200,200),(0,0,255)]

fnt = pygame.font.SysFont("comicsans", 40, bold = False, italic = False)

#makes an object to hold the board and game state, also uses the 
#backtracking algorithm to solve the sudoku puzzle
class sudokuGame(object):
    def __init__(self):
        self.original = []
        self.puzzle = []
        self.ans = []
        self.gameOver = False
        for i in range(9):
            self.original.append([])
            self.puzzle.append([])
            self.ans.append([])
            for j in range(9):
                self.puzzle[i].append(BOARDS[i][j])
                self.ans[i].append(BOARDS[i][j])
                self.original[i].append(BOARDS[i][j])
        self.solving(self.ans)
    
    def start(self):
        self.gameOver = False
        for i in range(9):
            for j in range(9):
                self.puzzle[i][j] = self.puzzle[i][j]

    def solving(self,board):
        current = self.findSpot(board)
        if not current:
            return True
        else:
            row,col = current
        for i in range(1,10):
            if(self.check(board,(row,col),i)):
                board[row][col] = i
                if(self.solving(board)):
                    return True
                board[row][col] = 0
        return False

    def check(self,board,place,number):
        for i in range(9):
            #check row
            if(board[place[0]][i] == number and i != place[1]):
                return False

            #check col
            if(board[i][place[1]] == number and i != place[0]):
                return False

        #check box
        bx = place[1]//3
        by = place[0]//3

        for i in range(by*3,by*3+3):
            for j in range(bx*3,bx*3+3):
                if(board[i][j] == number and (i,j) != place):
                    return False
        return True

    def findSpot(self,board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return(i,j)

#creates a button object to be used with pygame
class button():
    def __init__(self,color,x,y,width,height, text = ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,window,outline = None):
        if outline:
            pygame.draw.rect(window, outline,
                            (self.x - 2, self.y - 2, self.width + 4, self.height + 4,0))
        pygame.draw.rect(window, self.color,
                        (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont("comicsans",20)
            text = font.render(self.text,1,(0,0,0))
            window.blit(text,
                        (self.x + (self.width/2 - text.get_width()/2),
                        self.y + (self.height/2 - text.get_height()/2)))            
    
    def isOver(self,pos):
        if(pos[0] > self.x and pos[0] < self.x +self.width):
            if(pos[1] > self.y and pos[1] < self.y + self.height):
                return True
        return False

#class that is able to draw all the necessary parts for the GUI
class SudokuUI():
    def __init__(self,Window,game):
        self.game = game
        self.wind = Window
        self.row = -1
        self.col = -1
        self.__initUI()

    def __initUI(self):
        pygame.display.set_caption("Sudoku")

        self.restartButton = button(colors[4],170,500,50,30,"Restart")
        self.hintButton = button(colors[4],120,500,40,30,"Hint")
        self.solveButton = button(colors[4],230,500,40,30,"Solve")

        self.draw()

    def __drawGrid(self):
        for i in range(10):
            if i % 3 == 0:
                color = colors[3]
            else:
                color = colors[4]

            x0 = margin + i*side
            y0 = margin
            x1 = margin + i*side
            y1 = height - margin
            pygame.draw.line(self.wind,color,(x0,y0), (x1,y1))

            x0 = margin
            y0 = margin + i*side
            x1 = width - margin
            y1 = margin + i*side
            pygame.draw.line(self.wind,color, (x0,y0), (x1,y1))

    def __drawPuzzle(self):
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = margin + j*side + side/2
                    y = margin + i*side + side/2
                    original = self.game.original[i][j]
                    if answer == original:
                        color = colors[3]
                    elif(answer != self.game.ans[i][j]):
                        color = colors[1]
                    else:
                        color = colors[5]
                    txt = fnt.render(str(answer),1,color)
                    self.wind.blit(txt,(x,y))

    def cellClicked(self,event):
        x,y = event[0], event[1]
        if(margin < x < width - margin and margin < y < height - margin):
            row, col = (y - margin) // side, (x - margin) // side

            if((row,col) == (self.row,self.col)):
                self.row,self.col = -1,-1
            elif(self.game.original[row][col] == 0):
                self.row, self.col = row,col
        self.draw()

    def __drawCursor(self):
        if(self.row >= 0 and self.col >= 0):
            x0 = margin + self.col*side + 1
            y0 = margin + self.row*side + 1
            x1 = margin + (self.col + 1)*side - 1
            y1 = margin + (self.row + 1)*side - 1

            pygame.draw.line(self.wind, colors[1],(x0,y0),(x0,y1))
            pygame.draw.line(self.wind, colors[1],(x0,y0),(x1,y0))
            pygame.draw.line(self.wind, colors[1],(x0,y1),(x1,y1))
            pygame.draw.line(self.wind, colors[1],(x1,y0),(x1,y1))

            pygame.display.update()

    def solve(self):
        current = self.game.findSpot(self.game.puzzle)
        if not current:
            return True
        else:
            row,col = current
        for i in range(1,10):
            if(self.game.check(self.game.puzzle,(row,col),i)):
                self.game.puzzle[row][col] = i
                self.row,self.col = current[0],current[1]
                self.draw()
                pygame.time.delay(50)
                pygame.display.update()
                if(self.solve()):
                    return True
                self.game.puzzle[row][col] = 0
        return False

    def hint(self):
        if(self.row < 0 or self.col < 0):
            return
        self.game.puzzle[self.row][self.col] = self.game.ans[self.row][self.col]
        self.col, self.row = -1,-1
        self.draw()

    def restart(self):
        for i in range(9):
            for j in range(9):
                self.game.puzzle[i][j] = self.game.original[i][j]
        self.draw()

    def draw(self):
        self.wind.fill(colors[0])
        self.__drawGrid()
        self.__drawPuzzle()
        self.__drawCursor()
        self.restartButton.draw(self.wind)
        self.hintButton.draw(self.wind)
        self.solveButton.draw(self.wind)




if __name__ == '__main__':
    game = sudokuGame()
    game.start()
    graphics = SudokuUI(window,game)
    while True:
        position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(graphics.restartButton.isOver(position)):
                    graphics.restart()
                if(graphics.hintButton.isOver(position)):
                    graphics.hint()
                if(graphics.solveButton.isOver(position)):
                    graphics.solve()
                graphics.cellClicked(position)
            if(event.type == pygame.KEYDOWN):
                if(event.unicode in "123456789" and (graphics.col,graphics.row) != (-1,-1)):
                    game.puzzle[graphics.row][graphics.col] = int(event.unicode)
                    graphics.draw()
        pygame.display.update()
