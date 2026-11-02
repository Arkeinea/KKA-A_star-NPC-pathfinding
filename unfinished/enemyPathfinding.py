import pygame
import math
import sys

pygame.init()

# Konfigurasi Layar & Grid
WIDTH, HEIGHT = 600, 600
ROWS = 20
COLS = 20
CELL_SIZE = WIDTH // COLS

# Warna (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (231, 76, 60)      # Enemy / NPC
BLUE = (52, 152, 219)    # Player
GREEN = (46, 204, 113)   # Path A*
PURPLE = (155, 89, 182)  # Closed Set / Visited
ORANGE = (243, 156, 18)  # Open Set
OBSTACLE = (52, 73, 94)  # Tembok / Rintangan

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Enemy Chasing Player - The Fabrique Style")

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.is_obstacle = False

    def get_pos(self):
        return (self.row, self.col)

    def draw(self, surface):
        if self.is_obstacle:
            color = OBSTACLE
        else:
            color = WHITE
        pygame.draw.rect(surface, color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, GRAY, (self.x, self.y, CELL_SIZE, CELL_SIZE), 1)

def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_neighbors(node, grid):
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = node.row + dr, node.col + dc
        if 0 <= r < rows and 0 <= c < cols:
            if not grid[r][c].is_obstacle:
                neighbors.append(grid[r][c])
                
    return neighbors

def a_star_search(grid, start, end):
    open_set = [start]
    open_set_hash = {start}
    
    start.g = 0
    start.h = heuristic(start.get_pos(), end.get_pos())
    start.f = start.h
    
    closed_set = set()
    
    while open_set:
        # Cari node dengan f terendah
        current = min(open_set, key=lambda node: node.f)
        
        if current == end:
            # Rekonstruksi Path
            path = []
            temp = current
            while temp.parent:
                path.append(temp)
                temp = temp.parent
            path.reverse()
            return path, open_set, closed_set
            
        open_set.remove(current)
        open_set_hash.remove(current)
        closed_set.add(current)
        
        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue
                
            temp_g = current.g + 1  # Cost antar node tetangga adalah 1
            
            if neighbor not in open_set_hash:
                open_set.append(neighbor)
                open_set_hash.add(neighbor)
            elif temp_g >= neighbor.g:
                continue
                
            neighbor.parent = current
            neighbor.g = temp_g
            neighbor.h = heuristic(neighbor.get_pos(), end.get_pos())
            neighbor.f = neighbor.g + neighbor.h
            
    return [], open_set, closed_set

def make_grid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            node = Node(i, j)
            grid[i][j] = node
    return grid

def main():
    grid = make_grid()
    
    player = grid[2][2]
    enemy = grid[17][17]
    
    clock = pygame.time.Clock()
    run = True
    path = []
    
    obstacle_coords = [
        (5,5), (5,6), (5,7), (5,8), (5,9),
        (10,12), (11,12), (12,12), (13,12),
        (2,15), (3,15), (4,15), (5,15)
    ]
    for r, c in obstacle_coords:
        grid[r][c].is_obstacle = True

    while run:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                r = pos[1] // CELL_SIZE
                c = pos[0] // CELL_SIZE
                if 0 <= r < ROWS and 0 <= c < COLS:
                    node = grid[r][c]
                    if node != player and node != enemy:
                        node.is_obstacle = not node.is_obstacle
                        
            if event.type == pygame.KEYDOWN:
                pr, pc = player.row, player.col
                if event.key == pygame.K_UP and pr > 0 and not grid[pr-1][pc].is_obstacle:
                    player = grid[pr-1][pc]
                elif event.key == pygame.K_DOWN and pr < ROWS-1 and not grid[pr+1][pc].is_obstacle:
                    player = grid[pr+1][pc]
                elif event.key == pygame.K_LEFT and pc > 0 and not grid[pr][pc-1].is_obstacle:
                    player = grid[pr][pc-1]
                elif event.key == pygame.K_RIGHT and pc < COLS-1 and not grid[pr][pc+1].is_obstacle:
                    player = grid[pr][pc+1]

        for row in grid:
            for node in row:
                node.g = float('inf')
                node.f = float('inf')
                node.parent = None

        path, open_set, closed_set = a_star_search(grid, enemy, player)
        
        if path:
            # Enemy bergerak ke node pertama di path
            next_node = path[0]
            if next_node != player:
                enemy = next_node

        # --- DRAWING / RENDER ---
        win.fill(WHITE)
        
        # Gambar Grid & Obstacle
        for row in grid:
            for node in row:
                node.draw(win)
                
        # Gambar Closed Set (Visited)
        for node in closed_set:
            pygame.draw.rect(win, PURPLE, (node.x, node.y, CELL_SIZE, CELL_SIZE))
            
        for node in open_set:
            pygame.draw.rect(win, ORANGE, (node.x, node.y, CELL_SIZE, CELL_SIZE))

        for node in path:
            pygame.draw.rect(win, GREEN, (node.x, node.y, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(win, BLUE, (player.x + 2, player.y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
        pygame.draw.rect(win, RED, (enemy.x + 2, enemy.y + 2, CELL_SIZE - 4, CELL_SIZE - 4))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
