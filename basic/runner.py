from maze import *
from typing import Optional, Tuple

def create_runner(x: int = 0, y : int = 0, orientation:str = "N"):
    runner_list = []
    runner_list.append(x)
    runner_list.append(y)
    runner_list.append(orientation)
    return runner_list
    
    
    
#test1 = create_runner(1,5,"E")
#print(f"test1 ==  {test1}")


def get_x(runner):
    return runner[0]

def get_y(runner):
    return runner[1]

def get_orientation(runner):
    return runner[2]

def turn(runner, direction:str):

    runner_direction = get_orientation(runner)
    
    try:
        if direction == "Left":
            if runner_direction == "N":
                runner[2] = "W"
            
            elif runner_direction == "E":
                runner[2] = "N"
            
            elif runner_direction == "S":
                runner[2] = "E"
        
            elif runner_direction == "W":
                runner[2] = "S"
                
        elif direction == "Right":
            if runner_direction == "N":
                runner[2] = "E"
            
            elif runner_direction == "E":
                runner[2] = "S"
            
            elif runner_direction == "S":
                runner[2] = "W"
        
            elif runner_direction == "W":
                runner[2] = "N"   
        return runner
    except: raise ValueError
    


def forward(runner):

    runner_direction = get_orientation(runner)
    
    if runner_direction == "N":
        runner[1] = runner[1] + 1
        
    elif runner_direction == "E":
        runner[0] = runner[0] + 1
        
    elif runner_direction == "S":
        runner[1] = runner[1] - 1
        
    elif runner_direction == "W":
        runner[0] = runner[0] - 1
        
    else:
        print("Error. Runner orientation initialised incorrectly!")
        return
    return runner


def sense_walls(runner, maze) -> tuple[bool, bool, bool]:
    x_coordinate = get_x(runner)
    y_coordinate = get_y(runner)
    orientation = get_orientation(runner)
    walls_4 = get_walls(maze, x_coordinate, y_coordinate )
    
    if orientation == "N":
        return (walls_4[3], walls_4[0], walls_4[1])
    if orientation == "E":
        return (walls_4[0], walls_4[1], walls_4[2])
    if orientation == "S":
        return (walls_4[1], walls_4[2], walls_4[3])  
    else:
        return (walls_4[2], walls_4[3], walls_4[0])

    
def go_straight(runner,maze):
    orientation = get_orientation(runner)
    
    x_coordinate = get_x(runner)
    
    y_coordinate = get_y(runner)
    
    sensed_walls = sense_walls(runner,maze)
    
    if sensed_walls[1] == False:
        runner = forward(runner)
        return runner
    else:
        raise ValueError("Runner bumped into a wall!")   

def move(runner,maze):
    sensed_walls = sense_walls(runner, maze)     
    if sensed_walls[0] == False:
        #go left
        runner = turn(runner, "Left")
        #runner = runner + go_straight(runner,maze)
        runner = go_straight(runner,maze)
        movement = "LF"
        
    elif sensed_walls[1] == False:
        #go forward
        #runner = runner + go_straight(runner,maze)
        runner = go_straight(runner,maze)
        movement = "F"
        
    elif sensed_walls[2] == False:
        #go right
        runner = turn(runner, "Right")
        #runner = runner + go_straight(runner,maze)
        runner = go_straight(runner,maze)
        movement = "RF"
    else:
        runner = turn(runner, "Right")
        runner = turn(runner, "Right")
        #runner = runner + go_straight(runner,maze)
        runner = go_straight(runner,maze)
        movement = "B"
    return (runner,movement)
        
def explore(runner, maze, goal = None):
    target_found = False
    step_counter = 0
    dimensions = get_dimensions(maze)
    step_limit = 4 * dimensions[0] * dimensions[1]
    #print(f"The step limit is {step_limit}")
    route = []
    #auto_goal = []
    
    if goal == None:
        goal = get_dimensions(maze)
        #print(goal)
        updated_goal = (goal[0] - 1, goal[1] - 1)
        #print(updated_goal)
    else:
        updated_goal = (goal[0], goal[1])
    
    #The dimensions of the maze will be one greater than the rightmost coord, as the dimensions has to account for the 0 row and 0 column
    # so the default goal has to be the dimensions subtract one on x and y
    while target_found == False:
        if step_counter > step_limit:
            raise ValueError("Maze is not solvable via left-hug algorithm")
        step_counter = step_counter + 1
        
        if updated_goal[0] == get_x(runner) and updated_goal[1] == get_y(runner):
            target_found = True
        else:
            move_output = move(runner,maze)
            route.append((get_x(runner),get_y(runner),move_output[1]))
            runner = move_output[0]

    #Q6 code:
    with open("exploration.csv", "w") as explore_file:
        explore_file.write("Step,x-coordinate,y-coordinate,Actions \n")
        action_counter = 1
        for entries in route:
            x_coord = entries[0]
            y_coord = entries[1]
            action = entries[2]
            explore_file.write(f"{action_counter},{x_coord},{y_coord},{action}\n")
            action_counter = action_counter + 1
        explore_file.close()
       
    #print(route)
    return route
