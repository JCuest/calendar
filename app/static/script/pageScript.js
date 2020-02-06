function editorTabNext(obj){
    var eventId = /[0-9]/.exec(obj.id);
    var base = window.location.href

    if(eventId){
        eventId = parseInt(eventId);
        base += "/" + eventId;

        window.location.replace(base);
    }

}

function editorTabPast(obj){
    var eventId = /[0-9]/.exec(obj.id);
    var base = window.location.href

    if(eventId){
        eventId = parseInt(eventId);
        base += "/" + eventId;

        window.location.replace(base);
    }

}

function openMenu(){
    var icon = document.getElementById('menu_icon');
    var menu = document.getElementById('header_scroll_menu');
    var menu_ul = document.getElementById('header_menu');

    if(icon.innerHTML == "menu"){
        icon.innerHTML = "close";
        menu.style.display = "flex";
        menu_ul.style.display = "flex";
    }

    else {
        icon.innerHTML = "menu";
        menu.style.display = "none";
        menu_ul.style.display = "none";
    }
    
}

function showFriends(){
    var list = document.getElementById('friend_block_event');
    list.style.display = "flex";
}

function hideFriends(){
    var list = document.getElementById('friend_block_event');
    list.style.display = "none";
}


function sendEvent(){

}