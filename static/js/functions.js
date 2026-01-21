// remove leading/trailing slashes
export function cleanPath(p) {
  return (p || "").replace(/^\/+|\/+$/g, "");
}

// safely join two path parts
export function joinPath(a, b) {
  a = cleanPath(a);
  b = cleanPath(b);

  if (!a) {
    return b;
  }

  if (!b) {
    return a;
  } 

  return `${a}/${b}`;
}   

// return parent directory
export function parentPath(p) {
  p = cleanPath(p);
  if (!p) {
    return "";
  }
  const i = p.lastIndexOf("/");
  return i === -1 ? "" : p.slice(0, i);
}
