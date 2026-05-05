import pygame
import random
import sys

CELL = 30
COLS = 10
ROWS = 20
PLAY_W = COLS * CELL
PLAY_H = ROWS * CELL
SIDE_W = 200
WIDTH = PLAY_W + SIDE_W
HEIGHT = PLAY_H
FPS = 60

BLACK = (15, 15, 20)
GRID = (40, 40, 50)
WHITE = (230, 230, 235)
GREY = (90, 90, 100)

SHAPES = {
    'I': [[(0, 1), (1, 1), (2, 1), (3, 1)],
          [(2, 0), (2, 1), (2, 2), (2, 3)],
          [(0, 2), (1, 2), (2, 2), (3, 2)],
          [(1, 0), (1, 1), (1, 2), (1, 3)]],
    'O': [[(1, 0), (2, 0), (1, 1), (2, 1)]] * 4,
    'T': [[(1, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (1, 1), (2, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (1, 2)],
          [(1, 0), (0, 1), (1, 1), (1, 2)]],
    'S': [[(1, 0), (2, 0), (0, 1), (1, 1)],
          [(1, 0), (1, 1), (2, 1), (2, 2)],
          [(1, 1), (2, 1), (0, 2), (1, 2)],
          [(0, 0), (0, 1), (1, 1), (1, 2)]],
    'Z': [[(0, 0), (1, 0), (1, 1), (2, 1)],
          [(2, 0), (1, 1), (2, 1), (1, 2)],
          [(0, 1), (1, 1), (1, 2), (2, 2)],
          [(1, 0), (0, 1), (1, 1), (0, 2)]],
    'J': [[(0, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (2, 0), (1, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (2, 2)],
          [(1, 0), (1, 1), (0, 2), (1, 2)]],
    'L': [[(2, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (1, 1), (1, 2), (2, 2)],
          [(0, 1), (1, 1), (2, 1), (0, 2)],
          [(0, 0), (1, 0), (1, 1), (1, 2)]],
}

COLORS = {
    'I': (64, 200, 230),
    'O': (240, 215, 70),
    'T': (170, 80, 200),
    'S': (90, 210, 110),
    'Z': (230, 75, 80),
    'J': (70, 110, 220),
    'L': (235, 145, 55),
}


class Piece:
    def __init__(self, kind):
        self.kind = kind
        self.rot = 0
        self.x = 3
        self.y = 0

    def cells(self, rot=None, x=None, y=None):
        rot = self.rot if rot is None else rot
        x = self.x if x is None else x
        y = self.y if y is None else y
        return [(x + cx, y + cy) for cx, cy in SHAPES[self.kind][rot % 4]]


class Bag:
    def __init__(self):
        self.queue = []

    def _refill(self):
        kinds = list(SHAPES.keys())
        random.shuffle(kinds)
        self.queue.extend(kinds)

    def next(self):
        if len(self.queue) < 2:
            self._refill()
        return self.queue.pop(0)

    def peek(self):
        if not self.queue:
            self._refill()
        return self.queue[0]


class Tetris:
    def __init__(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.bag = Bag()
        self.piece = Piece(self.bag.next())
        self.hold = None
        self.hold_used = False
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.fall_timer = 0

    def fall_speed(self):
        return max(0.05, 0.8 - (self.level - 1) * 0.07)

    def valid(self, cells):
        for x, y in cells:
            if x < 0 or x >= COLS or y >= ROWS:
                return False
            if y >= 0 and self.board[y][x] is not None:
                return False
        return True

    def lock(self):
        for x, y in self.piece.cells():
            if 0 <= y < ROWS and 0 <= x < COLS:
                self.board[y][x] = self.piece.kind
        self.clear_lines()
        self.spawn()

    def clear_lines(self):
        new_board = [row for row in self.board if any(c is None for c in row)]
        cleared = ROWS - len(new_board)
        for _ in range(cleared):
            new_board.insert(0, [None] * COLS)
        self.board = new_board
        if cleared:
            points = {1: 100, 2: 300, 3: 500, 4: 800}[cleared]
            self.score += points * self.level
            self.lines += cleared
            self.level = 1 + self.lines // 10

    def spawn(self):
        self.piece = Piece(self.bag.next())
        self.hold_used = False
        if not self.valid(self.piece.cells()):
            self.game_over = True

    def move(self, dx, dy):
        cells = self.piece.cells(x=self.piece.x + dx, y=self.piece.y + dy)
        if self.valid(cells):
            self.piece.x += dx
            self.piece.y += dy
            return True
        return False

    def rotate(self, direction=1):
        new_rot = (self.piece.rot + direction) % 4
        for kick in (0, -1, 1, -2, 2):
            cells = self.piece.cells(rot=new_rot, x=self.piece.x + kick)
            if self.valid(cells):
                self.piece.rot = new_rot
                self.piece.x += kick
                return

    def soft_drop(self):
        if self.move(0, 1):
            self.score += 1
        else:
            self.lock()

    def hard_drop(self):
        dist = 0
        while self.move(0, 1):
            dist += 1
        self.score += dist * 2
        self.lock()

    def hold_piece(self):
        if self.hold_used:
            return
        if self.hold is None:
            self.hold = self.piece.kind
            self.spawn()
        else:
            self.hold, kind = self.piece.kind, self.hold
            self.piece = Piece(kind)
        self.hold_used = True

    def ghost_y(self):
        y = self.piece.y
        while self.valid(self.piece.cells(y=y + 1)):
            y += 1
        return y

    def step(self, dt):
        if self.game_over or self.paused:
            return
        self.fall_timer += dt
        if self.fall_timer >= self.fall_speed():
            self.fall_timer = 0
            if not self.move(0, 1):
                self.lock()


def draw_cell(surface, x, y, color, ghost=False):
    rect = pygame.Rect(x, y, CELL, CELL)
    if ghost:
        pygame.draw.rect(surface, color, rect, 2)
    else:
        pygame.draw.rect(surface, color, rect)
        inner = rect.inflate(-4, -4)
        light = tuple(min(255, c + 40) for c in color)
        pygame.draw.rect(surface, light, inner, 2)


def draw_mini(surface, kind, ox, oy):
    if kind is None:
        return
    cells = SHAPES[kind][0]
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    w = max(xs) - min(xs) + 1
    h = max(ys) - min(ys) + 1
    size = 20
    px = ox + (4 * size - w * size) // 2 - min(xs) * size
    py = oy + (3 * size - h * size) // 2 - min(ys) * size
    color = COLORS[kind]
    for cx, cy in cells:
        rect = pygame.Rect(px + cx * size, py + cy * size, size, size)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, tuple(min(255, c + 40) for c in color), rect.inflate(-4, -4), 2)


def draw(screen, font, big_font, game):
    screen.fill(BLACK)

    play = pygame.Surface((PLAY_W, PLAY_H))
    play.fill(BLACK)
    for x in range(0, PLAY_W, CELL):
        pygame.draw.line(play, GRID, (x, 0), (x, PLAY_H))
    for y in range(0, PLAY_H, CELL):
        pygame.draw.line(play, GRID, (0, y), (PLAY_W, y))

    for y in range(ROWS):
        for x in range(COLS):
            kind = game.board[y][x]
            if kind:
                draw_cell(play, x * CELL, y * CELL, COLORS[kind])

    if not game.game_over:
        gy = game.ghost_y()
        for x, y in game.piece.cells(y=gy):
            if y >= 0:
                draw_cell(play, x * CELL, y * CELL, COLORS[game.piece.kind], ghost=True)
        for x, y in game.piece.cells():
            if y >= 0:
                draw_cell(play, x * CELL, y * CELL, COLORS[game.piece.kind])

    pygame.draw.rect(play, WHITE, play.get_rect(), 2)
    screen.blit(play, (0, 0))

    side_x = PLAY_W + 15
    y = 15
    title = big_font.render("TETRIS", True, WHITE)
    screen.blit(title, (side_x, y))
    y += 50

    screen.blit(font.render("SCORE", True, GREY), (side_x, y)); y += 22
    screen.blit(font.render(str(game.score), True, WHITE), (side_x, y)); y += 32
    screen.blit(font.render("LINES", True, GREY), (side_x, y)); y += 22
    screen.blit(font.render(str(game.lines), True, WHITE), (side_x, y)); y += 32
    screen.blit(font.render("LEVEL", True, GREY), (side_x, y)); y += 22
    screen.blit(font.render(str(game.level), True, WHITE), (side_x, y)); y += 32

    screen.blit(font.render("NEXT", True, GREY), (side_x, y)); y += 22
    box = pygame.Rect(side_x, y, 4 * 20 + 20, 3 * 20 + 20)
    pygame.draw.rect(screen, GRID, box, 1)
    draw_mini(screen, game.bag.peek(), side_x + 10, y + 10); y += box.height + 15

    screen.blit(font.render("HOLD", True, GREY), (side_x, y)); y += 22
    box = pygame.Rect(side_x, y, 4 * 20 + 20, 3 * 20 + 20)
    pygame.draw.rect(screen, GRID, box, 1)
    draw_mini(screen, game.hold, side_x + 10, y + 10); y += box.height + 15

    help_lines = [
        "←/→ mover",
        "↑/X rotar",
        "Z rot. izq.",
        "↓ soft drop",
        "ESPACIO drop",
        "C hold",
        "P pausa",
        "R reiniciar",
    ]
    for line in help_lines:
        screen.blit(font.render(line, True, GREY), (side_x, y))
        y += 18

    if game.paused:
        overlay = pygame.Surface((PLAY_W, PLAY_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        msg = big_font.render("PAUSA", True, WHITE)
        screen.blit(msg, msg.get_rect(center=(PLAY_W // 2, PLAY_H // 2)))

    if game.game_over:
        overlay = pygame.Surface((PLAY_W, PLAY_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        msg = big_font.render("GAME OVER", True, WHITE)
        screen.blit(msg, msg.get_rect(center=(PLAY_W // 2, PLAY_H // 2 - 20)))
        sub = font.render("Pulsa R para reiniciar", True, WHITE)
        screen.blit(sub, sub.get_rect(center=(PLAY_W // 2, PLAY_H // 2 + 20)))


def main():
    pygame.init()
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas,menlo,monospace", 18, bold=True)
    big_font = pygame.font.SysFont("consolas,menlo,monospace", 28, bold=True)

    game = Tetris()
    das_dir = 0
    das_timer = 0
    DAS = 0.15
    ARR = 0.04
    arr_timer = 0

    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Tetris()
                elif event.key == pygame.K_p and not game.game_over:
                    game.paused = not game.paused
                elif not game.game_over and not game.paused:
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                        das_dir = -1
                        das_timer = 0
                        arr_timer = 0
                    elif event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                        das_dir = 1
                        das_timer = 0
                        arr_timer = 0
                    elif event.key == pygame.K_DOWN:
                        game.soft_drop()
                    elif event.key in (pygame.K_UP, pygame.K_x):
                        game.rotate(1)
                    elif event.key == pygame.K_z:
                        game.rotate(-1)
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
                    elif event.key == pygame.K_c:
                        game.hold_piece()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and das_dir == -1:
                    das_dir = 0
                elif event.key == pygame.K_RIGHT and das_dir == 1:
                    das_dir = 0

        if das_dir != 0 and not game.game_over and not game.paused:
            das_timer += dt
            if das_timer >= DAS:
                arr_timer += dt
                while arr_timer >= ARR:
                    game.move(das_dir, 0)
                    arr_timer -= ARR

        game.step(dt)
        draw(screen, font, big_font, game)
        pygame.display.flip()


if __name__ == "__main__":
    main()
