function callPython() {eel.hello();}

function Cards(aSuit, Avalue){
    this.aSuit = aSuit;
    this.Avalue = Avalue;
}

Cards.prototype = {
    /*Tamaño de las cartas*/
    width: 70, 
    height: 95,
    pixel: 15,

    getSuit: function(){return this.suit;},
    getValue: function(){return this.value;},

    /*Retornamos en string cada carta*/
    toString: function(){
        return this.value + this.suit;
    },

    getURL: function(){return "../images" + this.toString() + ".svg";},

    getBackURL: function(){return "../images/cardback_red.svg";},
};