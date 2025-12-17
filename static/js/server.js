const PI_LIST_URL    = "/pi/files";
const PI_PREVIEW_URL = "/pi/file/preview";
const PI_DISPLAY_URL = "/pi/file/display";
const PI_UPLOAD_URL  = "/pi/file/upload";

const PI_MKDIR_URL   = "/pi/dir/mkdir";

let piPath     = "";
let piSelected = null;

let localFileInput = null;

window.addEventListener("load", init);

function init() {
  // start at root
  loadPiDir("");

  const createFolderBtn = document.getElementById("createFolderBtn");
  const usePiFileBtn    = document.getElementById("usePiFileBtn");
  const uploadLocalBtn  = document.getElementById("uploadLocalBtn");
  localFileInput        = document.getElementById("localFileInput");


  if (createFolderBtn) {
    createFolderBtn.addEventListener("click", onCreateFolderClick);
  }

  if (usePiFileBtn) {
    usePiFileBtn.addEventListener("click", onUsePiFileClick);
  }

  if (uploadLocalBtn) {
    uploadLocalBtn.addEventListener("click", uploadFile);
  }
}

// ------------------- Load directory -------------------------------
async function loadPiDir(path) {
  try {
    const response = await fetch(PI_LIST_URL, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ path })
    });

    const data = await response.json();
    if (!response.ok) {
      console.error("pi/files error", data);
      alert("Kon map niet laden.");
      return;
    }

    piPath = data.path || "";
    renderPiBrowser(data);
  } catch (err) {
    console.error("loadPiDir exception:", err);
    alert("Er ging iets mis bij het laden van de map.");
  }
}

// ------------------- Render directory -----------------------------
function renderPiBrowser(data) {
  const piBrowser        = document.getElementById("piBrowser");
  const piBreadcrumb     = document.getElementById("piBreadcrumb");
  const piPreview        = document.getElementById("piPreview");
  const piPreviewImg     = document.getElementById("piPreviewImg");
  const piSelectedFileEl = document.getElementById("piSelectedFile");

  if (!piBrowser) return;

  piBrowser.innerHTML = "";

  // Breadcrumb
  piBreadcrumb.textContent = "/" + (piPath || "");

  // "Go up" entry
  if (piPath !== "") {
    const back = document.createElement("div");
    back.textContent = "⬅ .. (terug)";
    back.className = "text-primary mb-2";
    back.style.cursor = "pointer";
    back.onclick = () => {
      const parent = piPath.split("/").slice(0, -1).join("/");
      loadPiDir(parent);
    };
    piBrowser.appendChild(back);
  }

  const dirs  = data.dirs  || [];
  const files = data.files || [];

  // ---- Directories ------------------------------------------------
  dirs.forEach((name) => {
    const fullPath = (piPath ? piPath + "/" : "") + name;

    const row = document.createElement("div");
    row.className =
      "d-flex align-items-center justify-content-between p-1 rounded mb-1";
    row.style.cursor = "pointer";

    const nameSpan = document.createElement("span");
    nameSpan.textContent = "📁 " + name;
    nameSpan.className = "small";
    nameSpan.onclick = () => loadPiDir(fullPath);

    row.appendChild(nameSpan);
    piBrowser.appendChild(row);
  });

  // ---- Files ------------------------------------------------------
  files.forEach((name) => {
    const fullPath = (piPath ? piPath + "/" : "") + name;

    const row = document.createElement("div");
    row.className ="d-flex align-items-center justify-content-between p-1 rounded mb-1";
    row.style.cursor = "pointer";

    const nameSpan = document.createElement("span");
    nameSpan.textContent = name;
    nameSpan.className = "small text-truncate";
    nameSpan.onclick = () => {
      piSelected = fullPath;
      if (piSelectedFileEl) {
        piSelectedFileEl.textContent = "/" + fullPath;
      }
      if (piPreviewImg && piPreview) {
        piPreviewImg.src = PI_PREVIEW_URL + `?path=${encodeURIComponent(fullPath)}`;
        piPreview.style.display = "block";
      }
    };

    row.appendChild(nameSpan);
    piBrowser.appendChild(row);
  });

  if (dirs.length === 0 && files.length === 0) {
    const empty = document.createElement("div");
    empty.textContent = "Deze map is leeg.";
    empty.className = "text-muted small";
    piBrowser.appendChild(empty);
  }
}


// --------------- Create folder ------------------------------------
async function onCreateFolderClick() {
  const name = prompt("Naam van de nieuwe map:");
  if (!name) return;

  try {
    const response = await fetch(PI_MKDIR_URL, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ path: piPath, name })
    });
    const data = await response.json();

    if (!response.ok) {
      console.error("mkdir error:", data);
      alert("Kon map niet maken: " + (data.error || response.status));
      return;
    }

    loadPiDir(piPath);
  } catch (err) {
    console.error("mkdir exception:", err);
    alert("Er ging iets mis bij het maken van de map.");
  }
}

// --------------- Use selected file -------------------------------
async function onUsePiFileClick() {
  if (!piSelected) {
    alert("Geen bestand geselecteerd.");
    return;
  }

  try {
    const response = await fetch(PI_DISPLAY_URL, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ path: piSelected })
    });
    const data = await response.json();

    if (!response.ok) {
      console.error("use error:", data);
      alert("Kon bestand niet gebruiken: " + (data.error || response.status));
      return;
    }

    alert("Bestand is naar de matrix gestuurd!");
  } catch (err) {
    console.error("use exception:", err);
    alert("Er ging iets mis bij het gebruiken van het bestand.");
  }
}

// --------------- Rename / Move --------------------
async function renameOrMoveItem(currentRelPath, typeLabel) {
  const suggestion = currentRelPath;
  const newRelPath = prompt(
    "Nieuwe naam/locatie voor " + typeLabel + ":\n" +
    "(voorbeeld: images/nieuwenaam.png of andere_map/bestand.png)",
    suggestion
  );

  if (!newRelPath || newRelPath === currentRelPath) return;

  try {
    const response = await fetch(PI_MOVE_URL, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        from_path: currentRelPath,
        to_path: newRelPath
      })
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("move error:", data);
      alert("Kon " + typeLabel + " niet verplaatsen/hernoemen: " + (data.error || response.status));
      return;
    }

    loadPiDir(piPath);
  } catch (err) {
    console.error("move exception:", err);
    alert("Er ging iets mis bij het verplaatsen/hernoemen.");
  }
}

async function uploadFile() {
  if (!localFileInput) {
    alert("Local file input niet gevonden.");
    return;
  }

  const file = localFileInput.files?.[0];
  if (!file) {
    alert("Geen lokaal bestand geselecteerd.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("path", piPath || "");

  try {
    const response = await fetch("/pi/file/upload", {
      method: "POST",
      body: formData
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok || !data.ok) {
      console.error("upload error:", data);
      alert("Kon lokaal bestand niet uploaden: " + (data.error || response.status));
      return;
    }

    alert("Lokaal bestand is geüpload naar de Pi.");
    loadPiDir(piPath || "");
  } catch (err) {
    console.error("upload exception:", err);
    alert("Er ging iets mis bij het uploaden van het lokale bestand.");
  }
}
