from collections import deque
import copy
import time
import tracemalloc   # For memory usage tracking

# ANSI colors for terminal output
RED = "\033[91m"     # red for visited cells
GREEN = "\033[92m"   # green for solution path
RESET = "\033[0m"    # reset to default color

# Class to represent each state in the maze
class State:
    def __init__(self, x, y, path=None):
        self.x = x
        self.y = y
        self.path = path if path is not None else [(x, y)]

    def is_goal(self, goal):
        return (self.x, self.y) == goal

    def __eq__(self, other):
        return isinstance(other, State) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

# Generate successor states (up, down, left, right)
def successors(state, maze):
    rows, cols = len(maze), len(maze[0])
    moves = [(0,1), (0,-1), (1,0), (-1,0)]  # Right, Left, Down, Up
    children = []
    for dx, dy in moves:
        nx, ny = state.x + dx, state.y + dy
        if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != "#":
            new_path = state.path + [(nx, ny)]
            children.append(State(nx, ny, new_path))
    return children

# Print maze with visited (red) and solution path (green)
def print_maze(maze, visited, path):
    temp = copy.deepcopy(maze)
    for r in range(len(temp)):
        row_str = []
        for c in range(len(temp[0])):
            if (r,c) in path:
                if temp[r][c] in ["S","G"]:
                    row_str.append(GREEN + temp[r][c] + RESET)
                else:
                    row_str.append(GREEN + "•" + RESET)
            elif (r,c) in visited and temp[r][c] not in ["S","G"]:
                row_str.append(RED + "•" + RESET)
            else:
                row_str.append(temp[r][c])
        print(" ".join(row_str))
    print()

# BFS implementation
def breadth_first_search(maze, start, goal):
    initial_state = State(*start)
    if initial_state.is_goal(goal):
        return initial_state.path, {start}

    frontier = deque([initial_state])
    explored = set([initial_state])
    visited = set([start])

    while frontier:
        state = frontier.popleft()
        if state.is_goal(goal):
            return state.path, visited
        for child in successors(state, maze):
            if child not in explored:
                frontier.append(child)
                explored.add(child)
                visited.add((child.x, child.y))

    return None, visited

# ==== Maze declarations (same structure for all 10 test cases) ====
maze1 = [
    ["S","#","0","#","0","0","0","0","#","0","0","0"],
    ["0","#","0","#","#","#","0","#","#","#","0","#"],
    ["0","0","0","#","0","0","0","0","0","#","0","#"],
    ["#","#","0","#","#","#","#","#","0","#","0","#"],
    ["0","0","0","0","0","0","0","#","0","0","0","0"],
    ["0","#","#","#","#","#","#","#","#","0","#","0"],
    ["0","0","0","0","0","#","0","0","0","0","0","#"],
    ["#","#","#","#","0","#","#","#","0","#","#","0"],
    ["0","0","0","#","0","0","0","0","0","0","#","0"],
    ["0","#","#","#","#","#","#","#","0","#","#","0"],
    ["0","#","0","0","0","0","0","#","0","0","0","0"],
    ["0","0","0","#","#","#","0","0","0","#","#","0"]
]
maze2  = copy.deepcopy(maze1)
maze3  = copy.deepcopy(maze1)
maze4  = copy.deepcopy(maze1)
maze5  = copy.deepcopy(maze1)
maze6  = copy.deepcopy(maze1)
maze7  = copy.deepcopy(maze1)
maze8  = copy.deepcopy(maze1)
maze9  = copy.deepcopy(maze1)
maze10 = copy.deepcopy(maze1)

# Place goals
maze1[11][11] = "G"
maze2[0][11]  = "G"
maze3[11][0]  = "G"
maze4[0][4]   = "G"
maze5[5][11]  = "G"
maze6[8][3]   = "G"
maze7[7][11]  = "G"
maze8[0][2]   = "G"
maze9[0][7]   = "G"
maze10[4][6]  = "G"

# Start & Goal
start1,  goal1  = (0,0), (11,11)
start2,  goal2  = (0,0), (0,11)
start3,  goal3  = (0,0), (11,0)
start4,  goal4  = (0,0), (0,4)
start5,  goal5  = (0,0), (5,11)
start6,  goal6  = (0,0), (8,3)
start7,  goal7  = (0,0), (7,11)
start8,  goal8  = (0,0), (0,2)
start9,  goal9  = (0,0), (0,7)
start10, goal10 = (0,0), (4,6)

# ==== User input ====
choice = int(input("Enter test case number (1-10): "))

cases = {
    1: (maze1, start1, goal1),
    2: (maze2, start2, goal2),
    3: (maze3, start3, goal3),
    4: (maze4, start4, goal4),
    5: (maze5, start5, goal5),
    6: (maze6, start6, goal6),
    7: (maze7, start7, goal7),
    8: (maze8, start8, goal8),
    9: (maze9, start9, goal9),
    10: (maze10, start10, goal10)
}

if choice in cases:
    maze, start, goal = cases[choice]
    print(f"\n=== Running BFS on Test Case {choice} ===")

    # Measure time & memory
    tracemalloc.start()
    start_time = time.perf_counter()

    path, visited = breadth_first_search(maze, start, goal)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if path:
        print("Path length:", len(path))

        # First 5 steps (with maze print after each step)
        print("\n--- First 5 Steps ---")
        for i, step in enumerate(path[:5], 1):
            print(f"Step {i}: {step}")
            print_maze(maze, visited, path[:i])

        # Last 5 steps (with maze print after each step)
        print("\n--- Last 5 Steps ---")
        for i, step in enumerate(path[-5:], len(path)-4):
            print(f"Step {i}: {step}")
            print_maze(maze, visited, path[:i])

        # Final solution
        print("\n--- Final Solution Path (BFS) ---")
        print("Solution path coordinates:", " -> ".join([f"({coord[0]},{coord[1]})" for coord in path]))
        print(f"Total path length: {len(path)} steps")
        print("\nVisual representation:")
        print_maze(maze, visited, path)
    else:
        print("No path found.")

    # Performance report
    print("\n=== BFS Report ===")
    print(f"Initial State: {start}")
    print(f"Goal State: {goal}")
    print(f"Total Execution time: {(end_time - start_time) * 1000:.3f} ms")
    print(f"Total Memory consumption (Peak): {peak / 1024:.2f} KB")
else:
    print("Invalid test case number. Please enter 1–10.")
