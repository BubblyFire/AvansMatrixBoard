export const URLS = {
  list:    "/pi/files",
  preview: "/pi/file/preview",
  display: "/pi/file/display",
  upload:  "/pi/file/upload",
  mkdir:   "/pi/dir/mkdir",
  rename:  "/pi/path/rename",
  move:    "/pi/path/move",
  del:     "/pi/path/delete",
};

export async function postJSON(url, bodyObj) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(bodyObj || {}),
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }
  return data;
}
