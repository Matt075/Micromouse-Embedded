import time
from Maze import Maze
from Maze import Position
import Movement
import Sensor


def awaiting_signal():
    # wait for user signal to start searching the maze
    print 'Awaiting signal!'
    while not Sensor.front_wall():
        pass
    print 'Signal Received!'
    time.sleep(0.5)


def select_path():
    """ Algorithm for making decision
    - Advance to cell with the shortest distance to the center cells, unless
    - That cell has already been traversed, then
    - Take the next cell with the shortest distance to the center cells, AND
    has not been previously traversed
    """
    # Always move to the centre of intersection before making decision
    Movement.approach_center()

    decision = "t"
    path_checked = True
    shortest_choice = 1000
    if not Sensor.front_wall():
        # including the front opening in decision making if there is one
        shortest_choice = Maze.get_dist("front")
        # store the front cell's distance to the center cells
        path_checked = Maze.get_check_stat("front")
        # store whether this front cell has been previously traversed
        decision = "f"
    if not Sensor.left_wall_far():
        # including the left opening in decision making if there is one
        temp_distance = Maze.get_dist("left")
        temp_path_checked = Maze.get_check_stat("left")
        if ((temp_distance < shortest_choice)
                or (not temp_path_checked and path_checked)):
            # compare the current condition to the previous cell
            # and see if which cell is more favorable
            shortest_choice = temp_distance
            path_checked = temp_path_checked
            decision = "l"
    if not Sensor.right_wall_far():
        # including the right opening in decision making if there is one
        temp_distance = Maze.get_dist("right")
        temp_path_checked = Maze.get_check_stat("right")
        if ((temp_distance < shortest_choice)
                or (not temp_path_checked and path_checked)):
            # compare the current condition to the previous cell
            # and see if which cell is more favorable
            decision = "r"
    if Position.is_center():
        # ignore this. I can't really explain it, but it works
        decision = "f"
    return decision


def solve_maze():
    while not Position.is_center():

        # Set current position as having been traversed
        Maze.pos_set_checked()

        # if there is any opening on the sides, start path choosing
        if (not Sensor.left_wall_far() or not Sensor.right_wall_far()
                or Sensor.front_wall()):

            # Record coordinates moving forward
            Position.update_pos()

            # Select the path that leads to the cell with the shortest distance to
            # the center cells, unless that cell has been traversed and at least
            # one other has not been traversed
            path = select_path()

            # Run the path chosen
            print path + '\n'
            turns.append(path)
            if path == 'f':
                Movement.skip_forward()
            elif path == 'r':
                Movement.advance_right()
            elif path == 'l':
                Movement.advance_left()
            elif path == 't':
                Movement.turn_180()

        # move forward if the only way to go is to move forward
        else:
            Movement.advance_forward("s")
            Position.add_pos_counter()


def exit_center():
    """ Exit the center cells """
    after_move_taken = 0
    while after_move_taken < 3:
        if (not Sensor.left_wall_far() or not Sensor.right_wall_far()
                or Sensor.front_wall()):
            Movement.approach_center()
            print 'l'
            turns.append('l')
            Movement.advance_left()
            after_move_taken += 1
        else:
            Movement.advance_forward("s")

    after_move_taken = 0
    while after_move_taken < 1:
        if (not Sensor.left_wall_far() or not Sensor.right_wall_far()
                or Sensor.front_wall()):
            Movement.approach_center()
            if turns[len(turns) - 1] == 'l':
                print 'r'
                turns.append('r')
                Movement.advance_right()
            else:
                print 'l'
                turns.append('l')
                Movement.advance_left()
            after_move_taken += 1
        else:
            Movement.advance_forward("f")


def return_to_origin():
    """ Return to the starting point, taking the opposite decisions taken """
    after_move_taken = len(turns) - 5
    while after_move_taken > 0:
        if (not Sensor.left_wall_far() or not Sensor.right_wall_far()
                or Sensor.front_wall()):
            Movement.approach_center()
            if turns[after_move_taken - 1] == 'f':
                print 'f'
                turns.append('f')
                Movement.skip_forward()
            elif turns[after_move_taken - 1] == 'r':
                print 'l'
                turns.append('l')
                Movement.advance_left()
            elif turns[after_move_taken - 1] == 'l':
                print 'r'
                turns.append('r')
                Movement.advance_right()
            else:
                print 't'
                turns.append('t')
                Movement.turn_180()
            after_move_taken -= 1
        else:
            Movement.advance_forward("f")
    # Make a cool heroic 180 degree when the robot returns to starting point
    while not Sensor.front_wall():
        Movement.advance_forward("f")
    Movement.go_forward(0.3, "f")
    print 't'
    Movement.turn_180()
    Movement.stop()


turns = []  # Save the turns taken by robot during the search run
awaiting_signal()
solve_maze()
exit_center()
return_to_origin()


# Print the turns taken to a text file for use later (a fast run)
turn_list = open("turns.txt", "w")
for i in range(len(turns)):
    print>> turn_list, turns[i]
turn_list.close()
