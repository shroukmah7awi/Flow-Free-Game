import pygame
import sys
import random
from tkinter import messagebox, Tk
 

WIDTH, HEIGHT = 500, 500
ROWS, COLS = 5, 5
CELL_SIZE = WIDTH // COLS


BLACK  = (20, 20, 20)
WHITE  = (255, 255, 255)
GRAY   = (60, 60, 60)
RED    = (255, 50, 50)
GREEN  = (50, 255, 50)
BLUE   = (50, 50, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE]


def get_neighbors(cell):
    x, y = cell
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(dirs)
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS:
            yield (nx, ny)

def generate_full_solution():
    grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    paths = {}
    empty_cells = [(x, y) for x in range(COLS) for y in range(ROWS)]
    random.shuffle(empty_cells)

    def dfs(cell, color, path):
     
        if len(path) > 3 and random.random() < 0.3:
            return True

        for nb in get_neighbors(cell):
            nx, ny = nb
            if grid[ny][nx] is None:
                grid[ny][nx] = color
                path.append(nb)
                if dfs(nb, color, path):
                    return True
                # (Backtracking)
                path.pop()
                grid[ny][nx] = None
        return False

    for color in COLORS:
        if not empty_cells:
            return None

        
        start = None
        for c in empty_cells:
            if grid[c[1]][c[0]] is None:
                start = c
                break
        
        if not start: return None

        grid[start[1]][start[0]] = color
        path = [start]

        if dfs(start, color, path):
            paths[color] = path
            for p in path:
                if p in empty_cells:
                    empty_cells.remove(p)
        else:
            return None

    
    if any(None in row for row in grid):
        return None

    return paths

def generate_puzzle():
    while True:
        solution = generate_full_solution()
        if solution:
            dots = {color: [path[0], path[-1]] for color, path in solution.items()}
            return dots

  # main class
class FlowFree:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flow Free Advanced 🔥")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.dots_pos = generate_puzzle()
        self.paths = {col: [] for col in self.dots_pos}
        self.current_color = None
        self.is_drawing = False
        self.won = False

    def check_win(self):
        
        for col, pts in self.dots_pos.items():
            path = self.paths[col]
            if len(path) < 2: return False
            if not (pts[0] in path and pts[1] in path):
                return False

        filled_count = sum(len(path) for path in self.paths.values())
        return filled_count == ROWS * COLS

    def draw(self):
        self.screen.fill(BLACK)

        
        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

       #paths
        for col, path in self.paths.items():
            if len(path) > 1:
                points = [(p[0] * CELL_SIZE + CELL_SIZE // 2,
                           p[1] * CELL_SIZE + CELL_SIZE // 2) for p in path]
                pygame.draw.lines(self.screen, col, False, points, 12)

        #dots
        for col, pts in self.dots_pos.items():
            for x, y in pts:
                center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
                pygame.draw.circle(self.screen, col, center, CELL_SIZE // 3)
                pygame.draw.circle(self.screen, WHITE, center, CELL_SIZE // 3, 2) # إطار للنقطة

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

       
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                for col, pts in self.dots_pos.items():
                    if (mx, my) in pts:
                        self.current_color = col
                        self.paths[col] = [(mx, my)]
                        self.is_drawing = True

           
            if event.type == pygame.MOUSEMOTION and self.is_drawing:
                mx, my = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if 0 <= mx < COLS and 0 <= my < ROWS:
                    path = self.paths[self.current_color]
                    last = path[-1]

                    if abs(mx - last[0]) + abs(my - last[1]) == 1:
                       
                        if len(path) > 1 and (mx, my) == path[-2]:
                            path.pop()
                        
                        elif (mx, my) not in path:
                            
                            occupied = any((mx, my) in p for c, p in self.paths.items() if c != self.current_color)
                            if not occupied:
                                path.append((mx, my))
                              
                                if (mx, my) in self.dots_pos[self.current_color]:
                                    self.is_drawing = False

           
            if event.type == pygame.MOUSEBUTTONUP:
                self.is_drawing = False
                if self.check_win() and not self.won:
                    self.won = True
                    self.draw()
                    self.show_win_message()
         #R
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()

    def show_win_message(self):
        root = Tk()
        root.withdraw()
        messagebox.showinfo("🎉 You Win!", "Perfect!\nPuzzle Solved ✔️\nNo intersections ✔️")
        root.destroy()
        self.reset_game()

    def run(self):
        while True:
            self.draw()
            self.handle_events()
            self.clock.tick(60)

if __name__ == "__main__":
    game = FlowFree()
    game.run()