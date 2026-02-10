from maze import *
from runner import *
from typing import Optional, Tuple
import math
import sys

import argparse

def main(argv=None):
    try:
        parser = argparse.ArgumentParser(description ='ECS Maze Runner')

        parser.add_argument("maze",
                            type = str, 
                            help = "The name of the maze file, e.g., maze1.mz")

        parser.add_argument("--starting",
                            type = str, 
                            help = "The starting position, e.g., \"2, 1\"")

        parser.add_argument("--goal",
                            type = str,
                            help = "The goal position, e.g., \"4, 5\"")

        args = parser.parse_args(argv)
        read_maze = maze_reader(args.maze)
    except:
        raise ValueError ("Error while attempting to parse Command Line inputs")
    #print(f" Render: {render(read_maze)}")
    
    ## the starting and goal values must be converted into a compatible format
    #If starting is None we assign (0,0)
    #If goal is None we dont pass it in. It will be handled down
    #stream in shortest_path/explore
    
    if args.starting != None:
        start_x, start_y = args.starting.split(",")
        starting_tuple = (int(start_x), int(start_y))
    else:
        starting_tuple = (0,0)
        
    if args.goal != None:
        goal_x, goal_y = args.goal.split(",")
        goal_tuple = (int(goal_x), int(goal_y))

    if args.goal != None:
        #valid_coords_check ensures negative coords or coords outside the maze boundaries are not passed into pathfinding algos
        valid_coords_check = check_start_goal(read_maze, starting_tuple, goal_tuple)
        if valid_coords_check == False:
            raise ValueError("Inputed coords are not present on maze")
    else:
        # If goal is None, we do not need to check if it is present in the maze
        # So in goal's place we pass in (0,0) as we know that will definitely be in the maze
        #This way we can still test for start, even if goal is none
        valid_coords_check = check_start_goal(read_maze, starting_tuple, (0,0))
        if valid_coords_check == False:
            raise ValueError("Inputed coords are not present on maze")
    
    if args.goal != None:
        print(shortest_path(read_maze, starting_tuple, goal_tuple))   
    else:
        print(shortest_path(read_maze, starting_tuple))
    
    #print(starting_tuple)
    #print(goal_tuple)
    
    

def check_start_goal( maze, start, goal):
    #checks if start and goal coords are actually on the maze grid
    #print(start)
    all_coords = []
    maze_dimensions = get_dimensions(maze)
    for x in range (0, maze_dimensions[0] , 1):
        for y in range(0, maze_dimensions[1] , 1):
            all_coords.append((x,y))
    
    #print(all_coords[4])

    if start not in all_coords:
        print("Start not in maze")
        return False
    
    if goal not in all_coords:
        print("goal not in maze")
        return False
    
    return True
    
def shortest_path(maze, starting = None, goal = None):
    #coords_only is used to remove movements from the tuples to give us just coords. Stack is used to remove duplicate coords.
    #Initial orientation contains the orientation of the initial coord
    #a_star(maze, starting, goal)
    initial_orientation = "N"
    
    #exploration_steps is for part 6:
    exploration_steps = 0
    
    orientation_stack = []
    orientation_stack.append(initial_orientation)
    coords_only = []
    stack = []
    shortest_path = []
    
    if starting != None:
        first_coord = (starting[0], starting[1])
        #print(first_coord)
        runner = create_runner(starting[0],starting[1])
    else:
        first_coord = (0, 0)
        runner = create_runner()

    coords_only.append(first_coord)
    
    if goal != None:
        route = explore(runner,maze, goal)
    else:
        route = explore(runner,maze)
        
    

    ## Generates a list of just coords
    for tuples in route:
        exploration_steps = exploration_steps + 1
        coords_only.append((tuples[0], tuples[1]))
    #print(f"exploration_steps = {exploration_steps}")
        
    ##
    for coords in coords_only:
        if coords in stack:
            stack.pop()
        else:
            stack.append(coords)
 
    for i in range(1, len(stack), 1):
        adj_tuple = (0,0,0,0)
        prev_orientation = orientation_stack[-1]
        prev_coord = stack[i - 1]
        current_coord = stack[i]
        
        X_change = current_coord[0] - prev_coord[0]
        Y_change = current_coord[1] - prev_coord[1]
        
        movement, new_orientation = regen_movements(X_change,Y_change, prev_orientation)
        
        orientation_stack.append(new_orientation)
        tuple_to_add = (prev_coord[0],prev_coord[1],movement)
        shortest_path.append(tuple_to_add)
        #print(f"{prev_coord} : {movement}")
    #Below is for part 6:
    path_length = len(shortest_path)
    score = exploration_steps / 4 + path_length
    with open("statistics.CSV", "a") as stats:
        stats.write(f"{score}\n")
        stats.write(f"{exploration_steps}\n")
        stats.write(f"{shortest_path}\n")
        stats.write(f"{path_length}\n")
    stats.close()

    return shortest_path

def regen_movements(X_change, Y_change, prev_orientation):
    #Used to identify the movements for all coords in the path
    new_orientation = ""
    movement = ""
    
    if X_change == 1:
        new_orientation = "E"
        if prev_orientation == "N":
            movement = "RF" 
        elif prev_orientation == "E":
            movement = "F"
            
        elif prev_orientation == "S":
            movement = "LF"
            
        elif prev_orientation == "W":
            movement = "B"
            
    elif X_change == -1:
        new_orientation = "W"
        if prev_orientation == "N":
            movement = "LF"
            
        elif prev_orientation == "E":
            movement = "B"
            
        elif prev_orientation == "S":
            movement = "RF"
            
        elif prev_orientation == "W":
            movement = "F"
            
    elif Y_change == 1:
        new_orientation = "N"
        if prev_orientation == "N":
            movement = "F"
            
        elif prev_orientation == "E":
            movement = "LF"
            
        elif prev_orientation == "S":
            movement = "B"
            
        elif prev_orientation == "W":
            movement = "RF"
            
    elif Y_change == -1:
        new_orientation = "S"
        if prev_orientation == "N":
            movement = "B"
            
        elif prev_orientation == "E":
            movement = "RF"
            
        elif prev_orientation == "S":
            movement = "F"
            
        elif prev_orientation == "W":
            movement = "LF"
    
    return (movement,new_orientation)


def maze_reader(maze_file: str):
    try:
        
        height_counter = 0
        width_counter = 0
        with open(maze_file) as maze_diagram:
            lines = maze_diagram.readlines()
            
        ##basic error checking functions:
        line_check = maze_line_uniformity(lines)
        char_check = maze_char_consistency(lines)
        
        if line_check == False or char_check == False:
            raise ValueError("Error: Non uniform chars or non uniform lines")
        

        width_counter = len(lines[0])
        number_of_lines = 0
        for line in lines:
            number_of_lines = number_of_lines + 1
            
        #print(f"Number of lines: {number_of_lines}")
        
        max_y_value = (number_of_lines - 1) / 2
        current_y_value = max_y_value - 1
        
        #print(max_y_value)
        
        vertical_walls = []
        horizontal_walls = []

        # We don't want to include the lower and upper exterior walls, so we start at 1 and go up to len(lines) - 1
        for line in range(1,len(lines) -1, 1):
            #to ensure we're only looking at horizontall wall row
            if line % 2 == 0:
                current_row = lines[line]
                #print(f"{current_y_value}:{current_row}")
                char_even_check = 0
                for char in range(1,len(current_row), 1):
                    char_even_check = char_even_check + 1
                    #We dont want to include the diagram intersections of v and h walls, so we ensure the char is odd
                    if char_even_check % 2 != 0:
                        if current_row[char_even_check] == '#':
                            horizontal_walls.append((math.floor(char_even_check / 2),int(current_y_value)))
                            
                current_y_value = current_y_value - 1
            else:
                current_row = lines[line]       
                # Similar to above, we dont want to include the exterior walls
                for char in range(1, len(current_row) - 2, 1):
                    if current_row[char] == '#':
                        
                        vertical_walls.append((math.floor(char/2),int(current_y_value)))
                    
                    
                # There are no intersections to worry about in the vertical row, so we dont need to check for that           

        
        #print(f"horizontal walls: {horizontal_walls}")
        #print(f"vertical walls: {vertical_walls}")

        #max_Y = (height_counter -1 ) / 2
        #for the width_counter we need to remove the outer walls then we 
        max_X = (width_counter - 1) / 2
        
        maze = create_maze(int(max_X ), int(max_y_value ))
        
        #print(get_dimensions(maze))
        
        for h_walls in horizontal_walls:
            add_horizontal_wall(maze, h_walls[0],h_walls[1])
            
        for v_walls in vertical_walls:
            add_vertical_wall(maze, v_walls[1], v_walls[0])
            
        #For part 6:
        with open("statistics.CSV", "w") as stats:
            stats.write(f"{maze_file}\n")
        stats.close()
        
        
        return maze
    except:
        raise IOError("error while reading maze file")
    
    
def maze_line_uniformity(lines):
    #Ensures each line of imported maze has equal length
    #print(lines)
    line_with_no_n = []
    
    # Remove all the \n chars from the lines and put each new line inside an array instead
    # This way the lines have the same length but are also separated from each other
    for i in range(0,len(lines) ,1):
        temp = lines[i].replace("\n","")
        line_with_no_n.append(temp)
        
    #print(line_with_no_n)
    
    for line in line_with_no_n:
        if len(line) != len(line_with_no_n[0]):
            #print(line)
            #print(lines[0])
            #print("Line check failed")
            return False
    return True
    
def maze_char_consistency(lines):
    #ensures only accepted symbols are present in imported maze
    for line in lines:
        #print(line)
        for char in line:
            #char = char.replace(" ", "")
            if char != "#" and char != "." and char != "\n":
                #print(char)
                #print("Char check failed")
                return False
    return True

#maze = maze_reader("test.txt")

#runner = create_runner(0,0,"E")

#print(render(maze))

#print(get_dimensions(maze))

#maze_walls_generator_2(maze)

#s_path = shortest_path(runner,maze)

#print(s_path)

if __name__ == "__main__":
    main(sys.argv[1:])