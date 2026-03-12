/**
 * main.js — 30×30 pixel-art editor for the draw page.
 *
 * Responsibilities:
 *  - Render the canvas and grid lines
 *  - Handle mouse and touch input (draw, erase, pan modes)
 *  - Brush size and zoom controls
 *  - Debounce canvas changes and send pixel data to /sendtoboard
 *  - Save/load drawings to the server (/draw/save, /draw/list)
 *  - Load images from local files or from the Pi file browser
 */

const PAINT = 'Drawing';
const ERASE = 'Erasing';
const PAN   = 'Panning';
let gridTileMode = PAINT;

const rows    = 30;
const columns = 30;
const cells   = new Array(rows * columns).fill('#000000');

const canvas      = document.getElementById('pixelCanvas');
const ctx         = canvas.getContext('2d');
const colorPicker = document.getElementById('colorPicker');
const tileMode    = document.getElementById('modeDisplay');

const MIN_ZOOM    = 1;
const MAX_ZOOM    = 5;
const DEBOUNCE_MS = 150;

let isDrawing = false;
let cellSize;
let brushSize  = 1;
let zoomLevel  = 1;
let panMode    = false;
let sendTimer  = null;

// --- Canvas sizing ---
function resizeCanvas() {
    const wrapper = document.getElementById('canvasWrapper');
    const baseSize = wrapper.clientWidth;
    const size = baseSize * zoomLevel;
    canvas.width  = size;
    canvas.height = size;
    cellSize = size / columns;
    render();
}

// --- Render all cells + grid lines ---
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < columns; c++) {
            ctx.fillStyle = cells[r * columns + c];
            ctx.fillRect(c * cellSize, r * cellSize, cellSize, cellSize);
        }
    }

    if (cellSize >= 4) {
        ctx.strokeStyle = '#555';
        ctx.lineWidth   = 0.5;
        for (let r = 0; r <= rows; r++) {
            ctx.beginPath();
            ctx.moveTo(0, r * cellSize);
            ctx.lineTo(canvas.width, r * cellSize);
            ctx.stroke();
        }
        for (let c = 0; c <= columns; c++) {
            ctx.beginPath();
            ctx.moveTo(c * cellSize, 0);
            ctx.lineTo(c * cellSize, canvas.height);
            ctx.stroke();
        }
    }
}

// --- Convert canvas coords to cell ---
function getCellAt(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const col  = Math.floor((clientX - rect.left) / (rect.width / columns));
    const row  = Math.floor((clientY - rect.top)  / (rect.height / rows));
    if (col < 0 || col >= columns || row < 0 || row >= rows) return null;
    return { row, col };
}

// --- Paint with brush ---
function paintAt(clientX, clientY) {
    const cell = getCellAt(clientX, clientY);
    if (!cell) return;

    const color = gridTileMode === PAINT ? colorPicker.value : '#000000';
    const half  = Math.floor(brushSize / 2);

    for (let dr = -half; dr < brushSize - half; dr++) {
        for (let dc = -half; dc < brushSize - half; dc++) {
            const r = cell.row + dr;
            const c = cell.col + dc;
            if (r >= 0 && r < rows && c >= 0 && c < columns) {
                cells[r * columns + c] = color;
            }
        }
    }

    render();
    scheduleSend();
}

// --- Debounced matrix update ---
function scheduleSend() {
    clearTimeout(sendTimer);
    sendTimer = setTimeout(sendUpdate, DEBOUNCE_MS);
}

function hexToRgb(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgb(${r}, ${g}, ${b})`;
}

function sendUpdate() {
    $.ajax({
        url: '/sendtoboard',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ value: cells.map(hexToRgb) }),
        error: () => showToast('Failed to send pixels to the matrix.', 'error'),
    });
}

// --- Pi file picker modal ---
// Opens a pop-up that lets the user browse the Pi's file system
// and load a saved image directly into the canvas.
function showPiPickerModal() {
    // Track the currently open folder path (empty string = root)
    let pickerPath = '';

    // --- Dark overlay behind the modal ---
    const overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;inset:0;z-index:10000;background:rgba(15,23,42,0.55);display:flex;align-items:center;justify-content:center;padding:1rem;';

    // --- White modal box ---
    const box = document.createElement('div');
    box.style.cssText = 'background:#fff;border-radius:12px;padding:1.25rem;width:100%;max-width:420px;max-height:80vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,0.25);';
    // Stop clicks inside the box from closing the overlay
    box.addEventListener('click', e => e.stopPropagation());

    // --- Header row: title + close button ---
    const header = document.createElement('div');
    header.style.cssText = 'display:flex;align-items:center;justify-content:space-between;margin-bottom:0.75rem;';
    const title = document.createElement('h6');
    title.textContent = 'Load from Pi';
    title.style.cssText = 'font-weight:600;margin:0;font-size:1rem;';
    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.textContent = '×';
    closeBtn.className = 'btn btn-sm btn-outline-secondary';
    closeBtn.style.cssText = 'width:28px;height:28px;padding:0;line-height:1;';
    closeBtn.onclick = () => overlay.remove();
    header.append(title, closeBtn);

    // --- Breadcrumb: shows the current folder path ---
    const breadcrumb = document.createElement('div');
    breadcrumb.style.cssText = 'font-size:0.8rem;color:#64748b;margin-bottom:0.5rem;min-height:1.2em;';

    // --- Scrollable file/folder list ---
    const browser = document.createElement('div');
    browser.style.cssText = 'flex:1;overflow-y:auto;border:1px solid #e2e8f0;border-radius:8px;padding:4px;background:#f8fafc;min-height:200px;';

    // Assemble and show the modal
    box.append(header, breadcrumb, browser);
    overlay.appendChild(box);
    overlay.addEventListener('click', () => overlay.remove()); // click outside to close
    document.body.appendChild(overlay);

    // --- Helper: update the breadcrumb text ---
    function setBreadcrumb(path) {
        breadcrumb.textContent = '/ ' + (path || '');
    }

    // --- Helper: create a single clickable row (folder or file) ---
    function renderItem(icon, label, onClick) {
        const row = document.createElement('div');
        row.style.cssText = 'display:flex;align-items:center;gap:8px;padding:6px 8px;border-radius:6px;cursor:pointer;font-size:0.875rem;';
        row.addEventListener('mouseenter', () => row.style.background = '#e2e8f0');
        row.addEventListener('mouseleave', () => row.style.background = '');
        const span = document.createElement('span');
        span.textContent = `${icon}  ${label}`;
        span.style.cssText = 'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;';
        row.appendChild(span);
        row.addEventListener('click', onClick);
        return row;
    }

    // --- Load a directory from the Pi and render its contents ---
    function loadDir(path) {
        browser.innerHTML = '<div style="padding:8px;color:#94a3b8;font-size:0.85rem;">Loading…</div>';
        fetch('/pi/files', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path }),
        })
        .then(r => r.json())
        .then(data => {
            pickerPath = data.path || '';
            setBreadcrumb(pickerPath);
            browser.innerHTML = '';

            // Add a ".." back button unless we are already at the root
            if (pickerPath) {
                const up = pickerPath.includes('/')
                    ? pickerPath.slice(0, pickerPath.lastIndexOf('/'))
                    : '';
                browser.appendChild(renderItem('⬅', '..', () => loadDir(up)));
            }

            // Show "empty folder" message if there is nothing to list
            if ((!data.dirs || data.dirs.length === 0) && (!data.files || data.files.length === 0)) {
                const empty = document.createElement('div');
                empty.textContent = 'This folder is empty.';
                empty.style.cssText = 'padding:8px;color:#94a3b8;font-size:0.85rem;';
                browser.appendChild(empty);
                return;
            }

            // Render subdirectory rows (clicking opens the subfolder)
            (data.dirs || []).forEach(name => {
                const fullPath = pickerPath ? `${pickerPath}/${name}` : name;
                browser.appendChild(renderItem('📁', name, () => loadDir(fullPath)));
            });

            // Render file rows (clicking loads the image into the canvas)
            (data.files || []).forEach(name => {
                const fullPath = pickerPath ? `${pickerPath}/${name}` : name;
                browser.appendChild(renderItem('🖼️', name, () => {
                    loadImageIntoCanvas(`/pi/file/preview?path=${encodeURIComponent(fullPath)}`);
                    showToast(`"${name}" loaded into canvas.`);
                    overlay.remove();
                }));
            });
        })
        .catch(() => {
            browser.innerHTML = '<div style="padding:8px;color:#ef4444;font-size:0.85rem;">Failed to load directory.</div>';
        });
    }

    // Start at the root folder
    loadDir('');
}

// --- Load any image URL into the canvas (scales to 30x30) ---
function loadImageIntoCanvas(url) {
    const img = new Image();
    img.onload = () => {
        const offscreen    = document.createElement('canvas');
        offscreen.width    = columns;
        offscreen.height   = rows;
        const offCtx = offscreen.getContext('2d');
        offCtx.drawImage(img, 0, 0, columns, rows);

        const data = offCtx.getImageData(0, 0, columns, rows).data;
        for (let i = 0; i < rows * columns; i++) {
            const r = data[i * 4].toString(16).padStart(2, '0');
            const g = data[i * 4 + 1].toString(16).padStart(2, '0');
            const b = data[i * 4 + 2].toString(16).padStart(2, '0');
            cells[i] = `#${r}${g}${b}`;
        }

        render();
        scheduleSend();
    };
    img.src = url;
}

// --- Simple name prompt modal (standalone, no module imports needed) ---
function promptDrawingName() {
    return new Promise(resolve => {
        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;inset:0;z-index:10000;background:rgba(15,23,42,0.55);display:flex;align-items:center;justify-content:center;padding:1rem;';

        const box = document.createElement('div');
        box.style.cssText = 'background:#fff;border-radius:12px;padding:1.5rem;width:100%;max-width:360px;box-shadow:0 20px 60px rgba(0,0,0,0.25);';
        box.addEventListener('click', e => e.stopPropagation());

        const h = document.createElement('h6');
        h.textContent = 'Save drawing';
        h.style.cssText = 'font-weight:600;margin:0 0 1rem;font-size:1rem;';

        const input = document.createElement('input');
        input.type        = 'text';
        input.placeholder = 'Drawing name (e.g. my_art)';
        input.className   = 'form-control';
        input.style.borderRadius = '8px';

        const footer = document.createElement('div');
        footer.style.cssText = 'display:flex;gap:8px;justify-content:flex-end;margin-top:1rem;';

        const cancel  = document.createElement('button');
        cancel.type      = 'button';
        cancel.textContent = 'Cancel';
        cancel.className = 'btn btn-sm btn-outline-secondary';

        const confirm = document.createElement('button');
        confirm.type      = 'button';
        confirm.textContent = 'Save';
        confirm.className = 'btn btn-sm btn-primary';

        footer.append(cancel, confirm);
        box.append(h, input, footer);
        overlay.appendChild(box);
        document.body.appendChild(overlay);
        setTimeout(() => input.focus(), 30);

        const done = val => { overlay.remove(); resolve(val); };

        cancel.onclick  = () => done(null);
        confirm.onclick = () => done(input.value.trim());
        overlay.onclick = () => done(null);
        input.addEventListener('keydown', e => {
            if (e.key === 'Enter')  done(input.value.trim());
            if (e.key === 'Escape') done(null);
        });
    });
}

// --- Save drawing to server ---
async function saveToServer() {
    const name = await promptDrawingName();
    if (name === null) return; // cancelled

    const btn = document.getElementById('saveButton');
    btn.disabled    = true;
    btn.textContent = 'Saving…';

    fetch('/draw/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pixels: cells, name }),
    })
    .then(r => r.json())
    .then(data => {
        if (data.ok) {
            showToast(`Saved as "${data.filename}"!`);
            loadHistory();
        } else {
            showToast(data.error || 'Save failed.', 'error');
        }
    })
    .catch(() => showToast('Save failed.', 'error'))
    .finally(() => {
        btn.disabled    = false;
        btn.textContent = '💾 Save';
    });
}

// --- Load drawing history from server ---
function loadHistory() {
    fetch('/draw/list')
    .then(r => r.json())
    .then(data => renderHistory(data.drawings || []))
    .catch(() => {});
}

function renderHistory(drawings) {
    const grid = document.getElementById('historyGrid');
    if (!grid) return;

    if (drawings.length === 0) {
        grid.innerHTML = '<span class="text-muted small">No saved drawings yet.</span>';
        return;
    }

    grid.innerHTML = '';
    drawings.forEach(filename => {
        const wrap = document.createElement('div');
        wrap.style.cssText = 'position:relative;cursor:pointer;';
        wrap.title = filename;

        const img = document.createElement('img');
        img.src = `/draw/file/${filename}`;
        img.style.cssText = [
            'width:60px', 'height:60px',
            'image-rendering:pixelated',
            'border:2px solid #e2e8f0',
            'border-radius:6px',
            'display:block',
            'transition:border-color .15s',
        ].join(';');
        img.addEventListener('mouseenter', () => img.style.borderColor = '#6366f1');
        img.addEventListener('mouseleave', () => img.style.borderColor = '#e2e8f0');

        // Click to load into canvas
        img.addEventListener('click', () => {
            loadImageIntoCanvas(`/draw/file/${filename}`);
            showToast('Drawing loaded into canvas.');
        });

        // Delete button
        const del = document.createElement('button');
        del.textContent = '×';
        del.style.cssText = [
            'position:absolute', 'top:-6px', 'right:-6px',
            'width:18px', 'height:18px',
            'border-radius:50%',
            'background:#ef4444', 'color:#fff',
            'border:none', 'cursor:pointer',
            'font-size:11px', 'line-height:1',
            'display:none', 'align-items:center', 'justify-content:center',
            'padding:0',
        ].join(';');
        del.addEventListener('click', (e) => {
            e.stopPropagation();
            fetch(`/draw/delete/${filename}`, { method: 'DELETE' })
            .then(() => { showToast('Deleted.'); loadHistory(); })
            .catch(() => showToast('Delete failed.', 'error'));
        });

        wrap.addEventListener('mouseenter', () => del.style.display = 'flex');
        wrap.addEventListener('mouseleave', () => del.style.display = 'none');

        wrap.append(img, del);
        grid.appendChild(wrap);
    });
}

// --- Zoom ---
function setZoom(level) {
    zoomLevel = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, level));
    document.getElementById('zoomLevel').textContent = zoomLevel + 'x';
    resizeCanvas();
}

// --- Pan mode ---
function setPanMode(enabled) {
    panMode = enabled;
    canvas.style.pointerEvents = panMode ? 'none' : 'auto';
    document.getElementById('panButton').classList.toggle('active', panMode);
}

// --- Mouse events ---
canvas.addEventListener('mousedown', e => {
    if (panMode) return;
    isDrawing = true;
    paintAt(e.clientX, e.clientY);
});
window.addEventListener('mouseup', () => isDrawing = false);
canvas.addEventListener('mousemove', e => {
    if (isDrawing && !panMode) paintAt(e.clientX, e.clientY);
});

// --- Touch events ---
canvas.addEventListener('touchstart', e => {
    if (panMode) return;
    e.preventDefault();
    isDrawing = true;
    paintAt(e.touches[0].clientX, e.touches[0].clientY);
}, { passive: false });

canvas.addEventListener('touchmove', e => {
    if (panMode) return;
    e.preventDefault();
    paintAt(e.touches[0].clientX, e.touches[0].clientY);
}, { passive: false });

canvas.addEventListener('touchend', e => {
    if (panMode) return;
    e.preventDefault();
    isDrawing = false;
}, { passive: false });

// --- Toolbar buttons ---
function setModeButtons(activeId) {
    ['drawButton', 'eraseButton', 'panButton'].forEach(id => {
        document.getElementById(id).classList.toggle('active', id === activeId);
    });
}

document.getElementById('drawButton').addEventListener('click', () => {
    gridTileMode = PAINT;
    tileMode.textContent = PAINT;
    setModeButtons('drawButton');
    setPanMode(false);
});

document.getElementById('eraseButton').addEventListener('click', () => {
    gridTileMode = ERASE;
    tileMode.textContent = ERASE;
    setModeButtons('eraseButton');
    setPanMode(false);
});

document.getElementById('panButton').addEventListener('click', () => {
    setPanMode(!panMode);
    if (panMode) {
        gridTileMode = PAN;
        tileMode.textContent = PAN;
        setModeButtons('panButton');
    } else {
        gridTileMode = PAINT;
        tileMode.textContent = PAINT;
        setModeButtons('drawButton');
    }
});

document.getElementById('zoomIn').addEventListener('click',  () => setZoom(zoomLevel + 1));
document.getElementById('zoomOut').addEventListener('click', () => setZoom(zoomLevel - 1));

document.getElementById('clearButton').addEventListener('click', () => {
    cells.fill('#000000');
    render();
    sendUpdate();
});

document.getElementById('downloadButton').addEventListener('click', () => {
    const link      = document.createElement('a');
    link.download   = 'matrix-drawing.png';
    link.href       = canvas.toDataURL('image/png');
    link.click();
});

document.getElementById('saveButton').addEventListener('click', saveToServer);

document.getElementById('refreshHistory').addEventListener('click', loadHistory);

document.getElementById('loadFromPiButton').addEventListener('click', showPiPickerModal);

// Load image from local file
document.getElementById('loadImageInput').addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    loadImageIntoCanvas(url);
    showToast('Image loaded into canvas.');
    e.target.value = '';
});

document.querySelectorAll('.brushBtn').forEach(btn => {
    btn.addEventListener('click', () => {
        brushSize = parseInt(btn.dataset.size);
        document.querySelectorAll('.brushBtn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

window.addEventListener('resize', () => resizeCanvas());
resizeCanvas();
loadHistory();
