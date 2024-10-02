Python 3.8.0 (v3.8.0:fa919fdf25, Oct 14 2019, 10:23:27) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> import itertools
import time

# Define knight's moves (relative row, column changes)
KNIGHT_MOVES = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                (1, 2), (1, -2), (-1, 2), (-1, -2)]

# Grid dimensions
ROWS = 6
COLS = 6

# Convert position like 'a1' to (row, col) coordinates
def position_to_coords(pos):
    rows = '123456'
    cols = 'abcdef'
    return (rows.index(pos[1]), cols.index(pos[0]))

# Convert (row, col) coordinates to position like 'a1'
def coords_to_position(coords):
    rows = '123456'
    cols = 'abcdef'
    return f"{cols[coords[1]]}{rows[coords[0]]}"

# Check if a move is within grid boundaries
def is_valid_move(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# Create the grid with values A, B, C
def create_grid(A, B, C):
    grid_template = [
        ['A', 'A', 'A', 'B', 'B', 'C'],
        ['A', 'A', 'A', 'B', 'B', 'C'],
        ['A', 'A', 'B', 'B', 'C', 'C'],
        ['A', 'A', 'B', 'B', 'C', 'C'],
        ['A', 'B', 'B', 'C', 'C', 'C'],
        ['A', 'B', 'B', 'C', 'C', 'C']
    ]
    value_map = {'A': A, 'B': B, 'C': C}
    return [[value_map[cell] for cell in row] for row in grid_template]

# Find the intermediate squares that the knight moves over
def get_intermediate_squares(start, end):
    start_row, start_col = start
    end_row, end_col = end
    # Intermediate square is halfway between the start and end
    mid_row = (start_row + end_row) // 2
    mid_col = (start_col + end_col) // 2
    return [(mid_row, mid_col)]

# DFS to find paths with the exact score using integer bitmask for visited
def dfs(grid, current_pos, end_pos, current_score, visited, path, move_count, max_moves):
    row, col = current_pos
    position_index = row * COLS + col

    # Prune if move count exceeds max_moves
    if move_count > max_moves:
        return None

    # If reached the end position, check if the score is exactly 2024
    if current_pos == end_pos:
        if current_score == 2024:
            return path[:]
        return None

    # Mark current position as visited
    visited |= (1 << position_index)
    path.append(coords_to_position(current_pos))

    # Explore all possible knight moves
    for dr, dc in KNIGHT_MOVES:
        new_row, new_col = row + dr, col + dc
        if is_valid_move(new_row, new_col):
            new_position_index = new_row * COLS + new_col

            # Get the intermediate squares
            intermediates = get_intermediate_squares(current_pos, (new_row, new_col))
            intermediate_index = intermediates[0][0] * COLS + intermediates[0][1]

            # Check if the destination or any intermediate square has been visited
            if not (visited & (1 << new_position_index)) and not (visited & (1 << intermediate_index)):
                # Get the value of the current and next cell
                current_value = grid[row][col]
                next_value = grid[new_row][new_col]

                # Calculate new score based on the move
                if current_value != next_value:
                    new_score = current_score * next_value
                else:
                    new_score = current_score + next_value

                # Prune paths that exceed the target score
                if 0 < new_score <= 2024:
                    new_visited = visited | (1 << intermediate_index) | (1 << new_position_index)
                    result = dfs(grid, (new_row, new_col), end_pos, new_score, new_visited, path, move_count + 1, max_moves)
                    if result:
                        return result

    # Backtracking
    path.pop()
    return None

# Find a path for given A, B, C values
def find_path(A, B, C, max_moves, start, end):
    grid = create_grid(A, B, C)
    start_pos = position_to_coords(start)
    end_pos = position_to_coords(end)
    initial_score = grid[start_pos[0]][start_pos[1]]
    visited = 0
    path = []
    result = dfs(grid, start_pos, end_pos, initial_score, visited, path, 0, max_moves)
    return result

# Main function to find solutions
def find_solutions(max_moves=15):
    start_time = time.time()
    best_sum = float('inf')
    best_solution = None
    combinations_checked = 0

    # Generate combinations of A, B, C in order of increasing sum
    combinations = [(A, B, C) for A in range(1, 51) for B in range(A+1, 51) for C in range(B+1, 51)]
    combinations.sort(key=lambda x: x[0] + x[1] + x[2])

    for A, B, C in combinations:
        current_sum = A + B + C
        # If we have already found a solution with a lower sum, we can stop
        if current_sum >= best_sum:
            break

        combinations_checked += 1
        if combinations_checked % 1000 == 0:
            print(f"Checked {combinations_checked} combinations...")

        path1 = find_path(A, B, C, max_moves, 'a1', 'f6')

        if path1:
            path2 = find_path(A, B, C, max_moves, 'a6', 'f1')

            if path2:
                best_sum = current_sum
                best_solution = (A, B, C, path1, path2)
                # Early termination since we cannot find a better sum
                break

    end_time = time.time()
    total_time = end_time - start_time
    return best_solution, total_time, combinations_checked

def solve_and_print():
    print("Starting the solver...")
    solution, total_time, combinations_checked = find_solutions()

    if solution:
        A, B, C, path1, path2 = solution
        print(f"\nBest solution found:")
        print(f"A = {A}, B = {B}, C = {C}")
        print(f"Sum: {A + B + C}")
        print(f"Path from a1 to f6: {' -> '.join(path1)}")
        print(f"Path from a6 to f1: {' -> '.join(path2)}")
    else:
        print("No solution found.")

    print(f"\nTotal combinations checked: {combinations_checked}")
    print(f"Total execution time: {total_time:.4f} seconds")

if __name__ == "__main__":
    solve_and_print()
