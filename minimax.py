


def print_state(state):
    # """Prints the current state of the board / visual representation of the board."""
    for row in range(len(state)):
        for col in range(len(state)):
            if col == 2:
                print(state[row][col])
            else:
                print(state[row][col] + '|', end='')

def score_end(state):
    # """Scores the game state if the game has ended, otherwise returns None."""
    player = {'x' : 1,
              'o' : -1}
    for pl, res in player.items():
        if pl == state[0][0] and pl == state[0][1] and pl == state[0][2]: #Row
            return res
        elif pl == state[1][0] and pl == state[1][1] and pl == state[1][2]: #Row
            return res
        elif pl == state[2][0] and pl == state[2][1] and pl == state[2][2]: #Row
            return res
        elif pl == state[0][0] and pl == state[1][0] and pl == state[2][0]: #Column
            return res
        elif pl == state[0][1] and pl == state[1][1] and pl == state[2][1]: #Column
            return res
        elif pl == state[0][2] and pl == state[1][2] and pl == state[2][2]: #Column
            return res
        elif pl == state[0][0] and pl == state[1][1] and pl == state[2][2]: #Diagonal
            return res
        elif pl == state[0][2] and pl == state[1][1] and pl == state[2][0]: #Diagonal
            return res
        #Check for a draw
        elif state[0][0] != ' ' and state[0][1] != ' ' and state[0][2] != ' ' and state[1][0] != ' ' and state[1][1] != ' ' and state[1][2] != ' ' and state[2][0] != ' ' and state[2][1] != ' ' and state[2][2] != ' ':
            return 0
        else:
            continue
    return None

def play(state, row, col, player):
    # """Returns a new state after the given move has been played."""

    first_state = [[],[],[]]
    for r in range(len(state)):
        for item in range(len(state)):
            first_state[r].append(state[r][item])
    #Check if the new position is free (Should never run)
    if first_state[row][col] != ' ':
        print('This is not a legal move, try again!')
    #Change the state within the temporary list
    new_state = first_state
    new_state[row][col] = player
    new_tup = tuple([tuple(elem) for elem in new_state])
    return new_tup


def moves(state):
    """Returns the list of moves that are available from the current state."""

    #print(state)
    emp_spots = []
    for ro in range(len(state)):
        for pos in range(len(state)):
            if state[ro][pos] == ' ':
                #print((ro, pos))
                emp_spots.append((ro, pos))
            else:
                continue
    #print(emp_spots)
    return emp_spots

#This is the minimax algorithm
def score(state, player):
    """Given the game state and whose turn it is returns a tuple (estimated game score, best move to play)"""

    #This is the break case and returns the score from the end point of a branch in the recursion if the game has reached an end point
    if score_end(state) != None:
        return (score_end(state), None)

    pos_mov = moves(state)  # move(state) returns a list of tuples with all available spaces left on the board

    #Which player are we going to complete a recursion for on this play of the game?
    if player == 'x':
        branch_score = [] #array to keep a log of the end of branch scores
        place_played = [] #array to keep a log of the board place played

        #traverse all spaces on the board
        for row, col in pos_mov:
            #Returns a new state after the given move has been played
            state_new = play(state, row, col, player)
            #Next we call the recursive function with the new state and we change the player to start the route down this particular branch
            #x is the result from the recursive function, the end score of this particular branch!
            x, y = score(state_new, 'o')
            #Save this branch result in a list
            branch_score.append(x)
            #Save the position we played to give this result
            place_played.append((row, col))
            #Player x wants to get the highest possible score, so we can just take a max value of our list now the recursion is complete
            best = max(branch_score)
            #find the place that was played when we obtained this maximum result
            index = branch_score.index(best)
        return best, place_played[index]

    else: #This is practically a copy of the above for x, but we are looking to find the minimum value for player o
        branch_score = []
        place_played = []

        for row, col in pos_mov:
            state_new = play(state, row, col, player)
            x, y = score(state_new, 'x')
            branch_score.append(x)
            place_played.append((row,col))
            #Here we locate the minimum value rather than the maximum
            best = min(branch_score)
            index = branch_score.index(best)


        return best, place_played[index]

#Driver Code
#Set up a clean board and pick a random player
import random
state = ((' ',' ',' '),(' ',' ',' '),(' ',' ',' '))
pick_play = random.random()
if pick_play <= 0.5:
    player = 'x'
else:
    player = 'o'
#Print the original empty state
print_state(state)
print('')

#Run the game until the game ends...
while score_end(state) == None:
    #find out the best place to play the next move (MINIMAX)
    x, y = score(state, player)
    #x returned is the likely score and y is the tuple of the move to take
    #play the move denoted by the tuple y
    state = play(state, y[0], y[1], player)
    # new state returns a new nested tuple
    #print the new state
    print_state(state)
    print('')
    #Change the player for the next turn...
    if player == 'x':
        player = 'o'
    else:
        player = 'x'
    #Check if there is a winner and if so, print out the result
    if score_end(state) != None:
        if score_end(state) == 1:
            print('x wins the game')
        elif score_end(state) == -1:
            print('y wins the game')
        elif score_end(state) == 0:
            print('Its a Draw! ')
    else:
        continue
