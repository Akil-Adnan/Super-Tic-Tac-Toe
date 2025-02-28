import curses
from curses import wrapper
import time
from pprint import pprint
from random import randint
import sys

# 963 character description of the game collected from the web
description = "Super Tic-Tac-Toe begins with the usual 3x3 grid, but in each of its squares, another tic-tac-toe game is placed. The first player can play in any of these 81 spaces. Let's say they choose to play in the middle game in the upper right. The next player must play in the game whose location corresponds to the square chosen in the previous move. So, because X chose the upper right square, O must play in the upper right game. Let's say O goes in the middle. This means that X must play in the game in the middle. Because X played the middle square, O is now forced to play in this very same game and can block X. Play continues like this until someone gets three in a row in one of the games. When they do, that entire square is marked for them. If a player is ever forced to play in a game that has already been won, they can't and instead get to choose to play anywhere. Play continues until someone wins three games that are in a row."

# Typograpgy of the name of the game
name = (
 "███████ ██    ██ ██████  ███████ ██████      ████████ ██  ██████       ████████  █████   ██████       ████████  ██████  ███████"
 "██      ██    ██ ██   ██ ██      ██   ██        ██    ██ ██               ██    ██   ██ ██               ██    ██    ██ ██     "
 "███████ ██    ██ ██████  █████   ██████         ██    ██ ██      █████    ██    ███████ ██      █████    ██    ██    ██ █████  "
 "     ██ ██    ██ ██      ██      ██   ██        ██    ██ ██               ██    ██   ██ ██               ██    ██    ██ ██     "
 "███████  ██████  ██      ███████ ██   ██        ██    ██  ██████          ██    ██   ██  ██████          ██     ██████  ███████"

)

# For the initial pop up screen
start_text = (
"                           ███████╗██╗   ██╗██████╗ ███████╗██████╗                                "
"                           ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗                               "
"                           ███████╗██║   ██║██████╔╝█████╗  ██████╔╝                               "
"                           ╚════██║██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗                               "
"                           ███████║╚██████╔╝██║     ███████╗██║  ██║                               "
"                           ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝                               "
"                                                                                                   "
"████████╗██╗ ██████╗              ████████╗ █████╗  ██████╗              ████████╗ ██████╗ ███████╗"
"╚══██╔══╝██║██╔════╝              ╚══██╔══╝██╔══██╗██╔════╝              ╚══██╔══╝██╔═══██╗██╔════╝"
"   ██║   ██║██║         █████╗       ██║   ███████║██║         █████╗       ██║   ██║   ██║█████╗  "
"   ██║   ██║██║         ╚════╝       ██║   ██╔══██║██║         ╚════╝       ██║   ██║   ██║██╔══╝  "
"   ██║   ██║╚██████╗                 ██║   ██║  ██║╚██████╗                 ██║   ╚██████╔╝███████╗"
"   ╚═╝   ╚═╝ ╚═════╝                 ╚═╝   ╚═╝  ╚═╝ ╚═════╝                 ╚═╝    ╚═════╝ ╚══════╝"
"\n                                      Made by Akil Adnan                                         "
)

# For displaying purpose of the big board
big_board = (
"             |             |             "
"             |             |             "
"             |             |             "
"             |             |             "
"             |             |             "
"-------------|-------------|-------------"
"             |             |             "
"             |             |             "
"             |             |             "
"             |             |             "
"             |             |             "
"-------------|-------------|-------------"
"             |             |             "
"             |             |             "
"             |             |             "
"             |             |             "
"             |             |            "
)

O_sign = (
"   █████   "  
"  ██   ██  "
"  ██   ██  "
"  ██   ██  "
"   █████  "
)

X_sign = (
"  ██   ██  "
"   ██ ██   " 
"    ███    "
"   ██ ██   "
"  ██   ██ "
)

# Reference values corresponding to the position for checking the game
reference_values = {
    1: 4, 
    2: 3,
    3: 8,
    4: 9,
    5: 5,
    6: 1,
    7: 2,
    8: 7,
    9: 6
}


# All the value required for the main board
game = {
    "count": 0,
    "available": {1, 2, 3, 4, 5, 6, 7, 8, 9},
    "animation": set(),
    "outcome": None,
    "debug": False,
    "current_grid": 0,
    "previous_grid": 0,
    "player_move": 0,
    "X": set(),
    "O": set()
}


# Initiating the nine mini grids in the main grid
def create_keys(game_state):
    """Adds the essential keys for the 9 mini-grids to the game state dictionary.

    Args:
        game_state: A dictionary representing the game state.

    Returns:
        The modified game state dictionary with added mini-grid keys.
    """
    for i in range(1, 10):
        # Small board is refered by n_ 
        mini_grid = {
            f"{i}_available": {1, 2, 3, 4, 5, 6, 7, 8, 9},
            f"{i}_outcome": None,
            f"{i}_X": set(),
            f"{i}_O": set()
        }
        # Adding the newly formed keys
        game_state.update(mini_grid)

    return game_state



# For checking the game: only input the position values
def status(move_set):
    """Checks if the given move set forms a magic square.

    A magic square is a 3x3 grid where the sum of each row, column, and diagonal is the same.
    This function determines if the given move set can form a magic square. Replaces the values
    of the input set by reference values of the given position.

    Args:
        move_set: A set containing the positions of a player's moves on a 3x3 grid.

    Returns:
        1 if the move set forms a magic square, 0 otherwise.
    """
    # Convert the position list into reference value list for checking the 3x3 magic square grid
    converted_list = [reference_values[i] for i in move_set]
    # Code for finding the subsets
    output_list = [[]]
    for i in converted_list:
        output_list += [[i] + j for j in output_list]
    
    # Check if sum of the any three entries is 15
    status_ = 15 in list(map(lambda x: sum(x), filter(lambda x: len(x) == 3, output_list)))

    # If 15 found return 1, else return 0
    return status_


def check_game(X_moves = set(), O_moves = set(), available = set(), main_grid = False):
    """Analyzes the status of a grid given the moves made by X and O.

    Determines if the grid has a winner, is a draw, or if further moves can be made.

    Args:
        x_moves: A set of moves made by player X.
        o_moves: A set of moves made by player O.
        available_moves: A set of available moves in the grid.
        main_grid: A boolean indicating whether it's the main grid (default False).

    Returns:
        outcome: None if undetermined, 0 for draw, 1 for "X" win, 2 for "O" win.
    """
    # X or O completed the magic square or not
    X_status = status(X_moves)
    O_status = status(O_moves)
    # Any available moves in that grid
    available = len(available) != 0

    # If X and O hasn't completed magic square and moves are available in the grid
    if X_status == O_status == False and available:
        outcome = None
    
    # If X or O has completed the magic square
    elif X_status != O_status:
        outcome = 1 if X_status else 2
    
    # If moves aren't avilable
    else:
        # Special rules for main gird when the grid is filled up
        if main_grid:
            # If X and O occupies won same number of small grid
            if len(X_moves) == len(O_moves):
                outcome = 0
            # If X won more small grids than O
            elif len(X_moves) > len(O_moves):
                outcome = 1
            # If O won more small grids than O
            else:
                outcome = 2
        
        # Game is treated as draw
        else:
            outcome = 0

    return outcome


# Input system
def obtain_input(screen, available_moves=set(), move=None, toggle_debug_=None):
    """Gets valid input from the user.

    Continuously prompts the user for input until a valid input is provided.

    Args:
        window: The curses window object.
        available_moves: A set of valid input options.
        move: An optional string indicating the type of move (X, O, or None for grid selection).

    Returns:
        The valid input provided by the user.
    """
    # When the user inputs other character except for the accepted characters
    error_text = "\nThis move is not valid!!!\n  The available moves are:\n   " + str(available_moves)
    ref = {1:(4, 1), 2:(4, 5), 3:(4, 9), 4:(2, 1), 5:(2, 5), 6:(2, 9), 7:(0, 1), 8:(0, 5), 9:(0, 9)}
    default_box = "   |   |   \n   ---|---|---\n      |   |   \n   ---|---|---\n      |   |   \n"

    # Clears the window
    screen.clear()

    # If a move is given
    if move:
        # Default text
        input_text = "Please select the position in the grid: "
        screen.addstr(3, 0, input_text, curses.color_pair(4))
    # If a move is not given that is the function is used to obtain an input for changing the big grid
    else:
        # Text for changing the grid
        color = curses.color_pair(2)
        input_text = "Please select in which big grid to play: "
        screen.addstr(3, 0, input_text, color)

    move = "X" if game["count"] % 2 ==0 else "O"
    if move == "X":
        color = curses.color_pair(3) # Magenta-Black
        screen.addstr(0, 0, "MOVE : X", color)
    else:
        color = curses.color_pair(4) # Green-Black
        screen.addstr(0, 0, "MOVE : O", color)

    
    
    screen.addstr(6, 1, "Available moves:", curses.color_pair(2))
    screen.addstr(8, 3, default_box)
    for i in available_moves:
        screen.addstr(ref[i][0] + 8, ref[i][1] + 3, str(i), curses.color_pair(2))
    screen.refresh()

    # Runs until the desired input is found
    while True:
        # Get a character from the user
        key = screen.getkey()
       
        # Exit the function key
        if key == "q":
            sys.exit(0)
        
        if key == 'd':
            game["debug"] = not game["debug"]
            toggle_debug(toggle_debug_, game)
        
        # Display the pressed key
        screen.addstr(4, 4, f"INVALID KEY: {key}")


        # Validates the user input
        try:
            # Break if the user input in the available_moves
            if int(key) in available_moves:
                key = int(key)
                break
        # Ask for proper key from available moves
        except:
            pass

        screen.refresh()

    screen.refresh()
    
    return key


# Debugging screen
def toggle_debug(screen, game_status):
    """Needs work on it
    
    """
    if game_status["outcome"] == 0:
        game_outcome = "Draw"
    elif game_status["outcome"] == 1:
        game_outcome = "X won"
    elif game_status["outcome"] == 2:
        game_outcome = "O won"
    else:
        game_outcome = "Running"
    
    current_player_move = "X" if game_status["count"] % 2 ==0 else "O"

    debug_description = (
        f"Number of moves: {game_status["count"]}\n"
        f"Current move   : {current_player_move}\n"
        f"Available slots: {game_status["available"]}\n"
        f"Outcome        : {game_outcome}\n"
        f"X won grids    : {game_status["X"]}\n"
        f"O won grids    : {game_status["O"]}\n"
        f"Current grid   : {game_status["current_grid"]}\n"
        f"Previous grid  : {game_status["previous_grid"]}\n"
        f"Previous move  : {game_status["player_move"]}\n"
        f"Debug screen   : {game_status["debug"]}\n"
        f"Avaiable in 1  : {game_status["1_available"]}\n"
        f"Avaiable in 2  : {game_status["2_available"]}\n"
        f"Avaiable in 3  : {game_status["3_available"]}\n"
        f"Avaiable in 4  : {game_status["4_available"]}\n"
        f"Avaiable in 5  : {game_status["5_available"]}\n"
        f"Avaiable in 6  : {game_status["6_available"]}\n"
        f"Avaiable in 7  : {game_status["7_available"]}\n"
        f"Avaiable in 8  : {game_status["8_available"]}\n"
        f"Avaiable in 9  : {game_status["9_available"]}"
    )
    screen.erase()
    if game_status["debug"]:
        screen.addstr(0, 0, debug_description)
    else:
        screen.addstr(0, 0, description, curses.color_pair(1))
    
    screen.refresh()



# Returns a dictionary which would be used for printing having input variables as X-moves and O-moves
def combine_grid_data(x_moves=set(), o_moves=set(), get_num=False):
    """Combines move data for a grid into a dictionary.

    Creates a dictionary where keys represent move positions and values represent the player or state of the slot.

    Args:
        x_moves: A set of moves made by player X.
        o_moves: A set of moves made by player O.
        get_num: default False; if True instaed of X and O, returns the occupied space number

    Returns:
        A dictionary representing the grid state.
    """
    # Before adding the X and O moves; " " repersents no move has been given
    grid_data = {1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}
    for i in x_moves:
        if get_num:
            grid_data[i] = i
        else:
            grid_data[i] = "X"
        
    for i in o_moves:
        if get_num:
            grid_data[i] = i
        else:
            grid_data[i] = "O"

    return grid_data


def start_coordinates(stdscr, rows=0, cols=0, y_correction=0, x_correction=0):
    """Calculates the starting coordinates for a grid.

    Args:
        num_columns: The number of columns in the grid.
        num_rows: The number of rows in the grid.
        y_correction: An optional correction for the y-coordinate, defaults to 0.
        x_correction: An optional correction for the x-coordinate, defaults to 0.

    Returns:
        A tuple containing the starting y and x coordinates as integers.
    """
    all_rows, all_cols = stdscr.getmaxyx()
    start_y = all_rows // 2 - rows // 2 + y_correction
    start_x = all_cols // 2 - cols // 2 + x_correction

    return start_y, start_x


def compatibility(stdscr):
    """Checks if the terminal is compatible with the code.

    Args:
        stdscr: Standard screen curses

    Returns:
        1 if the terminal is fully compatible.
        exits the code if incompatible.
    """
    rows, cols = stdscr.getmaxyx()
    if rows < 30 or cols < 150:
        stdscr.addstr("Zoom out futher by Ctrl + - to play the game")
        stdscr.refresh()
        time.sleep(5)
        sys.exit(0)



def accessories(stdscr):
    """Initializes the game state and display settings.

    Returns:
        A tuple containing the input window, and debug window.
    """

    # Define the color pairs
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)


    # Starting screen
    rows, cols = start_coordinates(stdscr, 18, 99, -1, 0)
    flash_screen = curses.newwin(18, 99, rows, cols)
    flash_screen.addstr(0, 0, start_text, curses.color_pair(1))
    flash_screen.nodelay(True)
    while True:
        flash_screen.addstr(17, 32, "Press any key to start the game")
        flash_screen.refresh()
        time.sleep(.5)
        flash_screen.addstr(17, 32, "                               ")
        flash_screen.refresh()
        time.sleep(.5)
        try:
            flash_screen.getkey()
            flash_screen.erase()
            flash_screen.refresh()
            flash_screen.nodelay(False)
            time.sleep(.25)
            break
        except:
            pass
    

    # Initialize all the keys for the game
    create_keys(game)

    # Print the actual board
    print_grid(stdscr, game, 0, 0, 0)


    # Description or Debug screen of the game [Left middle] (Toggleable)
    rows, cols = start_coordinates(stdscr, 19, 50, 2, -50)
    toggle_debug_ = curses.newwin(19, 50, rows, cols)
    toggle_debug_.addstr(description, curses.color_pair(1))
    toggle_debug_.refresh()

    # Name of the game [Top middle]
    rows, cols = start_coordinates(stdscr, 6, 127, -11, 0)
    name_ = curses.newwin(6, 127, rows, cols)
    name_.addstr(name)
    name_.refresh()

    # Outlines of the big board [Centre]
    rows, cols = start_coordinates(stdscr, 18, 41, 3, 0)
    big_board_ = curses.newwin(18, 41, rows, cols)
    big_board_.addstr(big_board, curses.color_pair(1))
    big_board_.refresh()

    # Input box [Right middle]
    rows, cols = start_coordinates(stdscr, 19, 50, 2, 50)
    input_box_ = curses.newwin(19, 50, rows, cols)


    return input_box_, toggle_debug_


def highlight_last_move(screen, small_grid, previous_grid, last_position, game_state):
    """Highlights the previous move on the screen.

    Args:
        screen: The curses window object.
        small_grid: The current small grid number.
        previous_grid: The previous small grid number.
        previous_position: The previous position in the grid.
        game_state: The game state dictionary.
    """
    ref = {1:(4, 1), 2:(4, 5), 3:(4, 9), 4:(2, 1), 5:(2, 5), 6:(2, 9), 7:(0, 1), 8:(0, 5), 9:(0, 9)}
    if small_grid == previous_grid:
        if last_position != 0 and previous_grid in game_state["available"]:
            play = "X" if (game_state["count"] - 1) % 2 ==0 else "O"
            screen.addstr(ref[last_position][0], ref[last_position][1], play, curses.color_pair(1)) # Magenta-Black



def print_grid(stdscr, game_state = dict(), current_grid=int, previous_grid=0, last_position=0):
    """Prints the game board to the screen.

    Displays the main grid and sub-grids with the current game state.

    Args:
        stdscr: The curses screen object
        game_state: A dictionary representing the game state.
        current_grid: The index of the current sub-grid.
        current_grid: The index of the last sub-grid, default 0.
        last_position: The last position given by the user, default 0.
    """
    # Function for printing the small boards, just need the all_value dictionary
    count = 1
    # Finding the centre position of the grid
    corrected_y, corrected_x = start_coordinates(stdscr, 0, 0, 6, -19)

    # For row loop:
    for i in range(3):
        # For priting the columns in that row
        for j in range(3):
            # Display the playwindow as a separate window
            small_board_ = curses.newwin(5, 11, corrected_y - (i * 6), corrected_x + (j * 14))
            
            # If the small grid is won by X, only print the big X
            if count in game_state["X"]:
                # For a small animation that X-won that mini grid
                if count in game_state["animation"]:
                    # small_board_.cl
                    for x in range(6):
                        small_board_.addstr(0, 0, X_sign[0 : 11 * x], curses.color_pair(3))
                        time.sleep(.1)
                        small_board_.refresh()

                    game_state["animation"] -= {count}
                    
                else:
                    small_board_.addstr(X_sign)
            
            # If the small grid is won by X, only print the big X
            elif count in game_state["O"]:
                # For a small animation that X-won that mini grid
                if count in game_state["animation"]:
                    for x in range(6):
                        small_board_.addstr(0, 0, O_sign[0 : 11 * x], curses.color_pair(3))
                        time.sleep(.1)
                        small_board_.refresh()
                    
                    time.sleep(.5)
                    game_state["animation"] -= {count}
                else:
                    small_board_.addstr(O_sign)
            # If the small grid is drawn or play not complete
            else:
                # Convert in into printable format
                small_grid_ = combine_grid_data(game_state[f"{count}_X"], game_state[f'{count}_O'])
                # Load the board into the variable playwindow
                small_grid_converted = (
                    f" {small_grid_[7]} | {small_grid_[8]} | {small_grid_[9]} "
                    "---|---|---"
                    f" {small_grid_[4]} | {small_grid_[5]} | {small_grid_[6]} "
                    "---|---|---"
                    f" {small_grid_[1]} | {small_grid_[2]} | {small_grid_[3]}"
                    )
                # Highlight the current small grid in red color
                if count == game["current_grid"]:
                    small_board_.addstr(small_grid_converted, curses.color_pair(2)) # Red-Black
                    # If last position given, highlight that move
                else:
                    small_board_.addstr(small_grid_converted)
        
            highlight_last_move(small_board_, count, previous_grid, last_position, game_state)
            small_board_.refresh()
            # Refers to completion printing a small board
            count += 1



# The function to display the board and all other things will work here
def main(stdscr):
    """ Super Tic Tac Toe game in the terminal

    A strategic two-player game played on a 3x3 grid of smaller 3x3 grids. 
    Players alternate placing their mark (X or O) in a cell of the current active mini-grid.
    The location of the previous move determines the next player's mini-grid. Victory is achieved 
    by winning three mini-grids in a row, column, or diagonal.
    
    """

    # Checks if the game is compatible in the terminal or not
    compatibility(stdscr)

    # Display the accessories: Name, description
    input_box_, toggle_debug_ = accessories(stdscr)


    # The actual game mechanism
    while True:
        # Which side will play
        play = "X" if game["count"] % 2 == 0 else "O"
        
        # Debugging screen
        toggle_debug(toggle_debug_, game)

        # Obtain the input in which small grid is going to be played in
        if game["current_grid"] not in game["available"]:
            if len(game["available"]) > 1:
                game["current_grid"] = obtain_input(input_box_, game["available"], toggle_debug_=toggle_debug_)
                
            else:
                game["current_grid"] = [i for i in game["available"]][0]

            print_grid(stdscr, game, game["current_grid"], game["previous_grid"], game["player_move"])
        
        # Obtain in which position of the current grid the move will be used
        game["player_move"] = obtain_input(input_box_, game[f"{game["current_grid"]}_available"], move=play, toggle_debug_=toggle_debug_)
        game["previous_grid"] = game["current_grid"]

        # Changes in small board
        game[f"{game["current_grid"]}_available"] -= {game["player_move"]}
        game[f"{game["current_grid"]}_{play}"].add(game["player_move"])
    
        # Check small grid
        game[f"{game["current_grid"]}_outcome"] = check_game(game[f"{game["current_grid"]}_X"], game[f"{game["current_grid"]}_O"], game[f"{game["current_grid"]}_available"])
        
        # If outcome is not None
        if game[f"{game["current_grid"]}_outcome"] is not None:
            # Remove it from the available grids
            game["available"] -= {game["current_grid"]}
            # If the game is not draw, add in the set of "X" or "O" won key
            if game[f"{game["current_grid"]}_outcome"] != 0:
                game[play].add(game["current_grid"])
                game["animation"].add(game["current_grid"])

            # Update the outcome of the small grid dictionary
            game[f"{game["current_grid"]}_outcome"] = game[f"{game["current_grid"]}_outcome"]

        # Check the main grid
        game["outcome"] = check_game(game["X"], game["O"], game["available"], True)
        

        if game["outcome"] is not None:
            """Need a grand way to announce the winner"""

            print_grid(stdscr, game, 0, game["previous_grid"], game["player_move"])
            toggle_debug(toggle_debug_, game)
            
            input_box_.erase()
            if game["outcome"] == 1:
                output_text = ( 
                "      ██╗  ██╗    ██╗    ██╗ ██████╗ ███╗   ██╗\n"
                "      ╚██╗██╔╝    ██║    ██║██╔═══██╗████╗  ██║\n"
                "       ╚███╔╝     ██║ █╗ ██║██║   ██║██╔██╗ ██║\n"
                "       ██╔██╗     ██║███╗██║██║   ██║██║╚██╗██║\n"
                "      ██╔╝ ██╗    ╚███╔███╔╝╚██████╔╝██║ ╚████║\n"
                "      ╚═╝  ╚═╝     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═══╝"
                )

            elif game["outcome"] == 2:
                output_text = ( 
                "      ██████╗    ██╗    ██╗ ██████╗ ███╗   ██╗\n"
                "     ██╔═══██╗   ██║    ██║██╔═══██╗████╗  ██║\n"
                "     ██║   ██║   ██║ █╗ ██║██║   ██║██╔██╗ ██║\n"
                "     ██║   ██║   ██║███╗██║██║   ██║██║╚██╗██║\n"
                "     ╚██████╔╝   ╚███╔███╔╝╚██████╔╝██║ ╚████║\n"
                "      ╚═════╝     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═══╝"
                )
            else:
                output_text = ( 
                "        ██████╗ ██████╗  █████╗ ██╗    ██╗\n"
                "        ██╔══██╗██╔══██╗██╔══██╗██║    ██║\n"
                "        ██║  ██║██████╔╝███████║██║ █╗ ██║\n"
                "        ██║  ██║██╔══██╗██╔══██║██║███╗██║\n"
                "        ██████╔╝██║  ██║██║  ██║╚███╔███╔╝\n"
                "        ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ "
                )
            for i in range(8):
                input_box_.addstr(7, 0, output_text, curses.color_pair(2))
                input_box_.refresh()
                time.sleep(.7)
                input_box_.clear()
                input_box_.refresh()
                time.sleep(.5)

            time.sleep(3)
            sys.exit(0)


        game["current_grid"] = game["player_move"]
        game["count"] += 1

    
        # Print the actual board
        print_grid(stdscr, game, game["current_grid"], game["previous_grid"], game["player_move"])

    


# Running the function
wrapper(main)
