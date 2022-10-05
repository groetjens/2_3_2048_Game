import copy
import random
import itertools
import math

MAX_DEPTH = 4

WEIGHTS = [
    [-25, -10, 0, 10],
    [-10, 0, 10, 25],
    [0, 10, 25, 50],
    [10, 25, 50, 100]
]

PLAYER, CPU = 0, 1

def merge_left(b):
    # merge the board left
    # this function is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left
        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accu
        if len(row) == 1:
            return acc + [x]
        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accu, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accu, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]

def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]

def merge_down(b):
    # merge the board downward
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]

# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                # if same value or an empty cell
                if x == y or x == 0 or y == 0:
                    return True
        return False

    # check horizontally and vertically
    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b

def play_move(b, direction):
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b

def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, cols):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue
            
def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert merge_down(b) == [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [[2, 8, 4, 0], [16, 0, 2, 0], [4, 0, 0, 0], [0, 0, 0, 0]]
    assert (merge_down(b)) == [[0, 0, 0, 0], [2, 0, 0, 0], [16, 0, 4, 0], [4, 8, 2, 0]]
    assert (move_exists(b)) == True
    b = [[32, 64, 2, 16], [8, 32, 16, 2], [4, 16, 8, 4], [2, 8, 4, 2]]
    assert (move_exists(b)) == False
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    for i in range(11):
        add_two_four(b)
        print(b)

def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))


def get_expectimax_move(b):
    return expectimax(b, PLAYER, 0)[0]

# Opgave A

def expectimax(b, turn, depth):
    # wikipedia pseudocode
    # if node is a terminal node or depth = 0
    #   return the heuristic value of node
    if depth > MAX_DEPTH or not move_exists(b):
        return ("left", heuristics(b))


    # TODO THIS IS NOT USED BECAUSE THERE IS NO ADVERSARY THAT PLAYS
    # if the adversary is to play at node
    #   ###return value of minimum-valued child node
    #   alfa = math.inf
    #   for child in node:
    #       alfa = min(alfa, expectimax(child, depth - 1)


    # if we are to play at node
    #   ### return value of maximum-valued child node
    #   alfa = -math.inf
    #   for child in node:
    #   alfa = max(alfa, expectimax(child, depth -1)
    if turn == 0:
        max_move = ("none", -math.inf)
        for direction in ["left", "up", "down", "right"]:
            new_b = MERGE_FUNCTIONS[direction](b)
            if boards_equal(b, new_b) and not has_empty_spot(new_b):
                # if board is the same and no place for a new tile: move on
                continue
            new_move = (direction, expectimax(new_b, CPU, depth + 1)[1])
            if new_move[1] > max_move[1]:
                max_move = new_move
        return max_move


    # elif random event at node:
    #   return weighted average of all child nodes' values
    #   alfa = 0
    #   for child in node:
    #   alfa = alfa + (Probability[child] x expectimax(child, depth - 1)
    # return alfa

    else:
        new_b = clone_board(b)
        total = 0
        count = 0
        for x in range(4):
            for y in range(4):
                if new_b[x][y] == 0:

                    # try to place a 2
                    new_b[x][y] = 2
                    score = expectimax(new_b, PLAYER, depth + 1)[1]
                    # 90% chance to get a 2, so we weigh by multiplying by 9
                    total += score * 9

                    # Opgave B
                    # Bij Expectimax is pruning minder winstgevend dan bij Minimax
                    # Wel zou het kunnen werken als de kansen ver uit elkaar liggen
                    # Dus in theorie is de mogelijkheid op een 4 verwaarloosbaar
                    # als de kans 1:10 is. Dit zou de helft (?) schelen.

                    # try to place a 4
                    new_b[x][y] = 4
                    score = expectimax(new_b, PLAYER, depth + 1)[1]
                    # 10% chance to get a 4, so we weigh by multiplying by 1
                    total += score
                    count += 10
        if count == 0:
            total = expectimax(new_b, PLAYER, depth + 1)[1]
            count = 1
        return ("left", total / count)


def heuristics(b):
    # heuristics determines value of board by
    # value of tile * weight of tile

    value = 0
    for x in range(4):
        for y in range(4):
            value += WEIGHTS[x][y] * b[x][y]
    return value


def boards_equal(b, new_b):
    for x in range(4):
        for y in range(4):
            if b[x][y] != new_b[x][y]:
                return False
    return True


def has_empty_spot(b):
    for x in range(4):
        for y in range(4):
            if b[x][y] == 0:
                return True
    return False


def clone_board(b):
    return copy.deepcopy(b)

