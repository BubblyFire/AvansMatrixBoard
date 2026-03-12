let selectedPath = null;

function getImages(path, parent) {
    fetch("imagelist", {
        method: "post",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({ path })
    })
    .then(r => r.json())
    .then(data => buildUI(data, parent));
}

function selectImage(src, name) {
    selectedPath = src;

    document.querySelectorAll(".flexitem.selected").forEach(el => el.classList.remove("selected"));

    document.getElementById("previewImg").src = src;
    document.getElementById("previewImg").alt = name;
    document.getElementById("previewName").textContent = name;
    document.getElementById("noSelectionMsg").style.display = "none";
    document.getElementById("previewContent").style.display = "block";

    const btn = document.getElementById("sendBtn");
    btn.disabled = false;
    btn.textContent = IP_STRINGS.send_btn;
}

function sendSelected() {
    if (!selectedPath) return;

    const btn = document.getElementById("sendBtn");
    btn.disabled = true;
    btn.textContent = IP_STRINGS.sending;

    fetch("imagelist_show", {
        method: "post",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({ path: selectedPath })
    })
    .then(() => {
        showToast(IP_STRINGS.sent);
        btn.disabled = false;
        btn.textContent = IP_STRINGS.send_btn;
    });
}

function buildUI(data, parent) {
    if (parent === document.getElementById("dirs")) {
        parent.innerHTML = "";
    }

    // Directories
    data.dirs.forEach(dir => {
        const ep = document.createElement("div");
        const eb = document.createElement("button");
        const ec = document.createElement("div");
        const ef = document.createElement("div");

        ep.classList.add("fullrow");
        eb.classList.add("collapsable");
        ec.classList.add("content", "fullrow");
        ef.classList.add("flexcontainer");

        eb.innerHTML = `<img class="image" src="${dir.ico}" alt="${dir.alt}"><span>${dir.desc}</span>`;

        eb.addEventListener("click", () => {
            eb.classList.toggle("active");
            if (eb.classList.contains("active") && ef.childNodes.length === 0) {
                getImages(dir.src, ef);
            }
        });

        ep.appendChild(eb);
        ep.appendChild(ec);
        ec.appendChild(ef);
        parent.appendChild(ep);
    });

    // Images
    data.imgs.forEach(i => {
        const e = document.createElement("div");
        e.classList.add("flexitem");
        e.innerHTML = `<img class="fleximage" src="${i.src}" alt="${i.alt}"><span class="flexlabel">${i.desc}</span>`;

        e.addEventListener("click", () => {
            e.classList.add("selected");
            selectImage(i.src, i.desc);
        });

        parent.appendChild(e);
    });

    // Empty state
    if (data.imgs.length === 0 && data.dirs.length === 0 && parent.childNodes.length === 0) {
        parent.innerHTML = `<div class="ip-empty">${IP_STRINGS.empty}</div>`;
    }
}

function init() {
    getImages("", document.getElementById("dirs"));
}
