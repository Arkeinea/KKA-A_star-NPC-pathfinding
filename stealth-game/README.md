# Shadow Grid — A* Stealth Game

Prototipe game stealth 2D berbasis grid menggunakan HTML, CSS, dan JavaScript murni. Tidak membutuhkan framework atau library eksternal.

## Cara menjalankan

1. Ekstrak folder `stealth-game`.
2. Buka `index.html` di browser (Chrome atau Edge). File menggunakan script klasik, jadi tidak wajib memakai Live Server.
3. Gunakan W/A/S/D atau tombol panah untuk bergerak.
4. Tekan `G` atau tombol Debug untuk melihat radius pandang, garis LOS, dan jalur A*.
5. Tekan `R` atau tombol Restart untuk mengulang permainan.

## Cara menjalankan tes otomatis

Pastikan Node.js terpasang, buka terminal pada folder `stealth-game`, lalu jalankan:

```bash
node tests/self_test.js
```

Tes ini menguji validasi grid, batas map, gerak 4 arah, Bresenham, radius LOS, obstacle LOS, serta jalur A*.

## Struktur file

- `index.html`: struktur halaman dan urutan pemuatan script.
- `style.css`: tampilan antarmuka.
- `js/config.js`: ukuran cell, map, posisi awal, radius pandang, dan waypoint patroli.
- `js/grid.js`: array 2D, batas map, cell yang dapat dilewati, dan tetangga empat arah.
- `js/los.js`: jarak Euclidean, Bresenham, dan fungsi Line of Sight.
- `js/astar.js`: algoritma A* dan rekonstruksi jalur.
- `js/player.js`: input perpindahan player dan pemeriksaan target/tangkapan.
- `js/enemy.js`: mode PATROL/CHASE serta pergerakan enemy lewat A*.
- `js/renderer.js`: penggambaran grid, karakter, exit, dan overlay debug.
- `js/game.js`: inisialisasi, timer, UI, restart, dan kondisi menang/kalah.
- `tests/self_test.js`: tes inti algoritma yang dapat dijalankan dengan Node.js.

## Algoritma

### Grid
`0` menandakan lantai dan `1` menandakan tembok. Posisi karakter disimpan terpisah dari grid, dengan format `{ row, col }`. Gerakan hanya empat arah.

### Line of Sight
Pertama, jarak Euclidean dihitung dengan `sqrt((r1-r2)^2 + (c1-c2)^2)`. Jika lebih besar dari `sightRadius`, player tidak terlihat. Jika masih dalam radius, Bresenham menentukan urutan cell pada garis antara pusat enemy dan player. Tembok pada cell perantara menghalangi pandangan.

Untuk mencegah garis pandang melewati sudut dua cell, aturan tambahan konservatif diterapkan: pada transisi diagonal, tembok di salah satu cell samping juga dianggap menghalangi. Perilaku ini adalah keputusan desain prototipe dan dapat diubah bila kelompok menyepakati aturan lain.

### A* Pathfinding
A* menggunakan biaya langkah `g(n)`, heuristic Manhattan `h(n) = abs(row - targetRow) + abs(col - targetCol)`, dan `f(n) = g(n) + h(n)`. Setiap langkah empat arah berbiaya 1. Parent disimpan untuk merekonstruksi jalur. Untuk grid tanpa biaya tambahan, heuristic Manhattan admissible dan konsisten sehingga jalur yang ditemukan optimal.

### Enemy Behaviour
Enemy memilih mode CHASE jika player berada dalam radius serta tidak terhalang. Jika tidak, enemy bergerak menuju waypoint patroli. Langkah pergerakan enemy diperbarui oleh timer agar ia bergerak satu cell tiap tick, bukan sekali setiap frame.

## Pembagian tugas yang disarankan

- Dafa: `js/grid.js` dan `js/los.js`.
- Anggota A*: `js/astar.js`.
- Tata: `js/enemy.js`.
- Say: `js/player.js`.
- Khen Patra: integrasi, pengujian, dokumentasi, dan perbaikan.

## Referensi dan batasan

Artikel rujukan: https://pubs.ascee.org/index.php/iota/article/view/915/593

Artikel tersebut membahas penggunaan A* untuk pathfinding dalam game Construct 3. Proyek ini merupakan prototipe mandiri yang menerapkan konsep A* pada grid empat arah. Radius Euclidean dan Bresenham LOS diterapkan sebagai kebutuhan tambahan proyek; jangan menganggap detail itu berasal dari artikel tanpa verifikasi sumber.

Keterbatasan saat ini: hanya satu enemy, satu level contoh, tidak ada animasi sprite, dan enemy langsung kembali patroli ketika LOS terputus. Gerakan diproses pada level cell dan tabrakan ditentukan ketika player dan enemy menempati cell yang sama.
