/* Line of Sight: radius Euclidean + cell yang dilalui algoritma Bresenham. */
window.LineOfSight = {
  euclideanDistance(a, b) {
    return Math.hypot(a.row - b.row, a.col - b.col);
  },

  bresenhamLine(start, end) {
    let x0 = start.col;
    let y0 = start.row;
    const x1 = end.col;
    const y1 = end.row;
    const dx = Math.abs(x1 - x0);
    const sx = x0 < x1 ? 1 : -1;
    const dy = -Math.abs(y1 - y0);
    const sy = y0 < y1 ? 1 : -1;
    let error = dx + dy;
    const cells = [];

    while (true) {
      cells.push({ row: y0, col: x0 });
      if (x0 === x1 && y0 === y1) break;
      const twiceError = 2 * error;
      if (twiceError >= dy) {
        error += dy;
        x0 += sx;
      }
      if (twiceError <= dx) {
        error += dx;
        y0 += sy;
      }
    }
    return cells;
  },

  hasLineOfSight(enemyPos, playerPos, grid) {
    if (!GridUtils.isWalkable(enemyPos, grid) || !GridUtils.isWalkable(playerPos, grid)) return false;
    const line = this.bresenhamLine(enemyPos, playerPos);

    // Sel awal dan akhir adalah karakter, bukan obstacle perantara.
    for (let i = 1; i < line.length - 1; i += 1) {
      if (!GridUtils.isWalkable(line[i], grid)) return false;
    }

    /*
      Aturan sudut konservatif: jika garis berpindah diagonal tepat melewati
      sudut cell, tembok di salah satu sisi ikut menghalangi pandangan.
      Ini mencegah LOS 'bocor' di celah sudut dua cell.
    */
    for (let i = 1; i < line.length; i += 1) {
      const previous = line[i - 1];
      const current = line[i];
      const diagonal = previous.row !== current.row && previous.col !== current.col;
      if (diagonal) {
        const sideA = { row: previous.row, col: current.col };
        const sideB = { row: current.row, col: previous.col };
        if (!GridUtils.isWalkable(sideA, grid) || !GridUtils.isWalkable(sideB, grid)) return false;
      }
    }
    return true;
  },

  canEnemySeePlayer(enemyPos, playerPos, radius, grid) {
    if (!GridUtils.isWalkable(enemyPos, grid) || !GridUtils.isWalkable(playerPos, grid)) {
      return { visible: false, distance: Infinity, line: [] };
    }
    const distance = this.euclideanDistance(enemyPos, playerPos);
    const line = this.bresenhamLine(enemyPos, playerPos);
    if (distance > radius) return { visible: false, distance, line };
    const visible = this.hasLineOfSight(enemyPos, playerPos, grid);
    return { visible, distance, line };
  }
};
