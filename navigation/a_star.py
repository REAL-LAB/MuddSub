from queue import PriorityQueue
import random

def decision(probability):
    return random.random() < probability

infinity = float('inf')
class Node(object):

    def __init__(self, x, y, end):
        self.isOpen = False 
        self.isClosed = False
        self.isObstacle = False
        self.x = x
        self.y = y
        self.f = infinity
        self.h = 0
        self.string = "."
        if(end != None):
            self.h = ((end.x - self.x)**2 + (end.y - self.y)**2)**0.5
        self.g = infinity
        self.parent = None 
    
    def __lt__(self, other):
        return self.f < other.f
    def __gt__(self, other):
        return self.f > other.f
    def __str__(self):
        
        if(self.isObstacle):  return "1"
        return self.string
        
    

def makeGrid(width, height, prob, start_x, start_y, end_x, end_y):
    endNode = Node(end_x,end_y, None)
    grid = []
    for i in range(width):
        arr = []
        for j in range(height):
            node = Node(i,j,endNode)
            if(decision(prob) and (i != start_x or j != start_y)):
                node.isObstacle = True
            arr.append(node)
        grid.append(arr)
    grid[end_x][end_y] = endNode
    
    return grid


def solveGrid(grid, start_x, start_y, end_x, end_y):
    q = PriorityQueue()
    grid[start_x][start_y].isOpen = True 
    grid[start_x][start_y].g = 0
    grid[start_x][start_y].f = grid[start_x][start_y].h + grid[start_x][start_y].g
    #q_finished = PriorityQueue()
    #put starting node node in the queue
    q.put(grid[start_x][start_y])
    while(not q.empty()):
        
        #take the node from the priority list 
        nownode = q.get()
        nownode.isClosed = True
        #nownode.isOpen = False
        nownode.string = "2"
        #q_finished.put(nownode)
        if(nownode.x == end_x and nownode.y == end_y):
            #if we are at the end, then we are done
            return
        
        #check the neighbors
        dy = [1,1,1,0,0,-1,-1,-1]
        dx = [-1,0,1,-1,1,-1,0,1]
        for i in range(8):
            #check if index out of bounds 
            if (0 <= nownode.x + dx[i] < len(grid) and 0 <= nownode.y + dy[i] < len(grid[0])):
                neighbor = grid[nownode.x + dx[i]][nownode.y + dy[i]]
                if(neighbor.isObstacle):
                    continue
                if(neighbor.isClosed):
                    continue
                distance = ((nownode.x - neighbor.x)**2 + (nownode.y - neighbor.y)**2)**0.5
                if(nownode.g + distance < neighbor.g or not neighbor.isOpen):
                    #update f_cost
                    neighbor.g = nownode.g + distance 
                    neighbor.f = neighbor.g + neighbor.h
                    #make parent
                    neighbor.parent = nownode
                    if(not neighbor.isOpen):
                        neighbor.isOpen = True
                        q.put(neighbor)
                    



def makeParent(grid, node):
    grid[node.x][node.y].string = "3"
    if(node.parent == None): return 
    makeParent(grid, node.parent)



def main():
    #".": cell
    #"1": obstacle
    #"2": visited 
    #"3": actual path
    width = 10
    length = 10
    grid = makeGrid(width,length,0.3,0,0,width-1,length-1)
    solveGrid(grid, 0, 0, width-1, length-1)
    makeParent(grid, grid[width-1][length-1])
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(grid[i][j], end = " ")
        print("\n")
    

if __name__ == "__main__":
    main()
    