let num_cards = 1

document.getElementById("add_btn").addEventListener("click", () => {
    ++num_cards;
    // store card count in value attr of create_btn
    create_btn = document.getElementById("create_btn");
    create_btn.setAttribute("value", String(num_cards))
    remove_existing_errors();

    front = "front_" + num_cards;
    back = "back_" + num_cards;

    const card_number = document.createElement("h3");
    card_number.textContent = "Card" + num_cards;

    const front_label = document.createElement("label");
    front_label.textContent = "Front:";
    front_label.setAttribute("for", front);

    const front_input = document.createElement("input");
    front_input.required = true;
    front_input.setAttribute("type", "text");
    front_input.setAttribute("id", front);
    front_input.setAttribute("name", front);

    const back_label = document.createElement("label");
    back_label.textContent = "Back:";
    back_label.setAttribute("for", back);

    const back_input = document.createElement("input");
    back_input.required = true;
    back_input.setAttribute("type", "text");
    back_input.setAttribute("id", back);
    back_input.setAttribute("name", back);


    const div = document.createElement("div");
    div.append(card_number);
    div.append(front_label);
    div.append(document.createElement("br"));
    div.append(front_input);
    div.append(document.createElement("br"));
    div.append(back_label);
    div.append(document.createElement("br"));
    div.append(back_input);
    div.append(document.createElement("br"));
    div.append(document.createElement("br"));

    const add_btn = document.getElementById("add_btn");
    add_btn.before(div);
});

document.getElementById("create_btn").addEventListener("click", (e) => {
    if (num_cards < 4) {
        e.preventDefault();
        console.log("Cannot create");

        remove_existing_errors();

        const error_msg = document.createElement("div");
        error_msg.textContent = "Cannot create flashcard set with less than 4 cards!";
        error_msg.setAttribute("id", "error_msg");
        error_msg.setAttribute("class", "alert alert-danger");
        error_msg.setAttribute("role", "alert")

        const add_btn = document.getElementById("add_btn");
        add_btn.before(error_msg);
    }
});

const remove_existing_errors = () => {
    existing_error = document.getElementById("error_msg");
    if (existing_error != null) {
        existing_error.remove();
    }
};