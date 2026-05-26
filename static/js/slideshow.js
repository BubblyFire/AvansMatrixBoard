const IMAGE_EXTS = new Set(['.png', '.jpg', '.jpeg', '.gif', '.bmp']);

let currentTab         = 'folder';
let selectedFolderPath = null;   // virtual path, folder mode
let playlist           = [];     // [{path, name}], playlist mode

// ── Tabs ──────────────────────────────────────────────────────────────────────

function switchTab(tab) {
    currentTab = tab;
    document.getElementById('panelFolder').style.display   = tab === 'folder'   ? '' : 'none';
    document.getElementById('panelPlaylist').style.display = tab === 'playlist' ? '' : 'none';
    document.getElementById('tabFolder').className   = 'btn btn-sm ' + (tab === 'folder'   ? 'btn-secondary active' : 'btn-outline-secondary');
    document.getElementById('tabPlaylist').className = 'btn btn-sm ' + (tab === 'playlist' ? 'btn-secondary active' : 'btn-outline-secondary');
    // Reload browser at current path so + buttons appear/disappear correctly
    loadBrowser(browserPath);
    refreshStartButton();
}

// ── File browser ──────────────────────────────────────────────────────────────

let browserPath = '';  // tracks current path for breadcrumb

function loadBrowser(path) {
    browserPath = path;
    renderBreadcrumb(path);

    const container = document.getElementById('fileBrowser');
    container.innerHTML = '<div class="ip-empty">Loading…</div>';

    fetch('/pi/files', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path }),
    })
    .then(r => r.json())
    .then(data => renderBrowser(data, path, container))
    .catch(() => { container.innerHTML = '<div class="ip-empty">Failed to load.</div>'; });
}

function renderBreadcrumb(path) {
    const el = document.getElementById('breadcrumb');
    const parts = path ? path.split('/') : [];

    let html = `<span style="cursor:pointer;color:var(--accent);" onclick="loadBrowser('')">Root</span>`;
    let built = '';
    parts.forEach(part => {
        built += (built ? '/' : '') + part;
        const p = built;
        html += ` / <span style="cursor:pointer;color:var(--accent);" onclick="loadBrowser('${p}')">${part}</span>`;
    });
    el.innerHTML = html;
}

function isImage(name) {
    return IMAGE_EXTS.has(name.slice(name.lastIndexOf('.')).toLowerCase());
}

function renderBrowser(data, currentPath, container) {
    container.innerHTML = '';

    const dirs  = data.dirs  || [];
    const files = (data.files || []).filter(isImage);

    // "Use this folder" button in folder mode (any level except the virtual root)
    if (currentTab === 'folder' && currentPath) {
        const useBtn = document.createElement('button');
        useBtn.className = 'btn btn-sm btn-outline-primary w-100 mb-1';
        useBtn.textContent = '✔ Use this folder';
        useBtn.addEventListener('click', () => {
            const name = currentPath.split('/').pop();
            selectFolder(currentPath, name);
        });
        container.appendChild(useBtn);
    }

    if (dirs.length === 0 && files.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'ip-empty';
        empty.textContent = 'Empty folder.';
        container.appendChild(empty);
        return;
    }

    dirs.forEach(name => {
        const fullPath = currentPath ? `${currentPath}/${name}` : name;
        container.appendChild(makeRow('📁', name, false, () => loadBrowser(fullPath)));
    });

    files.forEach(name => {
        const fullPath = currentPath ? `${currentPath}/${name}` : name;
        container.appendChild(makeRow('🖼', name, true, () => {
            if (currentTab === 'playlist') addToPlaylist(fullPath, name);
        }));
    });
}

function makeRow(icon, label, isFile, onClick) {
    const row = document.createElement('div');
    row.style.cssText = 'display:flex;align-items:center;gap:8px;padding:10px 12px;min-height:44px;border-radius:6px;cursor:pointer;font-size:0.875rem;';
    row.addEventListener('mouseenter', () => row.style.background = '#e2e8f0');
    row.addEventListener('mouseleave', () => row.style.background = '');

    const icon_el = document.createElement('span');
    icon_el.textContent = icon;
    icon_el.style.flexShrink = '0';

    const label_el = document.createElement('span');
    label_el.textContent = label;
    label_el.style.cssText = 'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;';

    row.append(icon_el, label_el);

    if (isFile && currentTab === 'playlist') {
        const addBtn = document.createElement('span');
        addBtn.textContent = '+';
        addBtn.style.cssText = 'color:var(--accent);font-weight:bold;font-size:1rem;flex-shrink:0;';
        addBtn.title = 'Add to playlist';
        row.appendChild(addBtn);
    }

    row.addEventListener('click', onClick);
    return row;
}

// ── Folder mode ───────────────────────────────────────────────────────────────

function selectFolder(path, name) {
    selectedFolderPath = path;

    const display = document.getElementById('selectedFolderDisplay');
    display.className = 'rounded p-2';
    display.style.cssText = 'background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.3);';
    display.innerHTML = `📁 <strong>${name}</strong><br><span class="small text-muted">${path}</span>`;

    refreshStartButton();
}

// ── Playlist mode ─────────────────────────────────────────────────────────────

function addToPlaylist(path, name) {
    if (playlist.some(f => f.path === path)) return; // no duplicates
    playlist.push({ path, name });
    renderPlaylist();
    refreshStartButton();
}

function removeFromPlaylist(index) {
    playlist.splice(index, 1);
    renderPlaylist();
    refreshStartButton();
}

function clearPlaylist() {
    playlist = [];
    renderPlaylist();
    refreshStartButton();
}

function renderPlaylist() {
    const container = document.getElementById('playlistItems');
    document.getElementById('playlistCount').textContent = playlist.length;

    if (playlist.length === 0) {
        container.innerHTML = '<div class="ip-empty">Click image files in the browser to add them.</div>';
        return;
    }

    container.innerHTML = '';
    playlist.forEach(({ path, name }, i) => {
        const item = document.createElement('div');
        item.style.cssText = 'display:flex;align-items:center;gap:6px;padding:10px 12px;min-height:44px;font-size:0.82rem;border-radius:4px;';
        item.addEventListener('mouseenter', () => item.style.background = '#f1f5f9');
        item.addEventListener('mouseleave', () => item.style.background = '');

        const nameEl = document.createElement('span');
        nameEl.textContent = `🖼 ${name}`;
        nameEl.style.cssText = 'flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;';
        nameEl.title = path;

        const del = document.createElement('button');
        del.textContent = '×';
        del.style.cssText = 'border:none;background:none;color:#ef4444;cursor:pointer;font-size:1.25rem;padding:8px 12px;min-width:44px;min-height:44px;flex-shrink:0;';
        del.addEventListener('click', () => removeFromPlaylist(i));

        item.append(nameEl, del);
        container.appendChild(item);
    });
}

// ── Controls ──────────────────────────────────────────────────────────────────

function refreshStartButton() {
    const canStart = currentTab === 'folder'
        ? !!selectedFolderPath
        : playlist.length > 0;
    document.getElementById('startBtn').disabled = !canStart;
}

function startSlideshow() {
    const interval = parseInt(document.getElementById('intervalSlider').value, 10);
    let body;

    if (currentTab === 'folder') {
        body = { mode: 'folder', path: selectedFolderPath, interval };
    } else {
        body = { mode: 'playlist', files: playlist.map(f => f.path), interval };
    }

    fetch('/slideshow/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) { showToast(data.error, 'error'); return; }
        showToast('Slideshow started!');
        setRunningUI(true);
    })
    .catch(() => showToast('Failed to start slideshow.', 'error'));
}

function stopSlideshow() {
    fetch('/slideshow/stop', { method: 'POST' })
    .then(() => { showToast('Slideshow stopped.'); setRunningUI(false); })
    .catch(() => showToast('Failed to stop.', 'error'));
}

function setRunningUI(running) {
    document.getElementById('startBtn').disabled         = running;
    document.getElementById('stopBtn').disabled          = !running;
    document.getElementById('intervalSlider').disabled   = running;
    document.getElementById('tabFolder').disabled        = running;
    document.getElementById('tabPlaylist').disabled      = running;
}

// ── Status polling ────────────────────────────────────────────────────────────

function pollStatus() {
    fetch('/slideshow/status')
    .then(r => r.json())
    .then(data => {
        const card   = document.getElementById('statusCard');
        const dot    = document.getElementById('statusDot');
        const folder = document.getElementById('statusFolder');
        const file   = document.getElementById('statusFile');

        card.style.display = '';
        setRunningUI(data.running);

        if (data.running) {
            dot.className   = 'badge badge-success';
            dot.textContent = '● Playing';
            folder.textContent = data.folder ? `📁 ${data.folder}` : '';
            file.textContent   = data.current ? `🖼 ${data.current}` : '';
        } else {
            dot.className   = 'badge badge-secondary';
            dot.textContent = '● Stopped';
            folder.textContent = '';
            file.textContent   = '';
        }
    })
    .catch(() => {});
}

// ── Init ──────────────────────────────────────────────────────────────────────

function initSlideshow() {
    loadBrowser('');

    document.getElementById('intervalSlider').addEventListener('input', function () {
        document.getElementById('intervalDisplay').textContent = this.value;
    });

    document.getElementById('startBtn').addEventListener('click', startSlideshow);
    document.getElementById('stopBtn').addEventListener('click', stopSlideshow);

    pollStatus();
    setInterval(pollStatus, 2000);
}
