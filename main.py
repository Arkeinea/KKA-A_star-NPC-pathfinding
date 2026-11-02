import random


DIRECTIONS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

DIRECTIONS = DIRECTIONS_4

#tembok
WALL = "#"


def is_walkable(grid, position): #cek bisa non temok atau engga

    row, col = position

    return (
        0 <= row < len(grid)
        and 0 <= col < len(grid[row])
        and grid[row][col] != WALL
    )


def is_valid_step(grid, old_pos, new_pos): #valid move cek
    if not is_walkable(grid, old_pos) or not is_walkable(grid, new_pos): #ga valid
        return False

    dr = new_pos[0] - old_pos[0]
    dc = new_pos[1] - old_pos[1]

    if (dr, dc) not in DIRECTIONS: #harus salah satu dari 4 arah
        return False

    # Kalau geraknya diagonal, jangan sampai motong sudut tembok.
    # Jadi dua kotak di sampingnya juga harus kosong.
    if dr != 0 and dc != 0:
        side_1 = (old_pos[0] + dr, old_pos[1])
        side_2 = (old_pos[0], old_pos[1] + dc)

        if not (is_walkable(grid, side_1) and is_walkable(grid, side_2)):
            return False

    return True


def get_valid_neighbors(grid, position): #cek valid step dari posisi sekarang
    row, col = position
    candidates = [(row + dr, col + dc) for dr, dc in DIRECTIONS]
    return [pos for pos in candidates if is_valid_step(grid, position, pos)]




# Radius deteksi musuh
DETECTION_RADIUS = 6


def load_level(level_rows): #cek map (cell habis ini), buat nentuin posisi player, enemy dan target gitu
    if not level_rows:
        raise ValueError("Level kosong")

    width = len(level_rows[0])
    player_pos = None
    target_pos = None
    enemy_positions = []
    grid = []

    for r, row in enumerate(level_rows):
        if len(row) != width:
            raise ValueError(f"Baris {r} panjangnya beda dari baris pertama")

        cleaned = ""
        for c, ch in enumerate(row):
            if ch == "P":
                if player_pos is not None:
                    raise ValueError("Hanya boleh ada satu 'P'")
                player_pos = (r, c)
                cleaned += "."
            elif ch == "T":
                if target_pos is not None:
                    raise ValueError("Hanya boleh ada satu 'T'")
                target_pos = (r, c)
                cleaned += "."
            elif ch == "E":
                enemy_positions.append((r, c))
                cleaned += "."
            elif ch in (WALL, "."):
                cleaned += ch
            else:
                raise ValueError(f"Simbol tidak dikenal '{ch}' di {(r, c)}")
        grid.append(cleaned)

    if player_pos is None:
        raise ValueError("Level harus punya satu 'P'")
    if target_pos is None:
        raise ValueError("Level harus punya satu 'T'")

    return grid, player_pos, target_pos, enemy_positions




LEVEL_1 = [
    ".#.#.......#E....",
    "P..#....#...#...T",
    ".....#.#E.#......",
]

LEVEL_2 = [
    "P...#..........",
    ".##.#.#####.##.",
    "....#.#...#...E",
    ".##...#.#.#.##.",
    "....#...#...#E.",
    ".##.#.###.#.##.",
    "E...#.....#...T",
]

LEVEL_0 = [
    "P.............E",
    "...............",
    "..............E",
    "...............",
    "...............",
    "...............",
    "E.............T",
]

a = [
    "P........#....E",
    ".........#....#",
    ".........#...#E",
    "#####.........#",
    "...............",
    "...............",
    "E.............T",
]

b = [
    "P....#..E.....E",
    ".....#...#.E..#",
    ".........#.###E",
    "#####....#....#",
    "E..#.....#.....",
    ".#.#...........",
    "E#............T",
]



def bresenham_line(a, b): #garis lurus a-b termasuk a dan b
    r0, c0 = a
    r1, c1 = b
    dr, dc = abs(r1 - r0), abs(c1 - c0)
    sr = 1 if r0 < r1 else -1
    sc = 1 if c0 < c1 else -1
    err = dc - dr
    cells = []
    while True:
        cells.append((r0, c0))
        if (r0, c0) == (r1, c1):
            break
        e2 = 2 * err
        if e2 > -dr:
            err -= dr
            c0 += sc
        if e2 < dc:
            err += dc
            r0 += sr
    return cells


def can_see(grid, e_pos, p_pos, radius=DETECTION_RADIUS): #fungsi apa bisa lihat
    er, ec = e_pos
    pr, pc = p_pos

    #kjalo diluar radisu abaikan
    if max(abs(er - pr), abs(ec - pc)) > radius:
        return False

    #kalo didalam cek apakah kehalang tembok
    line = bresenham_line(e_pos, p_pos)
    for r, c in line[1:-1]:
        if grid[r][c] == WALL:
            return False
    return True




import heapq


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal, stats=None): #cari jalur terpendek dari start ke goal dengan A*
    start, goal = tuple(start), tuple(goal)

    # Kasus khusus
    if not is_walkable(grid, start) or not is_walkable(grid, goal):
        return None
    if start == goal:
        return [start]

    g_score = {start: 0} #cost sejauh ini
    came_from = {} #parent
    closed = set() #node yang udah di cek
    counter = 0  #urutan gitu
    open_heap = [(manhattan(start, goal), manhattan(start, goal), counter, start)] #masih open

    explored = 0
    while open_heap:
        _, _, _, current = heapq.heappop(open_heap) #f terkecil 

        if current in closed: #kalo udah di cek dan ada yg better
            continue
        closed.add(current)
        explored += 1

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            if stats is not None:
                stats["explored"] = explored
                stats["path_length"] = len(path) - 1
            return path

        for neighbor in get_valid_neighbors(grid, current):
            if neighbor in closed:
                continue
            new_g = g_score[current] + 1 #cost = 1
            if new_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = new_g
                came_from[neighbor] = current
                h = manhattan(neighbor, goal)
                counter += 1
                heapq.heappush(open_heap, (new_g + h, h, counter, neighbor))

    #kalo ga ketemu
    if stats is not None:
        stats["explored"] = explored
        stats["path_length"] = None
    return None



class Enemy: #enemy control gitu kali?
    def __init__(self, enemy_id, position, seed=None):
        self.enemy_id = enemy_id
        self.position = tuple(position)
        self.state = "PATROL"
        self.rng = random.Random(seed)

    def patrol(self, grid):
        options = get_valid_neighbors(grid, self.position)
        
        if not options:
            return "PATROL: no valid move"

        self.position = self.rng.choice(options)
        return f"PATROL: jalan ke: {self.position}."

    def chase(self, grid, path):

        if path is None or len(path) < 2:
            return "CHASE: gaada jalur A*"

        path = [tuple(cell) for cell in path]

        if path[0] != self.position:
            return "CHASE: bukan posisi enemy sekarang, jalur A* nggak valid"

        next_pos = path[1]

        #cek validitas step
        if not is_valid_step(grid, self.position, next_pos):
            return f"CHASE: jalan ke {next_pos} tidak valid atau ketutup tembok"

        self.position = next_pos
        return f"CHASE: enemy ngikutin A* ke {self.position}."

    def check_caught(self, player_position): #player gerak ke enemy
        return self.position == tuple(player_position)

    def update(self, grid, player_position, player_detected, path=None): #fungsi update kalo player udah jalan

        # Simpan posisi dan state sebelumnya buat dibandingin pas print
        before_pos = self.position
        before_state = self.state

        if self.state == "CAUGHT":
            detail = "Player tertangkap"

        elif self.check_caught(player_position):
            self.state = "CAUGHT"
            detail = "Player nguawur cik malah ke posisi enemy"

        elif player_detected: #player kedeteksi
            self.state = "CHASE"
            detail = self.chase(grid, path)

        else: #default nya bakal patroli
            self.state = "PATROL"
            detail = self.patrol(grid)

        #cek setelah enemy gerak
        if self.check_caught(player_position):
            self.state = "CAUGHT"
            detail += " PLAYER KETANGKEP!"

        #status enemy, buat debug aja sih
        print(f"[{self.enemy_id}] {before_state} -> {self.state}")
        print(f"  Posisi: {before_pos} -> {self.position}")
        print(f"  Player: {tuple(player_position)} | Kedeteksi: {player_detected}")
        print(f"  Aksi  : {detail}")

        #return status ke main
        return {
            "enemy_id": self.enemy_id,
            "position": self.position,
            "state": self.state,
            "caught": self.state == "CAUGHT",
            "description": detail,
        }

    


import io
import contextlib

#Kontrol player: 4 arah dan quit serta diam
MOVE_KEYS = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
STAY_KEY = "x"
QUIT_KEY = "q"


class Player:
    def __init__(self, position):
        self.position = tuple(position)


def get_player_move(grid, player, input_fn=input):
    while True:
        key = input_fn("Gerak (w/a/s/d, x = diam, q = keluar): ").strip().lower() #ambil input

        if key == QUIT_KEY:
            return None
        if key == STAY_KEY:
            return player.position
        if key not in MOVE_KEYS:
            print("Tombol tidak dikenal. Pakai w/a/s/d, x, atau q.")
            continue

        dr, dc = MOVE_KEYS[key]
        new_pos = (player.position[0] + dr, player.position[1] + dc)

        #cek validitas step
        if not is_valid_step(grid, player.position, new_pos):
            print("Langkah diblokir (tembok atau batas peta).")
            continue

        return new_pos



def reset_game(level_rows, num_enemies=None, seed=None): #reset, num enemies buat max, seed buat random movement (kek seed minecraft lah)

    grid, player_pos, target_pos, enemy_positions = load_level(level_rows)

    if num_enemies is not None:
        enemy_positions = enemy_positions[:num_enemies]

    enemies = [
        Enemy(f"E{i + 1}", pos, seed=None if seed is None else seed + i)
        for i, pos in enumerate(enemy_positions)
    ]
    return grid, Player(player_pos), enemies, target_pos


def check_win(player, target):
    return player.position == tuple(target)


def check_lose(player, enemies):
    return any(e.state == "CAUGHT" or e.position == player.position for e in enemies)


def enemy_turn(grid, player, enemies, radius=DETECTION_RADIUS):
    log = io.StringIO()
    with contextlib.redirect_stdout(log):
        for enemy in enemies:
            detected = can_see(grid, enemy.position, player.position, radius)
            path = astar(grid, enemy.position, player.position) if detected else None
            if path is None:
                detected = False
            enemy.update(grid, player.position, detected, path)
    return log.getvalue()



try:
    from IPython.display import clear_output
except ImportError:
    clear_output = None


def render_game(grid, player, enemies, target, turn=0, log="", clear=True):
    if clear and clear_output is not None:
        clear_output(wait=True)

    enemy_cells = {e.position for e in enemies}
    target = tuple(target)

    print(f"=== Giliran {turn} ===")
    for r, row in enumerate(grid):
        line = []
        for c, ch in enumerate(row):
            pos = (r, c)
            if pos == player.position:
                line.append("X" if pos in enemy_cells else "P")
            elif pos in enemy_cells:
                line.append("E")
            elif pos == target:
                line.append("T")
            else:
                line.append(ch)
        print(" ".join(line))
    print(f"P = player | E = enemy | T = target | {WALL} = tembok | X = tertangkap")

    if log:
        print("\n--- Aksi musuh giliran terakhir ---")
        print(log.rstrip())



def play(level_rows, num_enemies=None, seed=None, input_fn=input, show_log=True):
    """Jalankan game. Return "WIN", "LOSE", atau "QUIT"."""
    grid, player, enemies, target = reset_game(level_rows, num_enemies, seed)
    log = ""
    turn = 0

    while True:
        render_game(grid, player, enemies, target, turn, log if show_log else "")

        #player turn
        new_pos = get_player_move(grid, player, input_fn)
        if new_pos is None:
            print("Keluar dari game.")
            return "QUIT"
        player.position = new_pos
        turn += 1

        if check_win(player, target):
            render_game(grid, player, enemies, target, turn, clear=True)
            print("MENANG! Kamu sampai di target.")
            return "WIN"

        #enemy turn
        log = enemy_turn(grid, player, enemies)

        # 4. Kalah?
        if check_lose(player, enemies):
            render_game(grid, player, enemies, target, turn, log if show_log else "")
            print("KALAH! Kamu tertangkap musuh.")
            return "LOSE"

        clear_output(wait=True)


#format: play([nama level], [max enemy], [seed custom])
play(LEVEL_0, num_enemies=6)



