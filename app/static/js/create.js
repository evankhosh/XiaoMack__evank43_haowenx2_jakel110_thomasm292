let num_cards = 1

document.getElementById("add_btn").addEventListener("click", () => {
    ++num_cards;
    console.log(num_cards);
    front = "front_" + num_cards;
    back = "back_" + num_cards;

    const card_number = document.createElement("h3");
    card_number.textContent = "Card" + num_cards;

    const front_label = document.createElement("label");
    front_label.textContent = "Front:";
    front_label.setAttribute("for", front);

    const front_input = document.createElement("input");
    front_input.setAttribute("type", "text");
    front_input.setAttribute("id", front);
    front_input.setAttribute("name", front);

    const back_label = document.createElement("label");
    back_label.textContent = "Back:";
    back_label.setAttribute("for", back);

    const back_input = document.createElement("input");
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