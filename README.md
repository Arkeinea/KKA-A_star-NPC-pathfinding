GAME NPC (Non-Playable Character) Pathfinding Using A*

Program ini adalah simulasi permainan berbasis grid turn-based yang mengimplementasikan Algoritma A* (A-Star) untuk sistem pencarian jalur (pathfinding) dan navigasi Non-Playable Character (NPC) / musuh secara real-time.

Fitur & Mekanisme Utama
  1. Algoritma A* PathfindingAlgoritma A* digunakan untuk menentukan jalur terpendek dan paling     efisien bagi NPC menuju target/pemain. Penilaian jalur menggunakan rumus:
$$f(n) = g(n) + h(n)$$$
g(n)$: Total biaya perjalanan (cost) yang telah ditempuh dari titik awal.
$h(n)$: Estimasi jarak dari node saat ini ke tujuan menggunakan Manhattan Distance:
$$h(n) = \vert{}x_1 - x_2\vert{} + \vert{}y_1 - y_2\vert{}$$

  2. Sistem Persepsi (Line of Sight) & Radius Deteksi
     - Musuh memanfaatkan garis pandang (Line of Sight) dengan algoritma Bresenham's Line untuk mengecek apakah ada dinding yang menghalangi pandangan ke pemain.
     - Player hanya akan terdeteksi jika berada di dalam Radius Deteksi (DETECTION_RADIUS).
    
  3. State Machine Perilaku NPC (Behavior)
     - PATROL (Pasif): Bergerak secara acak (random move) ketika pemain di luar jangkauan
       pandang/radius.
     - CHASE (Aktif): Mengaktifkan jalur A* untuk mengejar pemain saat pemain terdeteksi.
     - CAUGHT (Tertangkap): Status tercapai apabila koordinat musuh bersinggungan langsung dengan
       posisi pemain (Game Over).
     
   4. Sistem Gameplay (Turn-Based Grid)
      - Legenda Peta:
       - P : Player
       - E : Enemy / Musuh
       - T : Target / Tujuan Akhir
       - # : Dinding / Tembok Rintangan
       - X : Player Tertangkap
      - Pergerakan terjadi secara bergantian (turn-based): Pemain bergerak 1 langkah $\rightarrow$ Seluruh Musuh memperbarui status dan bergerak 1 langkah.
      

      *Struktur Kode Program*
      _load_level()_: Membaca representasi peta dan memisahkan posisi Player (P), Target (T), serta Enemy (E)
      _is_valid_step()_ & _get_valid_neighbors()_: Memvalidasi pergerakan karakter agar tidak menembus tembok atau batas peta.
      _can_see()_ & _bresenham_line()_: Menghitung garis lurus persepsi pandangan NPC ke Player.
      _astar()_: Implementasi pencarian jalur A* menggunakan modul heapq (Priority Queue).
      _Enemy_ Class: Mengatur logika transisi status musuh (PATROL $\rightarrow$ CHASE $\rightarrow$ CAUGHT).
      _play()_: Fungsi utama untuk menjalankan game loop.


Cara Menjalankan Program
Prasyarat
Perangkat Anda perlu memiliki Python 3.x dan (opsional) environment Jupyter Notebook / VS Code. 

Langkah Eksekusi
  1. Jalankan File Script / Notebook:Buka file main.py atau ETS KKA A kel 10 Final.ipynb pada IDE Anda.
  2. Memulai Permainan:
Panggil fungsi play() dengan memilih denah level yang tersedia (misalnya LEVEL_0, LEVEL_1, LEVEL_2), jumlah musuh, dan seed acak jika diperlukan:
play(LEVEL_0, num_enemies=3)
  3. Kontrol Pemain (Input):
     w: Bergerak ke Atas
     s: Bergerak ke Bawah
     a: Bergerak ke Kiri
     d: Bergerak ke Kanan
     x: Diam / Lewati Giliran
     q: Keluar dari Permainan

Alur Keputusan Musuh (FLOWCHART SINGKAT)
<img width="317" height="620" alt="image" src="https://github.com/user-attachments/assets/059e2ea1-c0cf-4d66-ae2d-691ddf86e2b9" />

