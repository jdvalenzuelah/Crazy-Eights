
let username = ""
let roomid = ""

cards.init({table:'#card-table', type:STANDARD});

deck = new cards.Deck();

deck.x -= 50;

deck.addCards(cards.all);
deck.render({immediate:true});

upperhand = new cards.Hand({faceUp:false, y:60});
lowerhand = new cards.Hand({faceUp:true,  y:340});

$('#deal').click(function(){
    start_game()
    $('#deal').hide()
})

lowerhand.click(function(card){
    if (card.suit == discardPile.topCard().suit
        || card.rank == discardPile.topCard().rank
        || card.rank == '8') {     
		discardPile.addCard(card);
		discardPile.render();
        lowerhand.render();
        eel.make_move(card.suit, card.rank)
	}
})

discardPile = new cards.Deck({faceUp:true});
discardPile.x += 50;

eel.expose(on_turn);
function on_turn(card) {
    alert('Your turn')
}

function login() {
    username = $("#username").val();
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
    let room_id = $('#room_id').val()
    eel.join_room(room_id)
}

eel.expose(after_joined);
function after_joined(room_id) {
    $('#new_room').addClass('hidden')
    $('#join_room').addClass('hidden')
    $('#waiting').removeClass('hidden')
    update_room_id(room_id)
}

eel.expose(after_created);
function after_created(room_id) {
    $('#new_room').addClass('hidden')
    $('#join_room').addClass('hidden')
    $('#card-table').removeClass('hidden')
    update_room_id(room_id)
}

function update_room_id(room_id) {
    roomid = room_id
    console.log('updating room id')
    document.getElementById('roomid1').innerText = `Room id: ${roomid}`
    document.getElementById('roomid2').innerText = `Room id: ${roomid}`
}

function start_game() {
    eel.start_game()
}

eel.expose(on_game_started);
function on_game_started(player_deck, current_card) {
    $('#waiting').addClass('hidden')
    $('#start_game').addClass('hidden')
    $('#cardimg').removeClass('hidden')

    let incomming_deck = parse_python_deck(player_deck).map(function(el){
        return new cards.Card(el.suit, el.rank)
    })
    
    deck.add_specific(lowerhand, 50, incomming_deck, function(){
        console.log('Callback xd');
    });

    current_card = parse_python_card(current_card);
    current_card = new cards.Card(current_card.suit, current_card.rank)

    deck.deal(5, [upperhand], 50, function() {
        tempcard = deck.topCard()
        tempcard.rank = current_card.rank
        tempcard.suit = current_card.suit
		discardPile.addCard(tempcard);
		discardPile.render();
    });       
}

ranks_lookup = {
    'A': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': '10',
    'J': '11',
    'Q': '12',
    'K': '13'
}

suits_lookup = {
    'clubs': 'c',
    'diamonds': 'd',
    'hearts': 'h',
    'spades': 's'
}
function parse_python_deck(pdeck) {
    let trimmed = pdeck.replace('[', '').replace(']', '')
    let cards = trimmed.split(';')

    return cards.map(function(el){
        return parse_python_card(el)
    })

}

function parse_python_card(pcard) {
    let splited = pcard.split(',')
    return {
        suit: suits_lookup[splited[1]],
        rank: ranks_lookup[splited[0]]
    }
}

eel.expose(handle_error);
function handle_error(err) {
    console.error(err)
}
