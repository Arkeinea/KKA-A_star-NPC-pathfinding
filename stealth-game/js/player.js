window.PlayerController = {
  move(state, dr, dc) {
    if (state.gameOver) return false;
    const next = { row: state.player.row + dr, col: state.player.col + dc };
    if (!GridUtils.canStep(state.player, next, state.grid)) {
      state.message = "Ada tembok atau batas map di arah itu.";
      return false;
    }
    state.player = next;
    state.steps += 1;
    state.message = "Terus cari jalan menuju exit hijau.";

    if (GridUtils.samePosition(state.player, state.enemy.pos)) {
      Game.finish(state, "lose");
    } else if (GridUtils.samePosition(state.player, state.target)) {
      Game.finish(state, "win");
    }
    return true;
  }
};
