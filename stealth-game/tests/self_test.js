/* Tes sederhana yang bisa dijalankan dengan: node tests/self_test.js */
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const root = path.join(__dirname, '..');
global.window = global;
for (const file of ['config.js', 'grid.js', 'los.js', 'astar.js']) {
  vm.runInThisContext(fs.readFileSync(path.join(root, 'js', file), 'utf8'), { filename: file });
}
let passed = 0;
function check(name, condition) {
  if (!condition) {
    console.error(`FAIL: ${name}`);
    process.exitCode = 1;
  } else {
    passed += 1;
    console.log(`PASS: ${name}`);
  }
}
const grid = GridUtils.createGrid(GameConfig.mapRows);
check('posisi lantai valid', GridUtils.isWalkable({ row: 1, col: 1 }, grid));
check('posisi tembok tidak bisa dilewati', !GridUtils.isWalkable({ row: 0, col: 0 }, grid));
check('posisi luar map ditolak', !GridUtils.inBounds({ row: -1, col: 2 }, grid));
check('gerak diagonal ditolak', !GridUtils.canStep({ row: 1, col: 1 }, { row: 2, col: 2 }, grid));
const line = LineOfSight.bresenhamLine({ row: 1, col: 1 }, { row: 1, col: 5 });
check('Bresenham horizontal berisi semua cell', line.length === 5 && line[2].col === 3);
const clearGrid = Array.from({ length: 7 }, () => Array(7).fill(GridUtils.FLOOR));
check('LOS tanpa tembok terlihat', LineOfSight.canEnemySeePlayer({ row: 1, col: 1 }, { row: 1, col: 4 }, 5, clearGrid).visible);
check('LOS di luar radius tidak terlihat', !LineOfSight.canEnemySeePlayer({ row: 1, col: 1 }, { row: 1, col: 6 }, 3, clearGrid).visible);
clearGrid[1][2] = GridUtils.WALL;
check('LOS terhalang tembok tidak terlihat', !LineOfSight.canEnemySeePlayer({ row: 1, col: 1 }, { row: 1, col: 4 }, 5, clearGrid).visible);
const pathFound = AStar.findPath({ row: 1, col: 1 }, { row: 9, col: 13 }, grid);
check('A* menemukan jalur pada map game', pathFound.length > 0);
check('jalur A* dimulai dan berakhir tepat', pathFound.length > 0 && GridUtils.samePosition(pathFound[0], { row: 1, col: 1 }) && GridUtils.samePosition(pathFound[pathFound.length - 1], { row: 9, col: 13 }));
check('A* jalur empat arah saja', pathFound.length > 1 && pathFound.every((pos, i) => i === 0 || Math.abs(pos.row - pathFound[i - 1].row) + Math.abs(pos.col - pathFound[i - 1].col) === 1));
check('A* start sama goal', AStar.findPath({ row: 1, col: 1 }, { row: 1, col: 1 }, grid).length === 1);
const blockedGrid = [[0, 1, 0], [1, 1, 1], [0, 1, 0]];
check('A* melaporkan jalur tidak tersedia', AStar.findPath({ row: 0, col: 0 }, { row: 2, col: 2 }, blockedGrid).length === 0);
console.log(`\n${passed} tes lulus.`);
if (process.exitCode) process.exit(process.exitCode);
