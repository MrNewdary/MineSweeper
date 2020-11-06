import pygame
import math
import time
import random
pygame.init()

sizeX = 30
sizeY = 16
size = sizeX * sizeY
mines = 99
square_size = 30
border_size = 2
mine_locations = []
mine_locations_coord =[]
Circles =[]
flagged = []
amount_flagged = 0
game_position = 0
background_colour = (255, 255, 255)
screenwidth = square_size*sizeX + 200
screenheight = square_size*sizeY + 200
win = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Minesweeper')
win.fill(background_colour)

while len(mine_locations) < mines:
    i = random.randint(0, size-1)
    if i not in mine_locations:
        mine_locations.append(i)

for i in range(len(mine_locations)):
    x_coord = mine_locations[i] % sizeX
    y_coord = math.floor(mine_locations[i] / sizeX)
    mine_locations_coord.append((x_coord, y_coord))

class button():
    def __init__(self, color, x, y, width, height, text='', text_colour=(0, 0, 0)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.visible = False
        self.flagged = False
        self.text_colour = text_colour

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - border_size, self.y - border_size, self.width + 2*border_size, self.height + 2*border_size), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', square_size)
            text = font.render(self.text, 1, self.text_colour)
            win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2), self.y + (self.height // 2 - text.get_height() // 2)))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False



class Circle():
    def __init__(self, colour, x, y, radius):
        self.colour = colour
        self.x = x
        self.y = y
        self.radius = radius
    def draw(self):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)



def convert_to_index(x,y):
    return(x+(y*sizeX))

def inbounds(x,y):
    if x>=0 and x < sizeX and y >=0 and y < sizeY:
        return True

def count_adjacent(x, y):
    count = 0
    for (a,b) in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1, 1), (-1,-1)]:
         if ((x+a),(y+b)) in mine_locations_coord:
            count +=1
    return(count)

def search(x, y):
    if not inbounds(x, y):
        return

    if Buttons[convert_to_index(x,y)].visible:
        return
    if Buttons[convert_to_index(x,y)].flagged:
        return
    if (x,y) in mine_locations_coord:
        GameLost()
        return

    Buttons[convert_to_index(x,y)].visible = True
    Buttons[convert_to_index(x,y)].color = (150,150,150)

    count = count_adjacent(x,y)
    if count > 0:
        Buttons[convert_to_index(x,y)].text = str(count)
        if count == 1:
            Buttons[convert_to_index(x, y)].text_colour = (0,0,255)
        elif count == 2:
            Buttons[convert_to_index(x, y)].text_colour = (27, 132, 27)
        elif count == 3:
            Buttons[convert_to_index(x, y)].text_colour = (255, 0, 0)
        elif count == 4:
            Buttons[convert_to_index(x, y)].text_colour = (1, 0, 128)
        elif count == 5:
            Buttons[convert_to_index(x, y)].text_colour = (128, 1, 1)
        elif count == 6:
            Buttons[convert_to_index(x, y)].text_colour = (0, 128, 131)
        elif count == 7:
            Buttons[convert_to_index(x, y)].text_colour = (0, 0, 0)
        elif count == 8:
            Buttons[convert_to_index(x, y)].text_colour = (128, 128, 128)

        return

    for (a, b) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        search(x+a,y+b)

def flag(x,y):
    global amount_flagged
    if Buttons[convert_to_index(x, y)].visible == True:
        return
    if amount_flagged >= mines and Buttons[convert_to_index(x, y)].flagged == False:
        return
    if Buttons[convert_to_index(x, y)].flagged == True:
        Circles.pop(flagged.index((x, y)))
        flagged.pop(flagged.index((x, y)))
        Buttons[convert_to_index(x, y)].flagged = False
        amount_flagged -=1
        show_text(((screenwidth-square_size*sizeX)//2)//2-20, ((screenheight-square_size*sizeY)//2)//2, 50, (255, 0, 0), (255, 255, 255), str(mines-len(Circles)) + "   ")
    else:
        Buttons[convert_to_index(x, y)].flagged = True
        flagged.append((x, y))
        Circles.append(Circle((0, 0, 0), square_size * (x) + (screenwidth - square_size * sizeX) // 2 + square_size // 2,square_size * y + (screenheight - square_size * sizeY) // 2 + square_size // 2, 10))
        amount_flagged += 1
        show_text(((screenwidth-square_size*sizeX)//2)//2-20, ((screenheight-square_size*sizeY)//2)//2, 50, (255, 0, 0), (255, 255, 255), str(mines-len(Circles)) + "   ")
    if set(flagged) == set(mine_locations_coord):
        GameWon()

def show_text(x,y,font_size,font_colour,background_colour,text, font = 'comicsans'):
    font = pygame.font.SysFont(font, font_size)
    textsurface = font.render(text, 1, font_colour, background_colour)
    win.blit(textsurface, (x, y))

tileimg = pygame.image.load("flag.jpg")
tile_resize = pygame.transform.scale(tileimg, (square_size, square_size))
win.blit(tile_resize, (5, ((screenheight-square_size*sizeY)//2)//2))
show_text(((screenwidth-square_size*sizeX)//2)//2-20, ((screenheight-square_size*sizeY)//2)//2, 50, (255, 0, 0), (255, 255, 255), str(mines-len(Circles)) + "   ")

def GameWon():
    global game_position
    game_position = 1
    show_text(screenwidth // 2 - 110, (screenwidth - square_size * sizeX) // 2 - 70, 50, (255, 0, 0), (255, 255, 255),"GAME WON")

def GameLost():
    global game_position
    game_position = -1
    show_text(screenwidth//2-110,(screenwidth-square_size*sizeX)//2-70, 50, (255,0,0), (255,255,255), "GAME OVER")

def redrawWindow():
    for i in range(size):
        Buttons[i].draw(win, (136,136,136))
        if i in mine_locations:
            Buttons[i].color = (189, 189, 189)
    for i in range(len(Circles)):
        Circles[i].draw()
    if game_position == -1:
        for i in range(mines):
            Buttons[mine_locations[i]].color = (255, 0, 0)

run = True
Buttons = [button((189, 189, 189), square_size * (i % sizeX) + (screenwidth-square_size*sizeX)//2, square_size * (math.floor(i/sizeX)) + (screenheight-square_size*sizeY)//2, square_size-border_size, square_size-border_size) for i in range(size)]

while run:
    redrawWindow()
    pygame.display.update()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_position == 0:
                if event.button == 1:
                    for i in range(size):
                        if Buttons[i].isOver(pos):
                            x_coord = i % sizeX
                            y_coord = math.floor(i/sizeX)
                            count = count_adjacent(x_coord,y_coord)
                            #print(f"Clicked Button at ({str(x_coord)},{str(y_coord)})")
                            if not Buttons[i].flagged:
                                search(x_coord,y_coord)

                elif event.button == 3:
                    for i in range(size):
                        if Buttons[i].isOver(pos):
                            x_coord = i % sizeX
                            y_coord = math.floor(i / sizeX)
                            flag(x_coord,y_coord)

