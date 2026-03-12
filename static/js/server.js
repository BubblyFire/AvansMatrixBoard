import { URLS, postJSON } from "./api.js";
import { bindGlobalMenuClose } from "./menu.js";
import { joinPath } from "./functions.js";
import { makeTitle, makeMuted, makeRow, UI } from "./ui.js";
import { showInputModal } from "./modal.js";

let state = {
  path: "",
  selected: null,
};

window.addEventListener("load", init);

function init() {
  bindUI();
  bindGlobalMenuClose();
  loadDir("");
}

function bindUI() {
  UI.btnMkdir()?.addEventListener("click", onCreateFolderClick);
  UI.btnUse()?.addEventListener("click", onUseSelectedFileClick);
  UI.btnUpload()?.addEventListener("click", onUploadClick);
}

function setSelected(itemOrNull) {
  state.selected = itemOrNull;

  const selectedEl = UI.selectedEl();
  if (selectedEl) selectedEl.textContent = itemOrNull ? ("/" + itemOrNull.path) : "–";

  const wrap = UI.previewWrap();
  const img  = UI.previewImg();
  if (wrap && img) {
    if (itemOrNull && itemOrNull.kind === "file") {
      img.src = `${URLS.preview}?path=${encodeURIComponent(itemOrNull.path)}`;
      wrap.style.display = "block";
    } else {
      img.src = "";
      wrap.style.display = "none";
    }
  }
}

function setBreadcrumb(path) {
  const el = UI.breadcrumb();
  if (!el) return;

  const parts = path ? path.split('/') : [];
  const makeLink = (label, target) => {
    const a = document.createElement('span');
    a.textContent = label;
    a.style.cssText = 'cursor:pointer;color:var(--accent);';
    a.addEventListener('click', () => loadDir(target));
    return a;
  };

  el.innerHTML = '';
  el.appendChild(makeLink('Root', ''));

  let built = '';
  parts.forEach(part => {
    const sep = document.createTextNode(' / ');
    built += (built ? '/' : '') + part;
    const target = built;
    el.appendChild(sep);
    el.appendChild(makeLink(part, target));
  });
}

async function loadDir(path) {
  try {
    const data = await postJSON(URLS.list, { path });
    state.path = data.path || "";
    setBreadcrumb(state.path);
    setSelected(null);
    renderBrowser(data.dirs || [], data.files || []);
  } catch (e) {
    showToast('Failed to load directory.', 'error');
  }
}

function renderBrowser(dirs, files) {
  const browser = UI.browser();
  if (!browser) return;

  browser.innerHTML = "";

  if (dirs.length === 0 && files.length === 0) {
    browser.appendChild(makeMuted("This folder is empty."));
    return;
  }

  const rowCallbacks = {
    onSelect:    setSelected,
    currentPath: state.path,
    onSuccess:   () => loadDir(state.path),
  };

  browser.appendChild(makeTitle("Folders"));
  if (dirs.length === 0) {
    browser.appendChild(makeMuted("No folders."));
  } else {
    dirs.forEach((name) => browser.appendChild(makeRow({
      kind: "dir",
      name,
      path: joinPath(state.path, name),
      onOpen: () => loadDir(joinPath(state.path, name)),
    }, rowCallbacks)));
  }

  browser.appendChild(makeTitle("Files"));
  if (files.length === 0) {
    browser.appendChild(makeMuted("No files."));
  } else {
    files.forEach((name) => browser.appendChild(makeRow({
      kind: "file",
      name,
      path: joinPath(state.path, name),
      onOpen: () => setSelected({ kind: "file", name, path: joinPath(state.path, name) }),
    }, rowCallbacks)));
  }
}

async function onCreateFolderClick() {
  const name = await showInputModal({
    title: 'New Folder',
    placeholder: 'Folder name',
    confirmLabel: 'Create',
  });
  if (!name) return;

  try {
    await postJSON(URLS.mkdir, { path: state.path, name });
    showToast('Folder created.');
    loadDir(state.path);
  } catch (e) {
    showToast('Failed to create folder: ' + e.message, 'error');
  }
}

async function onUseSelectedFileClick() {
  if (!state.selected || state.selected.kind !== "file") {
    showToast('No file selected.', 'error');
    return;
  }
  try {
    await postJSON(URLS.display, { path: state.selected.path });
    showToast('Showing on matrix.');
  } catch (e) {
    showToast('Failed to send file to matrix.', 'error');
  }
}

async function onUploadClick() {
  const file = UI.fileInput()?.files?.[0];
  if (!file) {
    showToast('No local file selected.', 'error');
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("path", state.path || "");

  try {
    const res  = await fetch(URLS.upload, { method: "POST", body: formData });
    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.ok) throw new Error(data.error || `HTTP ${res.status}`);
    showToast('Upload complete.');
    loadDir(state.path);
  } catch (e) {
    showToast('Upload failed: ' + e.message, 'error');
  }
}
