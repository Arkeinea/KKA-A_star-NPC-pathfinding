/* A* empat arah dengan biaya langkah 1 dan heuristic Manhattan. */
window.AStar = {
  heuristic(a, b) {
    return Math.abs(a.row - b.row) + Math.abs(a.col - b.col);
  },

  findPath(start, goal, grid) {
    if (!GridUtils.isWalkable(start, grid) || !GridUtils.isWalkable(goal, grid)) return [];
    if (GridUtils.samePosition(start, goal)) return [GridUtils.clonePosition(start)];

    const open = [{ ...GridUtils.clonePosition(start), g: 0, f: this.heuristic(start, goal) }];
    const openKeys = new Set([GridUtils.key(start)]);
    const cameFrom = new Map();
    const gScore = new Map([[GridUtils.key(start), 0]]);
    const closed = new Set();

    while (open.length > 0) {
      open.sort((a, b) => a.f - b.f || a.g - b.g);
      const current = open.shift();
      const currentKey = GridUtils.key(current);
      openKeys.delete(currentKey);

      if (closed.has(currentKey)) continue;
      if (current.g !== gScore.get(currentKey)) continue;

      if (GridUtils.samePosition(current, goal)) {
        const path = [GridUtils.clonePosition(current)];
        let key = currentKey;
        while (cameFrom.has(key)) {
          const previous = cameFrom.get(key);
          path.push(previous.pos);
          key = previous.key;
        }
        path.reverse();
        return path;
      }

      closed.add(currentKey);
      for (const neighbor of GridUtils.neighbors(current, grid)) {
        const neighborKey = GridUtils.key(neighbor);
        if (closed.has(neighborKey)) continue;
        const tentativeG = gScore.get(currentKey) + 1;
        const bestG = gScore.get(neighborKey);
        if (bestG !== undefined && tentativeG >= bestG) continue;

        cameFrom.set(neighborKey, { key: currentKey, pos: GridUtils.clonePosition(current) });
        gScore.set(neighborKey, tentativeG);
        const f = tentativeG + this.heuristic(neighbor, goal);
        if (!openKeys.has(neighborKey)) {
          open.push({ ...GridUtils.clonePosition(neighbor), g: tentativeG, f });
          openKeys.add(neighborKey);
        } else {
          // Perbarui record yang sudah ada di OPEN.
          const existing = open.find((node) => GridUtils.key(node) === neighborKey);
          if (existing) { existing.g = tentativeG; existing.f = f; }
        }
      }
    }
    return [];
  }
};
