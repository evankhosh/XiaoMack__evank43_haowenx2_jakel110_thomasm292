var card = 1;
var flipped = false;
card_content = document.getElementById("card-content");
card_content.innerText = flashcards[0][0];

var flip = function() {
  card_content = document.getElementById("card-content");

  if (!flipped) {
    card_content.innerText = flashcards[card - 1][1];
    flipped = true;
  } else {
    card_content.innerText = flashcards[card - 1][0];
    flipped = false;
  }
};

var nextCard = function() {
  card += 1;
  if (card >= flashcards.length) {
    card = flashcards.length;
    next_card_btn = document.getElementById("next-card-btn");
    next_card_btn.style.visibility = "hidden";
    return;
  }

  if (card == flashcards.length) {
    next_card_btn = document.getElementById("next-card-btn");
    next_card_btn.style.visibility = "hidden";
  }

  if (card > 1) {
    prev_card_btn = document.getElementById("prev-card-btn");
    prev_card_btn.style.visibility = "visible";
  }

  card_content = document.getElementById("card-content");
  card_content.innerText = flashcards[card - 1][0];
  flipped = false;
};

var prevCard = function() {
  card -= 1;
  if (card < 1) {
    card = 1;    
    prev_card_btn = document.getElementById("prev-card-btn");
    prev_card_btn.style.visibility = "hidden";
    return;
  }

  if (card == 1) {
    prev_card_btn = document.getElementById("prev-card-btn");
    prev_card_btn.style.visibility = "hidden";
  }

  if (card < flashcards.length) {
    next_card_btn = document.getElementById("next-card-btn");
    next_card_btn.style.visibility = "visible";
  }

  card_content = document.getElementById("card-content");
  card_content.innerText = flashcards[card - 1][0];
  flipped = false;
};
