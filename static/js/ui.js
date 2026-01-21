export const UI = {
  browser:     () => document.getElementById("piBrowser"),
  breadcrumb:  () => document.getElementById("piBreadcrumb"),
  previewWrap: () => document.getElementById("piPreview"),
  previewImg:  () => document.getElementById("piPreviewImg"),
  selectedEl:  () => document.getElementById("piSelectedFile"),

  btnMkdir:    () => document.getElementById("createFolderBtn"),
  btnUse:      () => document.getElementById("usePiFileBtn"),
  btnUpload:   () => document.getElementById("uploadLocalBtn"),
  fileInput:   () => document.getElementById("localFileInput"),
};

export function makeTitle(text) {
  const t = document.createElement("div");
  t.className = "text-muted small mt-2 mb-1";
  t.textContent = text;
  return t;
}

export function makeMuted(text) {
  const d = document.createElement("div");
  d.className = "text-muted small";
  d.textContent = text;
  return d;
}

export function makeRow(item) {
  const row = document.createElement("div");
  row.className = "d-flex align-items-center justify-content-between p-1 rounded mb-1";

  const left = document.createElement("div");
  left.className = "d-flex align-items-center gap-2 flex-grow-1";
  left.style.cursor = "pointer";
  left.onclick = item.onOpen;

  const icon = item.kind === "dir" ? "📁" : "🖼️";
  const nameSpan = document.createElement("span");
  nameSpan.className = item.kind === "file" ? "small text-truncate" : "small";
  nameSpan.textContent = `${icon} ${item.name}`;

  left.appendChild(nameSpan);

  const dots = document.createElement("button");
  dots.type = "button";
  dots.className = "btn btn-sm btn-light";
  dots.textContent = "⋯";
  dots.onclick = (e) => {
    e.stopPropagation();
    // select it so "Use" button uses the same selection
    setSelected({ kind: item.kind, name: item.name, path: item.path });
    openActionMenu(dots, { kind: item.kind, name: item.name, path: item.path });
  };

  row.appendChild(left);
  row.appendChild(dots);
  return row;
}