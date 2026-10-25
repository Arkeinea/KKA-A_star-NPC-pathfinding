/* Konfigurasi pusat: ubah ukuran grid, radius, dan interval musuh dari sini. */
window.GameConfig = {
  cellSize: 50,
  sightRadius: 6,
  enemyStepMs: 460,
  mapRows: [
    "###############",
    "#.............#",
    "#.###...###...#",
    "#...#...#.....#",
    "###.#.###.###.#",
    "#...#.....#...#",
    "#.#####.#.#.#.#",
    "#.......#...#.#",
    "#.###.###.###.#",
    "#.............#",
    "###############"
  ],
  playerStart: { row: 1, col: 1 },
  enemyStart: { row: 1, col: 13 },
  target: { row: 9, col: 13 },
  patrolWaypoints: [
    { row: 1, col: 10 },
    { row: 3, col: 11 },
    { row: 5, col: 12 },
    { row: 9, col: 11 },
    { row: 9, col: 3 },
    { row: 7, col: 6 },
    { row: 5, col: 7 }
  ]
};
