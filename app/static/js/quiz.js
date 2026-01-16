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
    question_front.setAttribute("class", question_front.getAttribute("class").substring(6)); 

    ans_correct = document.getElementById("ans_" + chosen[0]);
    ans_correct.setAttribute("class", ans_correct.getAttribute("class").substring(6)); 

    for (let i = 0; i < 3; i++) {
        let c = get_random_int(num_cards);
        while (chosen.includes(c)) {
            c = get_random_int(num_cards);
        }

        ans = document.getElementById("ans_" + c);
        ans.setAttribute("class",  ans_correct.getAttribute("class").substring(6));
    }
};

const clear_q = () => {
    const q = document.getElementById("question");
    num_cards = Number(q.dataset.num_cards);

    for (let i = 0; i < num_cards; i++) {
        front = document.getElementById("q_" + i);
        if (!front.getAttribute("class").includes("d-none")) {
            front.setAttribute("class", "d-none " + back.getAttribute("class"))
        }
        back = document.getElementById("ans_" + i);
        if (!back.getAttribute("class").includes("d-none")) {
            back.setAttribute("class", "d-none " + back.getAttribute("class"))
        }
    }
}

const check_ans = (ans_id) => {
    id = Number(ans_id);

    if (id == question) {
        console.log("Correct");
        clear_q();
        generate_q();
    } else {
        console.log("wrong");
    }

};