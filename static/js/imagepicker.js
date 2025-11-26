
URL = "imagelist"


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

function buildUI(data, parent) {
    console.log("buildUI", data, parent);


    if (parent === _$("dirs")) {
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

        eb.innerHTML = `<img class="image" src="${dir.ico}" alt="${dir.alt}"><span> ${dir.desc}</span>`;

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
        e.innerHTML = `<img class="fleximage" src="${i.src}" alt="${i.alt}" title="${i.desc}">`;

        e.addEventListener("click", () => {
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


