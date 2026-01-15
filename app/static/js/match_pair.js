var front_selected = null;
var back_selected = null;
var incorrect = false;

var select_front = function(front_id) {
    if (incorrect) {
        unhighlight_incorrect();
    }

    if (front_selected != null){
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

    if (back_selected != null){
        unhighlight_selected(back_selected);
    }

    back_selected = document.getElementById(back_id);
    highlight_selected(back_selected);

    if (front_selected != null && back_selected != null) {
        match();
    }
}

var match = function() {
    
}

var highlight_selected = function(element) {

}

var unhighlight_selected = function(element) {

}

var highlight_correct = function() {


    front_selected = null;
    back_selected = null;
}

var highlight_incorrect = function() {

}

var unhighlight_incorrect = function() {


    front_selected = null;
    back_selected = null;
}