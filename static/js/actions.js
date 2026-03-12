import { postJSON, URLS } from "./api.js";
import { showInputModal, showConfirmModal } from "./modal.js";

export async function renameItem(item, onSuccess) {
  const newName = await showInputModal({
    title: `Rename "${item.name}"`,
    defaultValue: item.name,
    placeholder: 'New name',
    confirmLabel: 'Rename',
  });
  if (!newName || newName === item.name) return false;

  try {
    await postJSON(URLS.rename, { path: item.path, new_name: newName });
    showToast(`Renamed to "${newName}".`);
    onSuccess?.();
    return true;
  } catch (e) {
    showToast('Rename failed: ' + e.message, 'error');
    return false;
  }
}

export async function moveItem(item, currentPath, onSuccess) {
  const dst = await showInputModal({
    title: `Move "${item.name}"`,
    placeholder: 'Destination folder (leave empty for root)',
    defaultValue: currentPath || '',
    confirmLabel: 'Move',
  });
  if (dst === null) return false;

  try {
    await postJSON(URLS.move, { src: item.path, dst_dir: dst });
    showToast(`Moved to "/${dst || ''}" .`);
    onSuccess?.();
    return true;
  } catch (e) {
    showToast('Move failed: ' + e.message, 'error');
    return false;
  }
}

export async function deleteItem(item, onSuccess) {
  const confirmed = await showConfirmModal({
    title: 'Delete?',
    body: `/${item.path}`,
    confirmLabel: 'Delete',
    danger: true,
  });
  if (!confirmed) return false;

  try {
    await postJSON(URLS.del, { path: item.path });
    showToast(`Deleted "${item.name}".`);
    onSuccess?.();
    return true;
  } catch (e) {
    showToast('Delete failed: ' + e.message, 'error');
    return false;
  }
}
