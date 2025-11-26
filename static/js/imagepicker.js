
URL = "imagelist"

/*
  Fetches directories and images from the server for a given path, then passes the returned data to buildUI() to display it.
*/
function getImages(path, parent){
    console.log(`getImages(${path}, ${parent})`)
    url = "imagelist"
    fetch(url, {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"path": path})
        })
        .then( (response) => { 
            return response.json(); /* promise object! */
        })
        .then( (data) => { 
            buildUI(data, parent);
        });
}

/*
  Sends the selected image path to the backend to display it on the LED matrix.
*/
function upload(path){
    console.log(`upload(${path})`)
    url = "imagelist_show"
    fetch(url, {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"path": path})
        })
        .then( () => { 
            // expection OK
        })
}

function _$(id){
    return document.getElementById(id);
}

/*
  Builds the folder tree UI:
  - Creates collapsible folders
  - Displays images inside folders
  - Supports nested folder levels
*/
function buildUI(data, parent) {
    console.log("buildUI", data, parent);


    if (parent === _$("dirs")) {
        parent.innerHTML = "";
    }

    // Directories
    data.dirs.forEach(dir => {
        // ep = wrapper row for a folder
        const ep = document.createElement("div");

        // eb = clickable folder button
        const eb = document.createElement("button");

        // ec = collapsible container holding child content
        const ec = document.createElement("div");

        // ef = container for child folders & images
        const ef = document.createElement("div");

        ep.classList.add("fullrow");
        eb.classList.add("collapsable");
        ec.classList.add("content", "fullrow");
        ef.classList.add("flexcontainer");

        // Folder label with icon and name
        eb.innerHTML = `<img class="image" src="${dir.ico}" alt="${dir.alt}"><span> ${dir.desc}</span>`;

        eb.addEventListener("click", () => {
            // Toggle the visual open/closed state
            eb.classList.toggle("active");

            // Only load the folder contents the first time it's opened
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

        // Thumbnail image
        e.innerHTML = `<img class="fleximage" src="${i.src}" alt="${i.alt}" title="${i.desc}">`;

        e.addEventListener("click", () => {
            // Remove previous selection highlight
            parent.querySelectorAll(".flexitem.selected").forEach(el => {
                el.classList.remove("selected");
            });
            e.classList.add("selected");

            upload(i.src);
        });

        parent.appendChild(e);
    });

    // No data
    if (data.imgs.length === 0 && data.dirs.length === 0 && parent.childNodes.length === 0) {
        parent.innerHTML = '<div style="display:block;"><span>-- LEEG --</span></div>';
    }
}

function init(){
    getImages("", _$("dirs"));
}


