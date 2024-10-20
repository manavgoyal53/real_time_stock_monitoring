class LoopPuzzleSolver:
    def __init__(self, grid):
        self.grid = grid
        self.N = len(grid)
        self.edges = [[0] * (self.N * 2 + 1) for _ in range(self.N * 2 + 1)]  # Edge matrix to track horizontal and vertical edges
        self.visited = [[False] * (self.N * 2 + 1) for _ in range(self.N * 2 + 1)]  # For DFS path traversal

    def is_valid(self, x, y):
        """ Check if the current point is within grid bounds """
        return 0 <= x < self.N * 2 + 1 and 0 <= y < self.N * 2 + 1

    def can_place_edge(self, x, y, nx, ny):
        """ Check if placing an edge is valid based on the number constraints """
        if self.edges[x][y] == 1 or self.edges[nx][ny] == 1:
            return False  # Edge already exists
        # Ensure we're not placing edges where it violates the number constraints
        if x % 2 == 1 and y % 2 == 1:  # Skip cells that are numbers, only place edges between dots
            return False
        return True

    def dfs(self, x, y, start_x, start_y):
        """ Depth First Search to build a valid loop """
        if (x, y) == (start_x, start_y) and self.is_loop_complete():
            return True

        self.visited[x][y] = True

        # Try moving in four directions (right, down, left, up)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny) and not self.visited[nx][ny]:
                if self.can_place_edge(x, y, nx, ny):
                    self.edges[x][y] = 1  # Place edge
                    if self.dfs(nx, ny, start_x, start_y):
                        return True
                    self.edges[x][y] = 0  # Backtrack
        self.visited[x][y] = False
        return False

    def is_loop_complete(self):
        """ Check if the loop satisfies all conditions and is complete """
        # Check all numbers in the grid
        for i in range(self.N):
            for j in range(self.N):
                if not self.check_number_constraints(i, j):
                    return False
        return True

    def check_number_constraints(self, x, y):
        """ Check if the edges around a cell satisfy the number constraints """
        count = 0
        # Count number of edges around cell (x, y)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x * 2 + dx, y * 2 + dy
            if self.is_valid(nx, ny) and self.edges[nx][ny] == 1:
                count += 1
        return count == self.grid[x][y]

    def solve(self):
        """ Attempt to solve the puzzle starting from an arbitrary point """
        start_x, start_y = 0, 0  # Arbitrary starting point
        if self.dfs(start_x * 2, start_y * 2, start_x * 2, start_y * 2):
            print("Loop completed")
        else:
            print("No solution found")


# Example grid
grid = [
    [3, 0, 2, 0, 3],
    [2, 1, 1, 0, 2],
    [3, 0, 2, 3, 2],
    [3, 1, 1, 2, 2],
    [2, 2, 2, 2, 1]
]

solver = LoopPuzzleSolver(grid)
solver.solve()


