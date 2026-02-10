def change_tuple(input_tuple, position, value):
    #tuples cant be edited easily, so we use this function instead
    temp_list = list(input_tuple)
    
    temp_list[position] = value
    
    #print(temp_list)
    
    output_tuple = tuple(temp_list)
    
    return output_tuple

def create_maze(x: int = 5, y : int = 5):
    
    #The maze consists of a list. Within this list is many lists, each corresponding to a row
    # Inside each of these lists, are tuples. Each tuple corresponds to a coord
    # The tuple contains four values (x,y,left,bottom)
    # x and y are coords. Left and bottom indicate the presence of a wall to the east or south of a coord
    # This reduces data redundancy as each coord-tuple only contains 2 potential walls, 
    
    left = []
    bottom = []
    x_coords = []
    y_coords = []
    
    maze_list = []
    
    for i in range(0, x, 1):
        left.append(0)
        bottom.append(0)
        
    for i in range(0, x, 1):
        x_coords.append(i)
        
    for i in range(0, x, 1):
        y_coords.append(0)
        
    line_tuple = list(zip(x_coords, y_coords, left, bottom))
    
    
    maze_list.append(line_tuple.copy())

    # Changes the Y value in the quad tuple.    
    for y_value in range(1, y , 1):
        for counter in range(0, x , 1):
            line_tuple[counter] = change_tuple(line_tuple[counter], 1 , y_value)
        maze_list.append(line_tuple.copy())
        #.copy() is required otherwise maze_list would just contain copies of the last line_tuple to be added
        
        
    return maze_list
            

                 

def add_horizontal_wall(maze, x_coordinate, horizontal_line):
    line_list = maze[horizontal_line]
        
    tuple_to_change = line_list[x_coordinate]           
    
    new_tuple = change_tuple(tuple_to_change, 3, 1)
    
    line_list[x_coordinate] = new_tuple
    
    maze[horizontal_line] = line_list
    
    return maze
    

    
    
    
def add_vertical_wall(maze, y_coordinate, vertical_line):
    line_list = maze[y_coordinate]
    
    tuple_to_change = line_list[vertical_line]
    
    new_tuple = change_tuple(tuple_to_change, 2, 1 )  
    line_list[vertical_line] = new_tuple
    
    maze[y_coordinate] = line_list
    
    return maze


def get_dimensions(maze):
    Y = 0
    X = 0
    
    for lines in maze:
        Y = Y + 1
    
    first_line_in_maze = maze[0]
    
    for tuples in first_line_in_maze:
        X = X + 1
    #print(f"X: is {X} and Y is {Y}")   
    return (X,Y)


def get_walls(maze, x_coordinate: int, y_coordinate: int):
    
    east_wall = False
    south_wall = False
    north_wall = False
    west_wall = False
    
    #Code below ensures we only check for presence of internal walls if the coord is not right next to an external wall
    #If a coord is right next to any external wall, we return TRUE for that direction
    boundry_north = check_boundary_north(maze, x_coordinate, y_coordinate)
    boundry_east = check_boundary_east(maze, x_coordinate, y_coordinate)
    boundry_south = check_boundary_south(maze, x_coordinate, y_coordinate)
    boundry_west = check_boundary_west(maze, x_coordinate, y_coordinate)
    
    
    if boundry_north == True:
        north_wall = True
    else:
        coord_to_north_tuple = get_walls_of_current_cord(maze, x_coordinate, y_coordinate + 1)
        if coord_to_north_tuple[1] == True:
            north_wall = True
    
    
    if boundry_east == True:
        east_wall = True
    else:
        coord_to_east_tuple = get_walls_of_current_cord(maze, x_coordinate + 1, y_coordinate)
        if coord_to_east_tuple[0] == True:
            east_wall = True
            
    
    if boundry_south == True:
        south_wall = True
    else:
        coord_tuple = get_walls_of_current_cord(maze, x_coordinate, y_coordinate)
        if coord_tuple[1] == True:
            south_wall = True
            
    if boundry_west == True:
        west_wall = True
    else:
        coord_tuple = get_walls_of_current_cord(maze, x_coordinate, y_coordinate)
        if coord_tuple[0] == True:
            west_wall = True

    wall_check = (north_wall, east_wall, south_wall, west_wall)  
    return wall_check

def get_walls_of_current_cord(maze, x_coordinate: int, y_coordinate: int):
    #Due to the data structure of the maze. each coord-tuple contains 4 values
    #(x,y,left,bottom)
    #left and bottom indicate the presence of a wall to the west or south of that coord
    #this function essentially just checks for the presence of those walls
    line_list = maze[y_coordinate]
    left = False
    bottom = False
    
    selected_coord_tuple = line_list[x_coordinate]
    
    #print(selected_coord_tuple)
    
    if selected_coord_tuple[2] == 1:
        left = True
    if selected_coord_tuple[3] == 1:
        bottom = True
    
    return [left, bottom]

#All the check boundary functions are used to check if the selected coordinate does not lie alongside an external wall
def check_boundary_east(maze, x_coordinate: int, y_coordinate: int):
    dimensions = get_dimensions(maze)
    
    if dimensions[0] == x_coordinate + 1:
        #print("At an east boundary")
        return True
    return False
        
def check_boundary_north(maze, x_coordinate: int, y_coordinate: int):
    dimensions = get_dimensions(maze)
    
    if dimensions[1] == y_coordinate + 1:
        #print("At a north boundary")
        return True
    return False
    
def check_boundary_south(maze, x_coordinate: int, y_coordinate: int):
    if y_coordinate == 0:
        return True
    return False
    
def check_boundary_west(maze, x_coordinate: int, y_coordinate: int):
    if x_coordinate == 0:
        return True
    return False



    