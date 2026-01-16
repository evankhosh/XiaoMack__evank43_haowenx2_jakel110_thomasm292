const flip = (card) => {
  console.log("flipped");
  id = card.id;
  under_1 = id.indexOf("_");
  under_2 = id.lastIndexOf("_");
  card_id = id.substring(under_1 + 1, under_2);
  other_side_val = id.substring(under_2 + 1);

  curr = document.getElementById(id);

  other_side = document.createElement("div");
  other_side.setAttribute("onclick", "flip(this)");
  other_side.setAttribute("class", "card w-50 mx-auto py-10 align-items-center");
  other_side.setAttribute("role", "button");
  other_side.setAttribute("id", id + "_" + curr.textContent);

  inner_div = document.createElement("div");
  inner_div.setAttribute("class", "card-body");
  inner_div.textContent = other_side_val;

  other_side.append(inner_div);

  curr.before(other_side);
  curr.remove();
};
