function login() {
    let username = $("#username").val();
    if(validate_username){
        eel.login(username);
    }
}

function validate_username(username) {
    return username.length > 0
}

eel.expose(handle_login);
function handle_login(username) {
    console.debug(`Logged in as ${username}`)
    $('#new_room').removeClass('hidden')
    $('#join_room').removeClass('hidden')
    $('.log-in').addClass('hidden')
}

function new_room() {
    let rounds = $('#rounds').val()
    eel.create_new_room(rounds)
}

function join_room() {
    let roomid = $('#room_id').val()
    eel.join_room(roomid)
}

eel.expose(go_to_room);
function go_to_room() {
    window.location = '/room.html'
}

eel.expose(handle_error);
function handle_error(err) {
    console.error(err)
}
