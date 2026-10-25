window.Renderer = {
  draw(state) {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const cell = GameConfig.cellSize;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#0a1120";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const sight = LineOfSight.canEnemySeePlayer(state.enemy.pos, state.player, GameConfig.sightRadius, state.grid);
    state.enemy.visible = sight.visible;
    state.enemy.distance = sight.distance;
    state.enemy.sightLine = sight.line;

    for (let row = 0; row < state.grid.length; row += 1) {
      for (let col = 0; col < state.grid[row].length; col += 1) {
        const x = col * cell;
        const y = row * cell;
        if (state.grid[row][col] === GridUtils.WALL) {
          ctx.fillStyle = "#263750";
          ctx.fillRect(x + 1, y + 1, cell - 2, cell - 2);
          ctx.fillStyle = "#344864";
          ctx.fillRect(x + 4, y + 4, cell - 8, 4);
        } else {
          ctx.fillStyle = "#101b2d";
          ctx.fillRect(x + 1, y + 1, cell - 2, cell - 2);
          ctx.strokeStyle = "rgba(112, 137, 173, 0.11)";
          ctx.strokeRect(x + 0.5, y + 0.5, cell, cell);
        }
      }
    }

    // Gambar radius setelah grid agar lingkaran tidak tertutup lantai/tembok.
    if (state.debug) {
      const centerX = (state.enemy.pos.col + 0.5) * cell;
      const centerY = (state.enemy.pos.row + 0.5) * cell;
      ctx.beginPath();
      ctx.arc(centerX, centerY, GameConfig.sightRadius * cell, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(251, 191, 36, 0.07)";
      ctx.fill();
      ctx.strokeStyle = "rgba(251, 191, 36, 0.5)";
      ctx.setLineDash([7, 6]);
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Jalur A* enemy.
    if (state.debug && state.enemy.path && state.enemy.path.length > 1) {
      ctx.beginPath();
      ctx.setLineDash([5, 5]);
      ctx.strokeStyle = "#5eead4";
      ctx.lineWidth = 3;
      state.enemy.path.forEach((pos, index) => {
        const x = (pos.col + 0.5) * cell;
        const y = (pos.row + 0.5) * cell;
        if (index === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      });
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Garis Bresenham menuju player saat debug aktif.
    if (state.debug && sight.line.length > 0) {
      ctx.beginPath();
      ctx.moveTo((state.enemy.pos.col + 0.5) * cell, (state.enemy.pos.row + 0.5) * cell);
      ctx.lineTo((state.player.col + 0.5) * cell, (state.player.row + 0.5) * cell);
      ctx.strokeStyle = sight.visible ? "#fb7185" : "#fbbf24";
      ctx.lineWidth = 2;
      ctx.stroke();
      for (const pos of sight.line) {
        ctx.fillStyle = sight.visible ? "rgba(251,113,133,.55)" : "rgba(251,191,36,.45)";
        ctx.fillRect(pos.col * cell + cell * 0.37, pos.row * cell + cell * 0.37, cell * 0.26, cell * 0.26);
      }
    }

    this.drawMarker(ctx, state.target, cell, "#a3e635", "EXIT", "#17270b");
    this.drawCharacter(ctx, state.player, cell, "#60a5fa", "P");
    this.drawCharacter(ctx, state.enemy.pos, cell, "#fb7185", "E");
  },

  drawCharacter(ctx, pos, cell, color, label) {
    const x = (pos.col + 0.5) * cell;
    const y = (pos.row + 0.5) * cell;
    ctx.beginPath();
    ctx.arc(x, y, cell * 0.31, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.shadowColor = color;
    ctx.shadowBlur = 12;
    ctx.fill();
    ctx.shadowBlur = 0;
    ctx.fillStyle = "#07101e";
    ctx.font = `900 ${Math.round(cell * 0.31)}px system-ui`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, x, y + 1);
  },

  drawMarker(ctx, pos, cell, color, label, textColor) {
    const x = pos.col * cell + cell * 0.17;
    const y = pos.row * cell + cell * 0.17;
    ctx.fillStyle = color;
    ctx.globalAlpha = 0.9;
    ctx.fillRect(x, y, cell * 0.66, cell * 0.66);
    ctx.globalAlpha = 1;
    ctx.fillStyle = textColor;
    ctx.font = `900 ${Math.round(cell * 0.18)}px system-ui`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, x + cell * 0.33, y + cell * 0.33);
  }
};
