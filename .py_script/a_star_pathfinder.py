"""A pathfinder program to find the shortest path from 
the orange spot to the turquoise spot using A* Algorithm.
Displayes the shortest path in purple.
Displayes the adjacent nodes in green.
Displayes the open list nodes (that deviates from the intended path) in red"""

#import pygame lib
import pygame 

#initializing pygame methods
pygame.init()

#creating a class for nodes: contains information of the node position, the parent node position, and g,h&f values.
class Spot:

    def __init__(self, parent = None, coordinate = None):
        self.parent = parent
        self.coordinate = coordinate

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.coordinate == other.coordinate


#pygame window setup
window = pygame.display.set_mode((600, 600))
#setting a caption to the window
pygame.display.set_caption("Pathfinder Algorithm")

#defining color codes for all the colors used
orange = (255,100,10)
turquoise = (64, 224, 208)
green = (0, 255, 0)
grey = (0,0,0)
white = (255,255,255)
red = (255,0,0)
yellow = (255, 255, 0)
purple = (128, 0, 128)

#fill window with white color
window.fill(white)

barrier = [] #a list to store obstacle's locations

maze = [] #the entire maze stored in a list

start = None #start node coordinate

end = None #end node coordinate

#a function to draw box (in the specific spot/node), takes color and item from the maze list as arguments.
def draw_rect(color,box):
    pygame.draw.rect(window, color, box)

#Main Algorithm Function
def algorithm(game, start, end):

#defining start and end spot objects
    start_spot = Spot(None,start)
    start_spot.g = start_spot.h = start_spot.f = 0
    end_spot = Spot(None,end)
    end_spot.g = end_spot.h = end_spot.f = 0

#creating open and closed list
    open_list = []
    closed_list = []

    open_list.append(start_spot) #adding the start node to the open_list

    #a loop to move nodes from open list to closed list
    while len(open_list) > 0:

        current_spot = open_list[0] #taking the first item (start node) from the open list as current spot.
        current_index = 0

        #for all the spots/nodes in open list, if the f value of the spot/node is less than the current spot
        #remove that item from the open list and add it to the closed list
        for index,item in enumerate(open_list):
            if item.f < current_spot.f:
                current_spot = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_spot)


        #if the end spot is found then add the current coordinate and all the parent coordinate to the path list
        if current_spot == end_spot:
            path = []
            current = current_spot
            while current is not None:
                path.append(current.coordinate)
                draw_rect(purple, maze[current.coordinate[0]][current.coordinate[1]])
                current = current.parent
            return path[::-1]

        #create a list of neighbours to add 8 spots(if walkable) around our current spots
        neighbour = []

        #for loop to find 8 surrounding spots
        for new_coordinate in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            spot_coordinate = (current_spot.coordinate[0] + new_coordinate[0], current_spot.coordinate[1] + new_coordinate[1]) #adj spot calculation

            #if the adjacent spot(spot_coordinate) is outside the number of nodes in the maze then its not walkable, so ignored.
            if spot_coordinate[0] > (len(maze) - 1) or spot_coordinate[0] < 0 or spot_coordinate[1] > (len(maze[len(maze)-1]) -1) or spot_coordinate[1] < 0:
                continue

            #if the adjacent spot is a barrier then its not walkable either.
            if spot_coordinate in barrier:
                continue

            #the rest is walkable. Hence, considered (now the current spot will become a parent spot for this adjacent spot)
            new_spot = Spot(current_spot, spot_coordinate)

            neighbour.append(new_spot) #adding the adjacent spot to the neighbour list
            x,y = spot_coordinate
            draw_rect(green, maze[x][y]) #all the adjacent spots are displayed as green boxes in the window


        #a loop to add the low f score spots to the open list
        for buddy in neighbour:

            flag = 0


            if buddy in closed_list:
                continue

            #to calculate g,h and f scores of the adjacent nodes
            buddy.g = current_spot.g + 1
            buddy.h = ((buddy.coordinate[0] - end_spot.coordinate[0]) ** 2) + ((buddy.coordinate[1] - end_spot.coordinate[1]) ** 2)
            buddy.f = buddy.g + buddy.h

            #to check if the adjacent spot is already in the open list and whether it has a lower g score
            for open_spot in open_list:
                if buddy == open_spot and buddy.g > open_spot.g:
                    flag = 1
                    break

            if flag == 1:
                continue

            open_list.append(buddy) #add the adjacent spot to the open list
            draw_rect(red, maze[buddy.coordinate[0]][buddy.coordinate[1]]) #nodes in the open list are displayed in red

#function to calculate the top right corner coordinate value in a box by using the mouse position as an argument
def spot_cal(coor):
    a = coor[0]
    b = coor[1]
    x = (a//20)
    y = (b//20)
    return (x,y)

#drawing the maze window with all the boxes and adding the boxes to the maze list using for loop
for x in range(30):
    col = []
    for y in range(30):
        rect = pygame.Rect((x*20, y*20), (20, 20))
        rect2 = pygame.Rect((x*20 + 1, y*20 + 1), (18, 18))
        col.append(rect2)
        pygame.draw.rect(window,(150,150,150),rect,1)
    maze.append(col)

#initializing boolian values to check if the mouse button is pressed down or not 
left_mouse_down = False
right_mouse_down = False

run = True
 
#main while loop
while run:


    orange_in = 0 #initializing flag value to check if there is a start node already added in the maze (orange spot)
    turquoise_in = 0 #initializing flag value to check if there is a end node already added in the maze (turquoise spot)
    block = 0 #variable used to add the obstacle boxes to the barrier list
    empty = 0 #variable used to remove items from the barrier list if the right mouse button is pressed on the obstacle
    pixels = pygame.PixelArray(window) #variable to check all the pixels in the window (to check if orange or turquoise in window)

    event = pygame.event.poll() #.poll() func to get all the event and compare
    #if quit is clicked, stop the loop
    if event.type == pygame.QUIT:
        run = False

    #when mouse button is pressed
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #1 is left mouse button
        left_mouse_down = True
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        left_mouse_down = False

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: #3 is right mouse button
        right_mouse_down = True
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
        right_mouse_down = False

    #main for loop to check collide points; selects the entire box if the curser is moved anywhere inside the box when the mouse button is pressed
    for i in range(30):
        for j in range(30):
            if maze[i][j].collidepoint(pygame.mouse.get_pos()):
                if right_mouse_down: #right mouse button to clear to default box
                    draw_rect(white,maze[i][j])
                    (x,y) = empty = spot_cal(pygame.mouse.get_pos()) #.get_pos() func gets the mouse position (x,y)
                    if empty in barrier:
                        barrier.pop(barrier.index(empty)) #to clear obstacle (remove the obstacle boxes form the barrier list)

                if left_mouse_down:
                    if orange in pixels: #check if orange spot (start node) in the window
                        if turquoise in pixels: #check if turquoise spot (end node) in the window
                            draw_rect(grey,maze[i][j]) #if both orange and turquoise in the window then start putting barriers when left mouse button is pressed
                            (x,y) = block = spot_cal(pygame.mouse.get_pos())
                            barrier.append(block) #add the barrier boxes in barrier list
                        else:
                            pygame.time.wait(500)
                            draw_rect(turquoise, maze[i][j]) #if turquoise not in window put turquoise spot in the window when left mouse button is pressed
                            (x,y) = end = spot_cal(pygame.mouse.get_pos()) #add the turquoise spot coordinate to the "end" variable
                            
                    else:
                        draw_rect(orange,maze[i][j]) #if orange not in window put orange spot in the window when left mouse button is pressed
                        (x,y) = start = spot_cal(pygame.mouse.get_pos()) #add the orange spot coordinate to the "start" variable
                        pygame.time.wait(500)

    del pixels #deletes the saved pixel array to free up the memory 

    #when space key is pressed it starts to draw the path using the algorithm
    if event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_SPACE:
            path = algorithm(maze, start, end) #calls the algorithm function and returns the path list
            print(path) #prints the path list (purple spots)


    pygame.display.update() #updates the screen(window) everytime the loop runs
