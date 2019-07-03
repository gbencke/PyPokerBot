

export function getCardCode(card){
  let startIndex = "A".charCodeAt(0);
  let SuiteOff = 0;
  let CardOff = 0;
  let ret = "";

  let numCards = parseInt(card.length / 2);
  for(let x = 0 ; x < numCards ; x++){
    let currentCard = card.substring(x * 2, (x+1) * 2);

    if(currentCard.substring(1,2) === "d"){ SuiteOff = 0; }
    if(currentCard.substring(1,2) === "h"){ SuiteOff = 1; }
    if(currentCard.substring(1,2) === "s"){ SuiteOff = 2; }
    if(currentCard.substring(1,2) === "c"){ SuiteOff = 3; }

    if(currentCard.substring(0,1) === 'A'){ CardOff = 0; }
    if(currentCard.substring(0,1) === '2'){ CardOff = 1; }
    if(currentCard.substring(0,1) === '3'){ CardOff = 2; }
    if(currentCard.substring(0,1) === '4'){ CardOff = 3; }
    if(currentCard.substring(0,1) === '5'){ CardOff = 4; }
    if(currentCard.substring(0,1) === '6'){ CardOff = 5; }
    if(currentCard.substring(0,1) === '7'){ CardOff = 6; }
    if(currentCard.substring(0,1) === '8'){ CardOff = 7; }
    if(currentCard.substring(0,1) === '9'){ CardOff = 8; }
    if(currentCard.substring(0,1) === 'T'){ CardOff = 9; }
    if(currentCard.substring(0,1) === 'J'){ CardOff = 10; }
    if(currentCard.substring(0,1) === 'Q'){ CardOff = 11; }
    if(currentCard.substring(0,1) === 'K'){ CardOff = 12; }

    codeToPrint = startIndex + (SuiteOff * 13 + CardOff);
    if(codeToPrint > 90) codeToPrint+=6;

    charToPrint = String.fromCharCode(codeToPrint);
    ret += charToPrint;
  }
  return ret;
}

