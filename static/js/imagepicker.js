
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

function buildUI(data, parent){
    console.log(`buildUI(${data}}, ${parent})`);
    console.log(data);
  

    data.dirs.forEach(dir =>{
        var ep = document.createElement('div');
        var eb = document.createElement('button');
        var ec = document.createElement('div');
        var ef = document.createElement('div');
        ep.classList.add('fullrow');
        eb.classList.add('collapsable');
        ec.classList.add('content');
        ec.classList.add('fullrow');
        ef.classList.add('flexcontainer');
        // ef.classList.add('');
        eb.innerHTML = `<img class="image" src="${dir.ico}"><span> ${dir.desc}</span>`
        eb.addEventListener('click', (ev)=>{
            eb.classList.toggle('active'); 
            ec.classList.toggle('content');
            if (ef.childNodes.length == 0){
                getImages(dir.src,ef);
            }
        })
        eb.data = dir;
        ep.appendChild(eb);
        ec.appendChild(ef);
        parent.appendChild(ep);
        parent.appendChild(ec);
    })


    data.imgs.forEach(i=>{
        var e = document.createElement('div');
        e.classList.add('flexitem')
        e.innerHTML = `<img class="fleximage" src="${i.src}" alt="${i.alt}" title="${i.desc}">`
        parent.appendChild(e);
        e.addEventListener('click', ()=>{upload(i.src)})
    })

    if (data.imgs.length == 0 && data.dirs.length == 0){
        parent.innerHTML='<div style="display:block;"><span>-- LEEG --</span></div>';
    }


    //   <div class="image">{{ img['url'] }}</div>
}

function init(){
    getImages("", _$("dirs"));
}


