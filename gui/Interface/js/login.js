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
    window.location = '/room.html'
}

eel.expose(handle_error);
function handle_error(err) {
    console.error(err)
}


eel.expose(deck);
function deck (cards){
    console.debug(`your deck ${cards}`)

}