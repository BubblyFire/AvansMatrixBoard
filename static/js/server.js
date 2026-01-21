import { URLS, postJSON } from "./api.js";
import { bindGlobalMenuClose } from "./menu.js";
import { joinPath, parentPath } from "./functions.js";
import { makeTitle, makeMuted, makeRow } from "./ui.js";
import { UI } from "./ui.js"

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

  // Preview only for files
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
  if (el) el.textContent = "/" + (path || "");
}

async function loadDir(path) {
  try {
    const data = await postJSON(URLS.list, { path });
    state.path = data.path || "";
    setBreadcrumb(state.path);
    setSelected(null);
    renderBrowser(data.dirs || [], data.files || []);
  } catch (e) {
    console.error(e);
    alert("Kon map niet laden.");
  }
}
function renderBrowser(dirs, files) {
  const browser = UI.browser();
  if (!browser) return;

  browser.innerHTML = "";

  // Up
  if (state.path) {
    const up = document.createElement("div");
    up.textContent = "⬅ .. (terug)";
    up.className = "text-primary mb-2";
    up.style.cursor = "pointer";
    up.onclick = () => loadDir(parentPath(state.path));
    browser.appendChild(up);
  }

  // Empty
  if (dirs.length === 0 && files.length === 0) {
    const empty = document.createElement("div");
    empty.textContent = "Deze map is leeg.";
    empty.className = "text-muted small mt-2";
    browser.appendChild(empty);
    return;
  }

  // Folders
  browser.appendChild(makeTitle("📁 Mappen"));
  if (dirs.length === 0) {
    browser.appendChild(makeMuted("Geen mappen."));
  } else {
    dirs.forEach((name) => browser.appendChild(makeRow({
      kind: "dir",
      name,
      path: joinPath(state.path, name),
      onOpen: () => loadDir(joinPath(state.path, name)),
    })));
  }

  // Files
  browser.appendChild(makeTitle("🖼️ Bestanden"));
  if (files.length === 0) {
    browser.appendChild(makeMuted("Geen bestanden."));
  } else {
    files.forEach((name) => browser.appendChild(makeRow({
      kind: "file",
      name,
      path: joinPath(state.path, name),
      onOpen: () => setSelected({ kind: "file", name, path: joinPath(state.path, name) }),
    })));
  }
}

async function onCreateFolderClick() {
  const name = prompt("Naam van de nieuwe map:");
  if (!name) return;
  await postJSON(URLS.mkdir, { path: state.path, name });
  loadDir(state.path);
}

async function onUseSelectedFileClick() {
  if (!state.selected || state.selected.kind !== "file") {
    alert("Geen bestand geselecteerd.");
    return;
  }
  await postJSON(URLS.display, { path: state.selected.path });
  alert("Bestand is naar de matrix gestuurd!");
}

async function onUploadClick() {
  const file = UI.fileInput()?.files?.[0];
  if (!file) return alert("Geen lokaal bestand geselecteerd.");

  const formData = new FormData();
  formData.append("file", file);
  formData.append("path", state.path || "");

  const res = await fetch(URLS.upload, { method: "POST", body: formData });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || !data.ok) throw new Error(data.error || `HTTP ${res.status}`);

  alert("Upload klaar!");
  loadDir(state.path);
}