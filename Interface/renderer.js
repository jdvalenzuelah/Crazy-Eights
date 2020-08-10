//Iniciamos la libreria
cards.init({table:'#card-table', type:STANDARD});

//Crea una nueva baraja de cartas
deck = new cards.Deck();
//Por defecto está en el medio del contenedor, colóquelo ligeramente a un lado
deck.x -= 50;

//cards.all contiene todas las tarjetas, colóquelas todas en el
deck.addCards(cards.all);
deck.render({immediate:true});

//Ahora creemos un par de manos, una boca abajo y otra boca arriba.
upperhand = new cards.Hand({faceUp:false, y:60});
lowerhand = new cards.Hand({faceUp:true,  y:340});

//Vamos a agregar una pila de descarte
discardPile = new cards.Deck({faceUp:true});
discardPile.x += 50;


//Tratemos cuando se presione el botón Repartir:
$('#deal').click(function() {
	$('#deal').hide();
	//Aqui se reparte la cantidad que se desea de cartas, para cada uno de los jugadores
	deck.deal(5, [upperhand, lowerhand], 50, function() {
		discardPile.addCard(deck.topCard());
		discardPile.render();
	});
});

//Cuando haces clic en la carta superior de un mazo, se agrega una carta a tu mano
deck.click(function(card){
	if (card === deck.topCard()) {
		lowerhand.addCard(deck.topCard());
		lowerhand.render();
	}
});

/*Finalmente, cuando haces clic en una carta en tu mano, si es el mismo palo o rango que la carta superior de la pila 
de descarte luego se le agrega*/
lowerhand.click(function(card){
	if (card.suit == discardPile.topCard().suit
		|| card.rank == discardPile.topCard().rank) {
		discardPile.addCard(card);
		discardPile.render();
		lowerhand.render();
	}
});