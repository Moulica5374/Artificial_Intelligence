import argparse
import heapq
import time
from collections import deque
from pathlib import Path


# Define board size
N = 3

timeout = 900  # 15 minutes in seconds

# Define goal state
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Helper function to find the coordinates of a value in the board
def find_coord(board, value):
    for i in range(N):
        for j in range(N):
            if board[i][j] == value:
                return i, j

# Helper function to calculate Manhattan distance heuristic
def manhattan_distance(board):
    distance = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != 0:
                x_goal, y_goal = find_coord(goal_state, board[i][j])
                distance += abs(i - x_goal) + abs(j - y_goal)
    return distance

# Helper function to calculate Euclidean distance heuristic
def euclidean_distance(board):
    distance = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != 0:
                x_goal, y_goal = find_coord(goal_state, board[i][j])
                distance += ((i - x_goal) ** 2 + (j - y_goal) ** 2) ** 0.5
    return distance

# Helper function to calculate misplaced tile heuristic
def misplaced_tile(board):
    count = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != goal_state[i][j]:
                count += 1
    return count

# Helper function to get possible moves from a given state
def get_possible_moves(board):
    moves = []
    x, y = find_coord(board, 0)  # Find the empty tile

    if x > 0:
        moves.append('U')
    if x < N - 1:
        moves.append('D')
    if y > 0:
        moves.append('L')
    if y < N - 1:
        moves.append('R')

    return moves

# Helper function to apply a move to a board
def apply_move(board, move):
    x, y = find_coord(board, 0)
    new_board = [row[:] for row in board]

    if move == 'U':
        new_board[x][y], new_board[x - 1][y] = new_board[x - 1][y], new_board[x][y]
    elif move == 'D':
        new_board[x][y], new_board[x + 1][y] = new_board[x + 1][y], new_board[x][y]
    elif move == 'L':
        new_board[x][y], new_board[x][y - 1] = new_board[x][y - 1], new_board[x][y]
    elif move == 'R':
        new_board[x][y], new_board[x][y + 1] = new_board[x][y + 1], new_board[x][y]

    return new_board

# Helper function to check if a board is the goal state
def is_goal(board):
    return board == goal_state

def bfs(initial_state, timeout):
    start_time = time.time()
    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        if time.time() - start_time > timeout:
            return None, len(visited), "Timeout"
        state, path = queue.popleft()
        visited.add(tuple(map(tuple, state)))

        if is_goal(state):
            return path, len(visited), time.time() - start_time

        for move in get_possible_moves(state):
            new_state = apply_move(state, move)
            if tuple(map(tuple, new_state)) not in visited:
                queue.append((new_state, path + [move]))

# Iterative Deepening Depth-First Search (IDDFS)
def iddfs(initial_state, timeout):
    start_time = time.time()

    def dfs(state, path, depth_limit):
        if time.time() - start_time > timeout:
            return None, len(visited), "Timeout"
        if is_goal(state):
            return path, len(visited), time.time() - start_time

        if depth_limit == 0:
            return None, len(visited), time.time() - start_time

        for move in get_possible_moves(state):
            new_state = apply_move(state, move)
            if tuple(map(tuple, new_state)) not in visited:
                visited.add(tuple(map(tuple, new_state)))
                result, visited_count, elapsed_time = dfs(new_state, path + [move], depth_limit - 1)
                if result:
                    return result, visited_count, elapsed_time

        return None, len(visited), time.time() - start_time

    for depth_limit in range(100):
        visited = set()
        result, visited_count, elapsed_time = dfs(initial_state, [], depth_limit)
        if result:
            return result, visited_count, elapsed_time

# A* Search
def astar(initial_state, heuristic, timeout):
    start_time = time.time()

    def heuristic_cost(state):
        if heuristic == 'manhattan':
            return manhattan_distance(state)
        elif heuristic == 'euclidean':
            return euclidean_distance(state)
        elif heuristic == 'misplaced':
            return misplaced_tile(state)

    priority_queue = [(heuristic_cost(initial_state), 0, initial_state, [])]
    visited = set()

    while priority_queue:
        if time.time() - start_time > timeout:
            return None, len(visited), "Timeout"
        _, cost, state, path = heapq.heappop(priority_queue)
        visited.add(tuple(map(tuple, state)))

        if is_goal(state):
            return path, len(visited), time.time() - start_time

        for move in get_possible_moves(state):
            new_state = apply_move(state, move)
            if tuple(map(tuple, new_state)) not in visited:
                new_cost = cost + 1
                heapq.heappush(priority_queue, (new_cost + heuristic_cost(new_state), new_cost, new_state, path + [move]))

def file_reader(fPath):
    initial_board = []
    try:
        with open(fPath, 'r') as file:
            for line in file:
                print(line.strip())
                sub_number_list = []
                for number in line.split(' '):
                    if number == '_':
                        sub_number_list.append(0)
                    elif number == '_\n':
                        sub_number_list.append(0)
                    else:
                        sub_number_list.append(int(number))
                initial_board.append(sub_number_list)
        return initial_board
    except FileNotFoundError:
        print(f'The file {args.fPath} does not exist.')
    except Exception as e:
        print(f'An error occurred: {e}')


def list_absolute_paths(directory_path):
    try:
        directory = Path(directory_path)

        # Get a list of absolute paths for all files in the directory
        absolute_paths = [file.resolve() for file in directory.iterdir() if file.is_file()]

        return absolute_paths
    except FileNotFoundError:
        print(f'The directory {directory_path} does not exist.')
    except Exception as e:
        print(f'An error occurred: {e}')


def get_args():
    parser = argparse.ArgumentParser(description='Process arguments for Search algorithms')
    group_dir = parser.add_mutually_exclusive_group(required=False)

    parser.add_argument('--fPath', type=Path, help='file path to read the input state')
    parser.add_argument('--alg', type=str, help='Algorithm to run. BFS/IDS/h1/h2/h3')

    group_dir.add_argument('--dir', type=Path, help='Provide a directory path to run all Algs on tests in dir')
    return parser.parse_args()


def run_all_algorithms(initial_board, bt, dt, h1t, h2t, h3t, bn, dn, h1n, h2n, h3n):
    # BFS
    try :
        bfs_result, bfs_visited, bfs_time = bfs(initial_board, timeout)
        if bfs_result:
            print("BFS Path:", bfs_result)
            print("BFS States Visited:", bfs_visited)
            print("BFS Time Taken:", bfs_time)
            bt = bt + bfs_time
            bn = bn + bfs_visited
        else:
            print("BFS: Execution exceeded 15 minutes")
    except:
        pass

    # Iterative DFS
    try:
        iddfs_result, iddfs_visited, iddfs_time = iddfs(initial_board, timeout)
        if iddfs_result:
            print("IDDFS Path:", iddfs_result)
            print("IDDFS States Visited:", iddfs_visited)
            print("IDDFS Time Taken:", iddfs_time)
            dt = dt + iddfs_time
            dn = dn + iddfs_visited
        else:
            print("IDDFS: Execution exceeded 15 minutes")
    except:
        pass


    # A* with Misplaced tile heuristic
    try:
        astar_misplaced_result, astar_misplaced_visited, astar_misplaced_time = astar(initial_board, 'misplaced', timeout)
        if astar_misplaced_result:
            print("A* (Misplaced) Path:", astar_misplaced_result)
            print("A* (Misplaced) States Visited:", astar_misplaced_visited)
            print("A* (Misplaced) Time Taken:", astar_misplaced_time)
            h1t = h1t + astar_misplaced_time
            h1n = h1n + astar_misplaced_visited
        else:
            print("A* (Misplaced): Execution exceeded 15 minutes")
    except:
        pass

    # A* with Manhattan distance heuristic
    try:
        astar_manhattan_result, astar_manhattan_visited, astar_manhattan_time = astar(initial_board, 'manhattan',
                                                                                      timeout)
        if astar_manhattan_result:
            print("A* (Manhattan) Path:", astar_manhattan_result)
            print("A* (Manhattan) States Visited:", astar_manhattan_visited)
            print("A* (Manhattan) Time Taken:", astar_manhattan_time)
            h2t = h2t + astar_manhattan_time
            h2n = h2n + astar_manhattan_visited
        else:
            print("A* (Manhattan): Execution exceeded 15 minutes")
    except:
        pass

        # A* with Euclidean distance heuristic
    try:
        astar_euclidean_result, astar_euclidean_visited, astar_euclidean_time = astar(initial_board, 'euclidean', timeout)
        if astar_euclidean_result:
            print("A* (Euclidean) Path:", astar_euclidean_result)
            print("A* (Euclidean) States Visited:", astar_euclidean_visited)
            print("A* (Euclidean) Time Taken:", astar_euclidean_time)
            h3t = h3t + astar_euclidean_time
            h3n = h3n + astar_euclidean_visited
        else:
            print("A* (Euclidean): Execution exceeded 15 minutes")
    except:
        pass

    return bt, dt, h1t, h2t, h3t, bn, dn, h1n, h2n, h3n


def count_inversions(arr):
    count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                count += 1
    return count


if __name__ == "__main__":
    args = get_args()
    if args.dir:
        files_in_directory = list_absolute_paths(args.dir)
        bt = 0
        dt = 0
        h1t = 0
        h2t = 0
        h3t = 0
        bn = 0
        dn = 0
        h1n = 0
        h2n = 0
        h3n = 0
        print(files_in_directory)
        num_of_files = len(files_in_directory)
        for file in files_in_directory:
            initial_board = file_reader(file)
            bt, dt, h1t, h2t, h3t, bn, dn, h1n, h2n, h3n = \
                run_all_algorithms(initial_board, bt, dt, h1t, h2t, h3t, bn, dn, h1n, h2n, h3n)

        print(f"BFS Avg time: {bt/num_of_files}" )
        print(f"BFS Avg nodes: {bn / num_of_files}")
        print(f"DFS Avg time: {dt/num_of_files}")
        print(f"DFS Avg nodes: {dn / num_of_files}")
        print(f"H1 Avg time: {h1t/num_of_files}")
        print(f"H1 Avg ndoes: {h1n / num_of_files}")
        print(f"H2 Avg time: {h2t/num_of_files}")
        print(f"H2 Avg ndoes: {h2n / num_of_files}")
        print(f"H3 Avg time: {h3t/num_of_files}")
        print(f"H3 Avg ndoes: {h3n / num_of_files}")
    else:
        initial_board = file_reader(args.fPath)
        print(initial_board)

        if args.alg == 'BFS':
            # BFS
            bfs_result, bfs_visited, bfs_time = bfs(initial_board, timeout)
            if bfs_result:
                print("BFS Path:", bfs_result)
                print("BFS States Visited:", bfs_visited)
                print("BFS Time Taken:", bfs_time)
            else:
                print("BFS: Execution exceeded 15 minutes")
        elif args.alg == 'IDS':
            # Iterative DFS
            iddfs_result, iddfs_visited, iddfs_time = iddfs(initial_board, timeout)
            if iddfs_result:
                print("IDDFS Path:", iddfs_result)
                print("IDDFS States Visited:", iddfs_visited)
                print("IDDFS Time Taken:", iddfs_time)
            else:
                print("IDDFS: Execution exceeded 15 minutes")
        elif args.alg == 'h1':
            # A* with Misplaced tile heuristic
            astar_misplaced_result, astar_misplaced_visited, astar_misplaced_time = astar(initial_board, 'misplaced',
                                                                                          timeout)
            if astar_misplaced_result:
                print("A* (Misplaced) Path:", astar_misplaced_result)
                print("A* (Misplaced) States Visited:", astar_misplaced_visited)
                print("A* (Misplaced) Time Taken:", astar_misplaced_time)
            else:
                print("A* (Misplaced): Execution exceeded 15 minutes")
        elif args.alg == 'h2':
            # A* with Manhattan distance heuristic
            astar_manhattan_result, astar_manhattan_visited, astar_manhattan_time = astar(initial_board, 'manhattan',
                                                                                          timeout)
            if astar_manhattan_result:
                print("A* (Manhattan) Path:", astar_manhattan_result)
                print("A* (Manhattan) States Visited:", astar_manhattan_visited)
                print("A* (Manhattan) Time Taken:", astar_manhattan_time)
            else:
                print("A* (Manhattan): Execution exceeded 15 minutes")
        elif args.alg == 'h3':
            # A* with Euclidean distance heuristic
            astar_euclidean_result, astar_euclidean_visited, astar_euclidean_time = astar(initial_board, 'euclidean',
                                                                                          timeout)
            if astar_euclidean_result:
                print("A* (Euclidean) Path:", astar_euclidean_result)
                print("A* (Euclidean) States Visited:", astar_euclidean_visited)
                print("A* (Euclidean) Time Taken:", astar_euclidean_time)
            else:
                print("A* (Euclidean): Execution exceeded 15 minutes")
        else:
            print('Please select a valid algorithm BFS/IDS/h1/h2/h3')
