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

export function menuItem(label, fn, danger = false) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "btn btn-sm w-100 text-start";
  btn.style.border = "none";
  btn.style.background = "transparent";
  btn.style.padding = "6px 8px";
  btn.style.borderRadius = "6px";
  btn.style.cursor = "pointer";
  btn.textContent = label;
  if (danger) btn.style.color = "#dc3545";

  btn.onclick = async (e) => {
    e.stopPropagation();
    closeActionMenu();
    await fn();
  };

  return btn;
}

export function openActionMenu(anchorBtn, item) {
  closeActionMenu();

  const menu = document.createElement("div");
  menu.className = "pi-menu";
  menu.style.position = "absolute";
  menu.style.zIndex = "9999";
  menu.style.background = "white";
  menu.style.border = "1px solid #ddd";
  menu.style.borderRadius = "8px";
  menu.style.padding = "6px";
  menu.style.boxShadow = "0 6px 20px rgba(0,0,0,0.12)";
  menu.style.minWidth = "140px";

  const rect = anchorBtn.getBoundingClientRect();
  menu.style.left = `${rect.left + window.scrollX - 120}px`;
  menu.style.top  = `${rect.bottom + window.scrollY + 6}px`;

  menu.appendChild(menuItem("Rename", () => renameItem(item)));
  menu.appendChild(menuItem("Move",   () => moveItem(item)));
  menu.appendChild(menuItem("Delete", () => deleteItem(item), true));

  // Don’t close immediately when clicking inside
  menu.addEventListener("click", (e) => e.stopPropagation());

  document.body.appendChild(menu);
}
