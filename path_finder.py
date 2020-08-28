import pygame
import math
from queue import PriorityQueue

width = 1000
win= pygame.display.set_mode((width,width))
pygame.display.set_caption("the coolest thing I've ever made")

red= (255, 0, 0)
green= (0, 255, 0)
blue= (0, 255, 0)
yellow= (255, 255, 0)
white= (255,255,255)
black= (0, 0, 0)
purple = (129,0,120)
orange= (255, 165 ,0)
grey= (128, 128, 128)
turquoise= (64, 224, 208)

class Node:
    def __init__(self,row,col,width,total_rows):
        self.row=row
        self.col=col
        self.x=row*width
        self.y=col*width
        self.colour=white
        self.neighbour=[]
        self.width=width
        self.total_rows=total_rows

    def get_pos(self):
        return self.row,self.col
    def is_closed(self):
        return self.colour==red
    def is_open(self):
        return self.colour==green
    def is_barrier(self):
        return self.colour==black
    def is_start(self):
        return self.colour==orange
    def is_end(self):
        return self.colour==purple
    def reset(self):
        self.colour=white
    def make_open(self):
        self.colour=green
    def make_closed(self):
        self.colour=red
    def make_barrier(self):
        self.colour=black
    def make_end(self):
        self.colour=purple
    def make_start(self):
        self.colour=orange
    def make_path(self):
        self.colour=turquoise
    def draw(self,win):
        pygame.draw.rect(win,self.colour,(self.x,self.y,self.width,self.width))
    def update_neighbour(self,grid):
        self.neighbour=[]
        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbour.append(grid[self.row+1][self.col])
            
        if self.row>0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbour.append(grid[self.row-1][self.col])

        if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbour.append(grid[self.row][self.col+1])

        if self.col>0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbour.append(grid[self.row][self.col-1])
            
        
    def __lt__(self,other):
        return False

def h(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2) + abs (y1-y2)
def reconstruct_path(came_from,end,draw,current):
    while current in came_from:
        current=came_from[current]
        current.make_path()
        draw()
    
def algorithm(draw,grid,start,end):
    count=0
    open_set=PriorityQueue()
    open_set.put((0,count,start))
    came_from={}
    g_score={node: float('inf') for row in grid for node in row}
    g_score[start]=0
    f_score={node: float('inf') for row in grid for node in row}
    f_score[start]=h(start.get_pos(),end.get_pos())

    open_set_hash={start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                
        current=open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from,end,draw,current)
        for neighbou in current.neighbour:
            temp_g_score=g_score[current]+1
            if temp_g_score<g_score[neighbou]:
                came_from[neighbou]=current
                g_score[neighbou]= temp_g_score
                f_score[neighbou]=temp_g_score + h(neighbou.get_pos(),end.get_pos())
                if neighbou not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbou],count,neighbou))
                    open_set_hash.add(neighbou)
                    neighbou.make_open()
        draw()
        if current!=start:
            current.make_closed()
    return False

def make_grid(rows,width):
    grid=[]
    gap=width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node=Node(i,j,gap,rows)
            grid[i].append(node)
    return grid

def draw_grid(win,rows,width):
    gap=width//rows
    for i in range(rows):
        pygame.draw.line(win,grey,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,grey,(j*gap,0),(j*gap,width))


def draw(win,grid,rows,width):
    win.fill(white)

    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked(pos,rows,width):
    gap=width//rows
    y,x=pos
    row=y//gap
    col=x//gap
    return row,col

def main(win,width):
    rows=50
    grid=make_grid(rows,width)

    start=None
    end=None
    run=True
    started=False
    while run:
        draw(win,grid,rows,width)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked(pos,rows,width)
                node=grid[row][col]
                if not start and node!=end:
                    start=node
                    start.make_start()
                elif not end and node!=start:
                    end=node
                    end.make_end()
                elif node !=end and node !=start:
                    node.make_barrier()
                    
            elif pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked(pos,rows,width)
                node=grid[row][col]
                node.reset()
                if node==start:
                    start=None
                elif node==end:
                    node=None
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbour(grid)

                    algorithm(lambda:draw(win,grid,rows,width),grid,start,end)
    
        
main(win,width)














        
    
