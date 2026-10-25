window.EnemyAI = {
  update(state) {
    if (state.gameOver) return;
    const sight = LineOfSight.canEnemySeePlayer(
      state.enemy.pos, state.player, GameConfig.sightRadius, state.grid
    );
    state.enemy.visible = sight.visible;
    state.enemy.distance = sight.distance;
    state.enemy.sightLine = sight.line;

    let destination;
    if (sight.visible) {
      state.enemy.mode = "CHASE";
      destination = state.player;
    } else {
      state.enemy.mode = "PATROL";
      destination = GameConfig.patrolWaypoints[state.enemy.patrolIndex];
      if (GridUtils.samePosition(state.enemy.pos, destination)) {
        state.enemy.patrolIndex = (state.enemy.patrolIndex + 1) % GameConfig.patrolWaypoints.length;
        destination = GameConfig.patrolWaypoints[state.enemy.patrolIndex];
      }
    }

    const path = AStar.findPath(state.enemy.pos, destination, state.grid);
    state.enemy.path = path;
    if (path.length > 1) {
      const next = path[1];
      // Gerak hanya satu cell per tick dan tetap tunduk pada aturan grid.
      if (GridUtils.canStep(state.enemy.pos, next, state.grid)) {
        state.enemy.pos = GridUtils.clonePosition(next);
      }
    }

    if (GridUtils.samePosition(state.enemy.pos, state.player)) {
      Game.finish(state, "lose");
    }
  }
};
