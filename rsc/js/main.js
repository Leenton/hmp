


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

function close_modal(){
    modal.classList.add("hidden")
    for (let modal_action of document.querySelectorAll(".modal-content:not(.disabled)")){
        modal_action.remove()
    }

    //instead of hiding modal it shall now instead just delete the modal from the dom, remove it's existance. POG
    //java scirpt generated modals instead since then they can carry stuff like media ids and etc
    //general action modals can be loaded from javascript as well and use JS to infer data and configure themselves acordingly. 
}

function clear_tabs(){
    let tab = document.getElementById("library")
    tab.classList.remove("underline")
    tab = document.getElementById("playlists")
    tab.classList.remove("underline")
    tab = document.getElementById("scheduler")
    tab.classList.remove("underline")
}

async function load_player(){
    return "Hello"
}

async function load_library(){
    clear_tabs()
    library.classList.add("underline")
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
            
            content.innerHTML = '';
            data.media.forEach(item => {
                let new_item = document.createElement('div')
                new_item.classList.add('library-item')
                new_item.innerHTML = [`
                    <div class="media-name">
                        <p>`, item.name, `</p>
                    </div>
                    <p style="opacity:0.5;" class="hidden">Plays: `, item.plays, `</p>
                    <p>`, item.runtime, `</p>
                    <p>`, item.type, `</p>
                    <button onclick="load_media_modal('`, btoa(JSON.stringify(item)) ,`')" class="hidden edit" id="media_edit">Edit</button>`].join('')
                new_item.ondblclick = () => play('media', item.id)
                content.appendChild(new_item)
            })
        }
    )
}

async function load_playlists(){
    clear_tabs()
    playlists.classList.add("underline")
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
            
            content.innerHTML = '';
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
                        <button class="edit" id="playlist_edit">Edit</button>
                    </div>`].join("")
                content.appendChild(new_list)
            })
        }
    )
}

async function load_scheduler(){
    clear_tabs()
    scheduler.classList.add('underline')
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
            content.innerHTML = '<p>Sorry! Nothing here yet!</p>';
            console.log(data)
        }
    )
}

// function load_action_modal(){
//     console.log("ACTION")
//     media_action_modal.style.display = "block"
// }

function load_media_modal(input){
    let item = JSON.parse(atob(input))
    modal.classList.remove('hidden')
    let media_editor_modal = document.createElement('form')
    media_editor_modal.action = './api/library'
    media_editor_modal.method = 'POST'
    media_editor_modal.enctype = 'multipart/form-data'
    media_editor_modal.classList.add('modal-content','media-edit')
    media_editor_modal.id = 'media_editor'
    let inner = [`
        <input type="hidden" name="media_id" value="`, item['id'] ,`">
        <div class="media-item-image">
            <div class="media-cover-image">
                <img src='./rsc/images/pink.jpg'>
            </div>
            <div>
                <p>Plays: `, item['plays'] ,`</p>
                <p>Runtime: `, item['runtime'] ,`</p>
                <p>Created: `, (new Date(parseInt(parseFloat(item['created'] * 1000)))).toLocaleDateString("en-GB") ,`</p>
            </div>
        </div>
        <div class="modal-options">
            <label for="media_name">Name</label>
            <input type="text" autocomplete="off" name="media_name" id="media_name" value="`, item['name'],`"/>
            <label for="media_type">Media type</label>
            <select id="media_type" name="media_type">
                <option value="music">Music</option>
                <option value="podcast">Podcast</option>
                <option value="weather">Weather</option>
                <option value="effect">Effect</option>
            </select>
            <label for="media_cover">Cover</label>
            <input type="file" name="media_cover" id="media_cover" accept=".jpg, .png, .jpeg, .gif, .mp3, .wav, .flac" size="536870912">
            <div class="actions">
                <button name="req_type" id="media-save" value="edit">Save</button>
                <button name="req_type" id="media-delete" value="delete">Delete</button>
            </div>
        </div>
    `].join('')
    let split = '<option value="' + item['type'] + '"'
    inner = inner.split(split)
    media_editor_modal.innerHTML = [inner[0], split + ' selected', inner[1]].join('')
    document.body.appendChild(media_editor_modal)
}
