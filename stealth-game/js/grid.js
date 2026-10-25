/* Grid menggunakan array 2D: 0 = lantai, 1 = tembok. */
window.GridUtils = {
  FLOOR: 0,
  WALL: 1,

  createGrid(rows) {
    return rows.map((line) => Array.from(line, (symbol) => symbol === "#" ? this.WALL : this.FLOOR));
  },

  inBounds(pos, grid) {
    return Number.isInteger(pos.row) && Number.isInteger(pos.col) &&
      pos.row >= 0 && pos.row < grid.length &&
      pos.col >= 0 && pos.col < grid[0].length;
  },

  isWalkable(pos, grid) {
    return this.inBounds(pos, grid) && grid[pos.row][pos.col] === this.FLOOR;
  },

  samePosition(a, b) {
    return a.row === b.row && a.col === b.col;
  },

  key(pos) {
    return `${pos.row},${pos.col}`;
  },

  clonePosition(pos) {
    return { row: pos.row, col: pos.col };
  },

  /* Gerakan legal hanya empat arah; posisi tujuan harus lantai yang valid. */
  canStep(from, to, grid) {
    const distance = Math.abs(from.row - to.row) + Math.abs(from.col - to.col);
    return distance === 1 && this.isWalkable(to, grid);
  },

  neighbors(pos, grid) {
    const candidates = [
      { row: pos.row - 1, col: pos.col },
      { row: pos.row + 1, col: pos.col },
      { row: pos.row, col: pos.col - 1 },
      { row: pos.row, col: pos.col + 1 }
    ];
    return candidates.filter((candidate) => this.isWalkable(candidate, grid));
  }
};
