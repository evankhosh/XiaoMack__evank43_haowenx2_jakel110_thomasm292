let question = 0
function get_random_int(max) {
    return Math.floor(Math.random() * max);
}

const generate_q = () => {
    const q = document.getElementById("question");
    num_cards = Number(q.dataset.num_cards);

    question = get_random_int(num_cards);
    let chosen = [question];
    question_front = document.getElementById("q_" + chosen[0]);
    question_front.setAttribute("class", question_front.getAttribute("class").replace("d-none", "")); 

    ans_correct = document.getElementById("ans_" + chosen[0]);
    ans_correct.setAttribute("class", ans_correct.getAttribute("class").replace("d-none", "")); 

    for (let i = 0; i < 3; i++) {
        let c = get_random_int(num_cards);
        while (chosen.includes(c)) {
            c = get_random_int(num_cards);
        }
        chosen.push(c);

        ans = document.getElementById("ans_" + c);
        ans.setAttribute("class",  ans_correct.getAttribute("class").replace("d-none", ""));
    }
};

const clear_q = () => {
    const q = document.getElementById("question");
    num_cards = Number(q.dataset.num_cards);

    for (let i = 0; i < num_cards; i++) {
        console.log(i);
        front = document.getElementById("q_" + i);
        if (!front.getAttribute("class").includes("d-none")) {
            if (front.getAttribute("class") === "") {
                front.setAttribute("class", "d-none");
            } else {
                front.setAttribute("class", "d-none " + front.getAttribute("class"));
            }
        }
        back = document.getElementById("ans_" + i);
        if (!back.getAttribute("class").includes("d-none")) {
            if (back.getAttribute("class") === "") {
                back.setAttribute("class", "d-none");
            } else {
                back.setAttribute("class", "d-none " + back.getAttribute("class"));
            }
        }
    }
}

const remove_msg = () => {
    const msg = document.getElementById("msg");
    if (msg != null) {
        msg.remove();
    }
}

const check_ans = (ans_id) => {
    id = Number(ans_id);
    remove_msg();

    if (id == question) {
        console.log("Correct");
        msg = document.createElement("h2");
        msg.setAttribute("id", "msg");
        msg.setAttribute("class", "text-success");
        msg.textContent = "Correct!";
        form = document.getElementById("question");
        form.after(msg);
        clear_q();
        generate_q();
    } else {
        console.log("wrong");
        msg = document.createElement("h2");
        msg.setAttribute("id", "msg");
        msg.setAttribute("class", "text-danger");
        msg.textContent = "Wrong :(";
        form = document.getElementById("question");
        form.after(msg);
    }

};