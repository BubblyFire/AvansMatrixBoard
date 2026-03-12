import { openActionMenu } from "./menu.js";

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
  t.className = "section-label mt-3 mb-1";
  t.textContent = text;
  return t;
}

export function makeMuted(text) {
  const d = document.createElement("div");
  d.className = "text-muted small";
  d.textContent = text;
  return d;
}

/**
 * @param {{ kind, name, path, onOpen }} item
 * @param {{ onSelect: function, currentPath: string, onSuccess: function }} callbacks
 */
export function makeRow(item, { onSelect, currentPath, onSuccess } = {}) {
  const row = document.createElement("div");
  row.className = "d-flex align-items-center justify-content-between rounded mb-1";
  row.style.cssText = 'padding:4px 6px;transition:background .1s;';

  row.addEventListener('mouseenter', () => row.style.background = '#f8fafc');
  row.addEventListener('mouseleave', () => row.style.background = '');

  const left = document.createElement("div");
  left.className = "d-flex align-items-center flex-grow-1 text-truncate";
  left.style.cursor = "pointer";
  left.onclick = item.onOpen;

  const icon = item.kind === "dir" ? "📁" : "🖼️";
  const nameSpan = document.createElement("span");
  nameSpan.className = "small text-truncate";
  nameSpan.textContent = `${icon}  ${item.name}`;
  left.appendChild(nameSpan);

  const dots = document.createElement("button");
  dots.type = "button";
  dots.className = "btn btn-sm btn-light flex-shrink-0 ml-1";
  dots.style.cssText = 'padding:2px 8px;font-size:1rem;line-height:1;border-radius:6px;';
  dots.textContent = "⋯";
  dots.title = "More options";
  dots.onclick = (e) => {
    e.stopPropagation();
    const ctx = { kind: item.kind, name: item.name, path: item.path };
    onSelect?.(ctx);
    openActionMenu(dots, ctx, { onSuccess, currentPath });
  };

  row.appendChild(left);
  row.appendChild(dots);
  return row;
}
