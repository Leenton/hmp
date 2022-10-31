


//Interact with the audio player. 

async function player(player_command, args = null){
    request_params = {
        command : player_command,
        data : args    
    }
    fetch('/api/player',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }, 
        body: JSON.stringify(request_params)
    }).then(response => {
        console.log("successfully did the thing you asked leenton")
    })
}

async function play(type, id){
    
    request = {
        type :  type,
        resouce_id : id
    }

    await player("play", request)
    //other shit to change the state of the player so we can make the web page more dyanmic. 
}

async function resume(){
    console.log("stuff")
    await player("resume")
    //other shit to change the state of the player so we can make the web page more dyanmic. 
}

async function pause(){
    await player("pause")
    //other shit to change the state of the player so we can make the web page more dyanmic. 
}
async function restart(){
    await player("restart")
    //other shit to change the state of the player so we can make the web page more dyanmic. 
}
async function back(){
    await player("back")
    //other shit to change the state of the player so we can make the web page more dyanmic. 
}
async function backback(){
    await player("backback")
    //other shit to change the state of the player so we can make the web page more dyanmic. 
}
async function forward(){
    await player("forward")
    //other shit to change the state of the player so we can make the web page more dyanmic. 
}
async function forwardforward(){
    await player("forwardforward")
    //other shit to change the state of the player so we can make the web page more dyanmic. 
}
function clear_tabs(){
    let tab = document.getElementById("library");
    tab.classList.remove("underline")
    tab = document.getElementById("playlists");
    tab.classList.remove("underline")
    tab = document.getElementById("scheduler");
    tab.classList.remove("underline")
}

async function load_player(){
    const resposne = await fetch('/api/test')
    const result = resposne.json()
    return result
}

async function load_library(){
    clear_tabs()
    let tab = document.getElementById("library");
    tab.classList.add("underline")
    fetch('/api/library',{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }, 
    }).then(
        response => response.json()
    ).then(
        data => {
            //empty out the  content container div, then insert each item we got in our web request.
            
            let container = document.getElementById("content");
            container.innerHTML = '';
            data.media.forEach(item => {
                let new_item = document.createElement('div')
                new_item.classList.add('library_item')
                new_item.innerHTML = [
                    `
                    <div class="media_name">
                        <p>`, item.name, `</p>
                    </div>
                    <p style="opacity:0.5;" class="hidden">Plays: `, item.plays, `</p>
                    <p>`, item.runtime, `</p>
                    <p>`, item.type, `</p>
                    <button onclick="load_media_modal()" class="hidden" id="media_edit">Edit</button>`].join("")
                new_item.ondblclick = () => play('media', item.id)
                container.appendChild(new_item)
            })
        }
    )
}

async function load_playlists(){
    clear_tabs()
    let tab = document.getElementById("playlists");
    tab.classList.add("underline")
    fetch('/api/playlists',{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }, 
    }).then(
        response => response.json()
    ).then(
        data => {
            //empty out the  content container div, then insert each item we got in our web request.
            
            let container = document.getElementById("content");
            container.innerHTML = '';
            data.media_lists.forEach(list => {
                let new_list = document.createElement('div')
                new_list.classList.add('list')
                new_list.innerHTML = [
                    `<div class="list-details">
                        <p>`, list.name, `</p>
                    </div>
                    <div class="list-actions">
                        <p>Type:`, list.type, `</p>
                        <p>Accepts Interupts:`, list.interuptable, `</p>
                        <button id="play">Play</button>
                        <button id="playlist_edit">Edit</button>
                    </div>`].join("")
                container.appendChild(new_list)
            })
        }
    )
}

async function load_scheduler(){
    clear_tabs()
    let tab = document.getElementById("scheduler");
    tab.classList.add("underline")
    fetch('/api/scheduler',{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }, 
    }).then(
        response => response.json()
    ).then(
        data => {
            //empty out the  content container div, then insert each item we got in our web request.
            let container = document.getElementById("content");
            container.innerHTML = '<p>Sorry! Nothing here yet!</p>';
            console.log(data)
        }
    )
}

// function load_action_modal(){
//     console.log("ACTION")
//     media_action_modal.style.display = "block"
// }

function load_media_modal(){
    console.log("WE WANT TO EDIT SOME MEDIA")
    media_modal.style.display = "block"
}

window.onclick = function(event) {
if (event.target == media_modal) {
    media_modal.style.display = "none";
}
}



