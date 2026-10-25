window.Game = {
  state: null,
  enemyTimer: null,
  uiTimer: null,

  createState() {
    const grid = GridUtils.createGrid(GameConfig.mapRows);
    return {
      grid,
      player: GridUtils.clonePosition(GameConfig.playerStart),
      enemy: {
        pos: GridUtils.clonePosition(GameConfig.enemyStart),
        mode: "PATROL",
        visible: false,
        distance: Infinity,
        path: [],
        sightLine: [],
        patrolIndex: 0
      },
      target: GridUtils.clonePosition(GameConfig.target),
      debug: false,
      gameOver: false,
      result: null,
      message: "Cari jalan menuju exit hijau.",
      steps: 0
    };
  },

  init() {
    const canvas = document.getElementById("gameCanvas");
    canvas.width = GameConfig.mapRows[0].length * GameConfig.cellSize;
    canvas.height = GameConfig.mapRows.length * GameConfig.cellSize;

    document.getElementById("restartBtn").addEventListener("click", () => this.restart());
    document.getElementById("overlayRestartBtn").addEventListener("click", () => this.restart());
    document.getElementById("debugBtn").addEventListener("click", () => this.toggleDebug());

    window.addEventListener("keydown", (event) => {
      const key = event.key.toLowerCase();
      const movements = {
        w: [-1, 0], arrowup: [-1, 0],
        s: [1, 0], arrowdown: [1, 0],
        a: [0, -1], arrowleft: [0, -1],
        d: [0, 1], arrowright: [0, 1]
      };
      if (movements[key]) {
        event.preventDefault();
        if (event.repeat) return;
        PlayerController.move(this.state, movements[key][0], movements[key][1]);
        this.render();
      } else if (key === "r") {
        this.restart();
      } else if (key === "g") {
        this.toggleDebug();
      }
    });
    this.restart();
  },

  restart() {
    if (this.enemyTimer) clearInterval(this.enemyTimer);
    if (this.uiTimer) clearInterval(this.uiTimer);
    this.state = this.createState();
    document.getElementById("endOverlay").classList.add("hidden");
    const debugButton = document.getElementById("debugBtn");
    debugButton.textContent = "Debug: OFF";
    debugButton.setAttribute("aria-pressed", "false");
    this.render();
    this.enemyTimer = setInterval(() => {
      EnemyAI.update(this.state);
      this.render();
    }, GameConfig.enemyStepMs);
    this.uiTimer = setInterval(() => this.render(), 120);
  },

  toggleDebug() {
    this.state.debug = !this.state.debug;
    const button = document.getElementById("debugBtn");
    button.textContent = `Debug: ${this.state.debug ? "ON" : "OFF"}`;
    button.setAttribute("aria-pressed", String(this.state.debug));
    this.render();
  },

  finish(state, result) {
    if (state.gameOver) return;
    state.gameOver = true;
    state.result = result;
    state.message = result === "win" ? "Kamu berhasil mencapai exit!" : "Enemy berhasil menangkapmu.";
    const overlay = document.getElementById("endOverlay");
    const title = document.getElementById("endTitle");
    const description = document.getElementById("endDescription");
    const icon = document.getElementById("endIcon");
    title.textContent = result === "win" ? "Kamu berhasil!" : "Kamu tertangkap!";
    description.textContent = result === "win"
      ? `Kamu mencapai exit dalam ${state.steps} langkah.`
      : "Coba gunakan tembok untuk memutus garis pandang enemy.";
    icon.textContent = result === "win" ? "✓" : "!";
    icon.classList.toggle("lose", result === "lose");
    overlay.classList.remove("hidden");
  },

  render() {
    if (!this.state) return;
    Renderer.draw(this.state);
    const state = this.state;
    const sight = LineOfSight.canEnemySeePlayer(state.enemy.pos, state.player, GameConfig.sightRadius, state.grid);
    const mode = document.getElementById("enemyMode");
    mode.textContent = state.enemy.mode;
    mode.classList.toggle("chase", state.enemy.mode === "CHASE");
    mode.classList.toggle("patrol", state.enemy.mode !== "CHASE");
    document.getElementById("distanceValue").textContent = Number.isFinite(sight.distance) ? `${sight.distance.toFixed(1)} cell` : "—";
    const sightMessage = document.getElementById("sightMessage");
    sightMessage.classList.toggle("notice-alert", sight.visible);
    sightMessage.classList.toggle("notice-neutral", !sight.visible);
    sightMessage.textContent = sight.visible
      ? "BAHAYA: enemy melihat player dan sedang mengejar!"
      : "Aman sementara: player di luar radius atau terhalang tembok.";
    document.getElementById("gameMessage").textContent = state.message;
    const badge = document.getElementById("gameStatusBadge");
    badge.textContent = state.gameOver ? (state.result === "win" ? "MENANG" : "KALAH") : "BERMAIN";
    badge.classList.toggle("over", state.gameOver);
  }
};

document.addEventListener("DOMContentLoaded", () => Game.init());
