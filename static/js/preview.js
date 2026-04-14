// Live preview of the LED matrix.
//
// Builds a grid of <div> cells once, then repaints their background-color
// from /preview/state every POLL_MS. Polling pauses when the tab is hidden.

(() => {
  const POLL_MS = 250;

  const grid = document.getElementById('previewGrid');
  if (!grid) return;

  const width  = parseInt(grid.dataset.width,  10);
  const height = parseInt(grid.dataset.height, 10);

  // Create the cells once. We reuse the same elements on every poll.
  const cells = [];
  for (let i = 0; i < width * height; i++) {
    const cell = document.createElement('div');
    cell.className = 'px';
    grid.appendChild(cell);
    cells.push(cell);
  }

  const statusEl    = document.getElementById('previewStatus');
  const statusLabel = document.getElementById('previewStatusLabel');

  function setStatus(live) {
    statusEl.classList.toggle('paused', !live);
    statusLabel.textContent = live
      ? window.PREVIEW_LABELS.live
      : window.PREVIEW_LABELS.paused;
  }

  async function poll() {
    if (document.hidden) {
      setStatus(false);
      return;
    }
    try {
      const res  = await fetch('/preview/state', { cache: 'no-store' });
      if (!res.ok) throw new Error('bad status');
      const data = await res.json();
      const px   = data.pixels || [];
      const n    = Math.min(px.length, cells.length);
      for (let i = 0; i < n; i++) {
        const [r, g, b] = px[i];
        // Only touch the DOM when the color actually changed
        const next = `rgb(${r},${g},${b})`;
        if (cells[i]._c !== next) {
          cells[i].style.backgroundColor = next;
          cells[i]._c = next;
        }
      }
      setStatus(true);
    } catch {
      setStatus(false);
    }
  }

  poll();
  setInterval(poll, POLL_MS);
})();
