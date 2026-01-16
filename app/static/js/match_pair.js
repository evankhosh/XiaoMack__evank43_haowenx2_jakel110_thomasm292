var front_selected = null;
var back_selected = null;
var all_selected = [];
var incorrect = false;

var select_front = function(front_id) {
    if (incorrect) {
        unhighlight_incorrect();
    }

    if (front_selected != null || front_selected == document.getElementById(front_id)){
        unhighlight_selected(front_selected);
    }

    front_selected = document.getElementById(front_id);
    highlight_selected(front_selected);

    if (front_selected != null && back_selected != null) {
        match();
    }
}

var select_back = function(back_id) {
    if (incorrect) {
        unhighlight_incorrect();
    }

    if (back_selected != null || back_selected == document.getElementById(back_id)){
        unhighlight_selected(back_selected);
    }

    back_selected = document.getElementById(back_id);
    highlight_selected(back_selected);

    if (front_selected != null && back_selected != null) {
        match();
    }
}

var match = function() {
    var correct = false;

    for (flashcard of flashcards) {
        if (front_selected.firstElementChild.textContent == flashcard[0] &&
            back_selected.firstElementChild.textContent == flashcard[1]) {
            correct = true;
            break;
        }
    }
    if (correct) {
        highlight_correct();
    } else {
        highlight_incorrect();
    }
}

var reset = function() {
    for (element of all_selected) {
        element.style.backgroundColor = "white";
    }

    all_selected = [];
    front_selected = null;
    back_selected = null;
    incorrect = false;
}

var highlight_selected = function(element) {
    element.style.backgroundColor = "yellow";
    all_selected.push(element);
}

var unhighlight_selected = function(element) {
    element.style.backgroundColor = "white";
    all_selected = all_selected.filter(e => e != element);
}

var highlight_correct = function() {
    front_selected.style.backgroundColor = "lightgreen";
    back_selected.style.backgroundColor = "lightgreen";

    front_selected = null;
    back_selected = null;
}

var highlight_incorrect = function() {
    front_selected.style.backgroundColor = "lightcoral";
    back_selected.style.backgroundColor = "lightcoral";
    all_selected.push(front_selected, back_selected);

    incorrect = true;
}

var unhighlight_incorrect = function() {
    front_selected.style.backgroundColor = "white";
    back_selected.style.backgroundColor = "white";
    all_selected = all_selected.filter(e => e != front_selected && e != back_selected);

    front_selected = null;
    back_selected = null;
    incorrect = false;
}