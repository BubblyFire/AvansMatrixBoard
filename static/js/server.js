const PI_LIST_URL    = "/pi/dirs";
const PI_PREVIEW_URL = "/pi-files/preview";
const PI_MKDIR_URL   = "/pi-files/mkdir";
const PI_USE_URL     = "/pi-files/use";

// Keeps track of the current path and selected file
let piPath = "";
let piSelected = null;

/*
  Start the browser by loading the root folder
*/
function init() {
  loadPiDir("");

  // Hook up buttons
  const createFolderBtn = document.getElementById("createFolderBtn");
  const usePiFileBtn    = document.getElementById("usePiFileBtn");

  if (createFolderBtn) {
    createFolderBtn.addEventListener("click", onCreateFolderClick);
  }

  if (usePiFileBtn) {
    usePiFileBtn.addEventListener("click", onUsePiFileClick);
  }
}

/*
  Load folder contents from the server.
  This function gets a list of folders + files using fetch()
  and then calls renderPiBrowser() to show it on the page.
*/
async function loadPiDir(path) {
    console.log("Loading:", path);

    const response = await fetch(PI_LIST_URL, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ path: path })
    });

    const data = await response.json();
    piPath = data.path || "";
    renderPiBrowser(data);
}

/*
  Draws the folder browser.
  This updates the breadcrumb, folder list, files, and preview.
*/
function renderPiBrowser(data) {
    const piBrowser        = document.getElementById("piBrowser");
    const piBreadcrumb     = document.getElementById("piBreadcrumb");
    const piPreview        = document.getElementById("piPreview");
    const piPreviewImg     = document.getElementById("piPreviewImg");
    const piSelectedFileEl = document.getElementById("piSelectedFile");

    // Clear the folder view first
    piBrowser.innerHTML = "";

    // Show current path at the top
    piBreadcrumb.textContent = "/" + (piPath || "");

    // If not in root, show the "go up" button
    if (piPath !== "") {
        const back = document.createElement("div");
        back.textContent = "⬅ .. (terug)";
        back.className = "text-primary mb-2";
        back.style.cursor = "pointer";

        back.onclick = () => {
            // Go to parent folder
            const parent = piPath.split("/").slice(0, -1).join("/");
            loadPiDir(parent);
        };

        piBrowser.appendChild(back);
    }

    // List of folders
    (data.dirs || []).forEach((name) => {
        const folder = document.createElement("div");
        folder.textContent = "📁 " + name;
        folder.className = "p-1 rounded mb-1";
        folder.style.cursor = "pointer";

        folder.onclick = () => {
            const nextPath = (piPath ? piPath + "/" : "") + name;
            loadPiDir(nextPath);
        };

        piBrowser.appendChild(folder);
    });

    // List of files
    (data.files || []).forEach((name) => {
        const file = document.createElement("div");
        file.textContent = name;
        file.className = "p-1 rounded mb-1";
        file.style.cursor = "pointer";

        file.onclick = () => {
            const fullPath = (piPath ? piPath + "/" : "") + name;
            piSelected = fullPath;

            // Show selected file path
            piSelectedFileEl.textContent = "/" + fullPath;

            // Update preview
            piPreviewImg.src = `/pi/file/preview?path=${encodeURIComponent(fullPath)}`;
            piPreview.style.display = "block";
        };

        piBrowser.appendChild(file);
    });

    // If folder has nothing inside it
    if (!data.dirs && !data.files) {
        const empty = document.createElement("div");
        empty.textContent = "Deze map is leeg.";
        empty.className = "text-muted small";
        piBrowser.appendChild(empty);
    }
}

/*
  "Nieuw mapje" button handler
  Calls /pi-files/mkdir with JSON { path, name }
*/
async function onCreateFolderClick() {
  const name = prompt("Naam van de nieuwe map:");
  if (!name) {
    return;
  }

  try {
    const response = await fetch(PI_MKDIR_URL, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        path: piPath, // current folder
        name: name
      })
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("mkdir error:", data);
      alert("Kon map niet maken: " + (data.error || response.status));
      return;
    }

    // Reload current folder to show new directory
    loadPiDir(piPath);
  } catch (err) {
    console.error("mkdir exception:", err);
    alert("Er ging iets mis bij het maken van de map.");
  }
}

/*
  "Use Selected Pi File" button handler
  Calls /pi-files/use with JSON { path }
*/
async function onUsePiFileClick() {
  if (!piSelected) {
    alert("Geen bestand geselecteerd.");
    return;
  }

  try {
    const response = await fetch(PI_USE_URL, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        path: piSelected
      })
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("use error:", data);
      alert("Kon bestand niet gebruiken: " + (data.error || response.status));
      return;
    }

    // Optionally show a small confirmation
    alert("Bestand is naar de matrix gestuurd!");
  } catch (err) {
    console.error("use exception:", err);
    alert("Er ging iets mis bij het gebruiken van het bestand.");
  }
}
