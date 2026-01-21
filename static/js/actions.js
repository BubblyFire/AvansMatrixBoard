import { cleanPath } from "./functions.js";
import { postJSON } from "./api.js" 

export async function renameItem(item) {
  const newName = prompt(`Nieuwe naam voor:\n${item.name}`, item.name);
  if (!newName) return false;

  await postJSON(URLS.rename, { path: item.path, new_name: newName });
  return true;
}

export async function moveItem(item) {
  const dst = prompt(`Verplaats "${item.name}" naar welke map?`, currentPath || "");
  if (dst === null) return false;

  await postJSON(URLS.move, { src: item.path, dst_dir: cleanPath(dst) });
  return true;
}

export async function deleteItem(item) {
  const ok = confirm(`Verwijderen?\n\n${item.kind}: /${item.path}`);
  if (!ok) return false;

  await postJSON(URLS.del, { path: item.path });
  return true;
}