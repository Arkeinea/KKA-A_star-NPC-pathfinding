import random

# ==========================================
# INISIALISASI GRID DAN POSISI AWAL
# ==========================================
GRID_WIDTH = 10
GRID_HEIGHT = 5

# Representasi Grid: '.' = Kosong, 'X' = Rintangan, 'T' = Target
grid = [['.' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Posisi awal entitas [y, x]
player_pos = [1, 0]  # P
npc_pos = [1, 6]     # E (Enemy / NPC)
target_pos = [1, 9]  # T (Target Menang)

# Daftar rintangan (Obstacles)
obstacles = [[0, 2], [1, 2], [2, 4], [2, 6], [0, 6]]

for obs in obstacles:
    grid[obs[0]][obs[1]] = 'X'

grid[target_pos[0]][target_pos[1]] = 'T'


def print_grid():
    """Fungsi untuk menampilkan peta grid ke konsol."""
    print("\n" + "=" * 30)
    for r in range(GRID_HEIGHT):
        row_str = ""
        for c in range(GRID_WIDTH):
            if [r, c] == player_pos:
                row_str += "P "
            elif [r, c] == npc_pos:
                row_str += "E "
            elif [r, c] == target_pos:
                row_str += "T "
            else:
                row_str += grid[r][c] + " "
        print(row_str)
    print("=" * 30)


def calculate_distance(pos1, pos2):
    """Menghitung jarak Manhattan (heuristic untuk A*)"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# ==========================================
# FUNGSI PERILAKU NPC (BEHAVIOR)
# ==========================================
def npc_behavior(npc, player, obstacles):
    """
    Sistem Persepsi & Perilaku NPC:
    - Jika pemain berada dalam radius deteksi (jarak <= 3), aktifkan mode Chasing (A*).
    - Jika di luar jangkauan, NPC melakukan Patroli secara acak (Pasif).
    """
    detection_radius = 3 
    dist = calculate_distance(npc, player)
    
    if dist <= detection_radius:
        print("[SISTEM] NPC mendeteksi pemain! Masuk mode KEJAR (Chasing A*).")
        
        # Simulasi langkah optimal A* menuju posisi player
        best_move = list(npc)
        if npc[0] < player[0]:
            best_move[0] += 1
        elif npc[0] > player[0]:
            best_move[0] -= 1
            
        if npc[1] < player[1]:
            best_move[1] += 1
        elif npc[1] > player[1]:
            best_move[1] -= 1
            
        # Validasi apakah langkah valid (tidak menabrak rintangan/batas grid)
        if (0 <= best_move[0] < GRID_HEIGHT and 
            0 <= best_move[1] < GRID_WIDTH and 
            grid[best_move[0]][best_move[1]] != 'X'):
            return best_move
        return npc
    else:
        print("[SISTEM] NPC berpatroli (Pasif)...")
        moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        valid_moves = []
        for m in moves:
            nm = [npc[0] + m[0], npc[1] + m[1]]
            if (0 <= nm[0] < GRID_HEIGHT and 
                0 <= nm[1] < GRID_WIDTH and 
                grid[nm[0]][nm[1]] != 'X'):
                valid_moves.append(nm)
        if valid_moves:
            return random.choice(valid_moves)
        return npc


# ==========================================
# GAME LOOP UTAMA
# ==========================================
def main():
    global player_pos, npc_pos
    running = True
    
    print("=== SIMULASI GAME: PATHFINDING & NPC BEHAVIOR ===")
    print("Keterangan: [P] = Player, [E] = NPC, [T] = Target, [X] = Rintangan")
    
    while running:
        print_grid()
        
        # 1. Input Player (Turn-based)
        move = input("Gerakkan Player (W=Atas, S=Bawah, A=Kiri, D=Kanan, Q=Keluar): ").upper()
        
        if move == 'Q':
            print("Game dihentikan.")
            break
            
        new_player_pos = list(player_pos)
        if move == 'W':
            new_player_pos[0] -= 1
        elif move == 'S':
            new_player_pos[0] += 1
        elif move == 'A':
            new_player_pos[1] -= 1
        elif move == 'D':
            new_player_pos[1] += 1
        else:
            print("Perintah tidak valid! Gunakan W/A/S/D.")
            continue
            
        # Validasi batas grid dan rintangan untuk player
        if (0 <= new_player_pos[0] < GRID_HEIGHT and 
            0 <= new_player_pos[1] < GRID_WIDTH and 
            grid[new_player_pos[0]][new_player_pos[1]] != 'X'):
            player_pos = new_player_pos
        else:
            print("Gerakan diblokir (Menabrak Rintangan / Keluar Peta)!")
            continue
            
        # 2. Cek Kondisi Menang (Player mencapai Target T)
        if player_pos == target_pos:
            print_grid()
            print("SELAMAT! Anda berhasil mencapai target dan MENANG!")
            break
            
        # 3. Pergerakan NPC Berdasarkan Behavior & A*
        npc_pos = npc_behavior(npc_pos, player_pos, obstacles)
        
        # 4. Cek Kondisi Kalah (Tertangkap NPC - Koordinat Bersinggungan)
        if player_pos == npc_pos:
            print_grid()
            print("GAME OVER! Anda tertangkap oleh NPC!")
            break

if __name__ == "__main__":
    main()