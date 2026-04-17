import random #a module that will allow us to give random positions to the fruits that will spawn on the map
import curses #Library we will be handling the user interface and game mechanics

#Define the screen
s = curses.initscr()

# Set the cursor to 0 so it's invisible
curses.curs_set(0)

# Get the width and the height
sh, sw, = s.getmaxyx()

# Create a new window from the height and width at the top left corner. Sets w to modify that window
w = curses.newwin(sh, sw, 0, 0)

# Enable all keys
w.keypad(1)

# Determine how fast the snake moves
w.timeout(100)

# The snake's initial X position
snk_x = sw//4

# The snake's initial Y position
snk_y = sh//2

# Create the initial snake body parts
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]

# Set the first food item at the center of the screen
food = [sh//2, sw//2]

# Add the food to the screen
w.addch(int(food[0]), int(food[1]), curses.ACS_PI) #pi is our food

#Inital direction of the snake
key = curses.KEY_RIGHT

# Infinite loop repeating every time the snake moves
while True:
    next_key = w.getch() #gets the next key press

    #The following checks ever possibly wrong combination of snake control. This variable is a boolean!
    wrong_operation = True if (next_key==-1 or next_key==curses.KEY_DOWN and key == curses.KEY_UP\
                            or key==curses.KEY_DOWN and next_key == curses.KEY_UP \
                            or next_key==curses.KEY_LEFT and key == curses.KEY_RIGHT\
                            or key==curses.KEY_LEFT and next_key == curses.KEY_RIGHT) else False  
    #If next key is a wrong operation, keep key as the previous key. If it is a correct operation, pass the next key to key. 
    key = key if wrong_operation else next_key



    # Handle snake losing by checking if the snake hits the border. 
    if snake[0][0] <= 0 or snake[0][0] >= sh-1 or snake[0][1] <= 0 or snake[0][1] >= sw-1 or snake[0] in snake[1:]:
        # Close the curses window and exit the program
        curses.nocbreak() #Switches from game mode to terminal mode
        s.keypad(False) #Disables all key control for the snake
        curses.echo()  #Enables typing in the terminal
        curses.endwin() #Closes the window
        print("Oops, you lost!")
        break #Exits the loop



    #Makes a temp variable new head with previous head posiiton
    new_head = [snake[0][0], snake[0][1]] #[snk_y, snk_x]

    # Player presses key down
    if key == curses.KEY_DOWN:
        new_head[0] += 1 #Adds 1 to the snk_y value (moves down)
    # Player presses key up
    if key == curses.KEY_UP:
        new_head[0] -= 1 #Subtracts 1 to the snk_y value (moves up)
    # Player presses key left
    if key == curses.KEY_LEFT:
        new_head[1] -= 1 #Subtracts 1 to the snk_x value (moves left)
    # Player presses key right
    if key == curses.KEY_RIGHT: #Add 1 to the snk_x value (moves right)
        new_head[1] += 1

    # Insert the new head of the snake
    snake.insert(0, new_head) #adds a new block with the new head to the snake body. 


    # Check if the snake ran into the food
    if snake[0] == food:
        # Since the snake ate the food, we need to set a new food position
        food = None 

        while food is None:
            # Randomize the position of the new food using random library.
            nf = [ #new food =
                random.randint(1, sh-1), #1-sh1 limits the range of the randint to be within the borders
                random.randint(1, sw-1)
            ]
            # Set the new food is the new food is not in the snake. If it is the loop repeats (indentations)
            food = nf if nf not in snake else None


        # Add the new food position to the screen
        w.addch(food[0], food[1], curses.ACS_PI)
        w.refresh() #refreshes


    #Handles the snake not running into food by memoving the tail and adding the new head to the terminal
    else:
        tail = snake.pop() #Removes the last block of the snake, and gives the value to tail
        w.addch(int(tail[0]), int(tail[1]), ' ') #sets the tail to blank.

    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD) #Trys to add the new head of the snake to the terminal
