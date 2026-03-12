import { renameItem, moveItem, deleteItem } from "./actions.js";

export function bindGlobalMenuClose() {
  document.addEventListener("click", closeActionMenu);
  window.addEventListener("scroll", closeActionMenu, true);
  window.addEventListener("resize", closeActionMenu);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeActionMenu();
  });
}

export function closeActionMenu() {
  document.querySelectorAll(".pi-menu").forEach((m) => m.remove());
}

function menuItem(label, fn, danger = false) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "btn btn-sm w-100 text-start";
  btn.style.cssText = [
    'border:none', 'background:transparent',
    'padding:8px 10px', 'border-radius:6px',
    'cursor:pointer', 'font-size:0.875rem',
    danger ? 'color:#ef4444' : '',
  ].join(';');

  btn.textContent = label;

  btn.addEventListener('mouseenter', () => {
    btn.style.background = danger ? '#fef2f2' : '#f1f5f9';
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.background = 'transparent';
  });

  btn.onclick = async (e) => {
    e.stopPropagation();
    closeActionMenu();
    await fn();
  };

  return btn;
}

/**
 * @param {HTMLElement} anchorBtn
 * @param {{ kind: string, name: string, path: string }} item
 * @param {{ onSuccess: function, currentPath: string }} context
 */
export function openActionMenu(anchorBtn, item, { onSuccess, currentPath } = {}) {
  closeActionMenu();

  const menu = document.createElement("div");
  menu.className = "pi-menu";
  menu.style.cssText = [
    'position:absolute', 'z-index:9999',
    'background:#fff',
    'border:1px solid #e2e8f0',
    'border-radius:10px',
    'padding:4px',
    'box-shadow:0 8px 24px rgba(0,0,0,0.12)',
    'min-width:150px',
  ].join(';');

  const rect = anchorBtn.getBoundingClientRect();
  menu.style.left = `${rect.left + window.scrollX - 110}px`;
  menu.style.top  = `${rect.bottom + window.scrollY + 6}px`;

  menu.appendChild(menuItem("✏️ Rename", () => renameItem(item, onSuccess)));
  menu.appendChild(menuItem("📁 Move",   () => moveItem(item, currentPath, onSuccess)));
  menu.appendChild(menuItem("🗑️ Delete", () => deleteItem(item, onSuccess), true));

  menu.addEventListener("click", (e) => e.stopPropagation());
  document.body.appendChild(menu);
}
