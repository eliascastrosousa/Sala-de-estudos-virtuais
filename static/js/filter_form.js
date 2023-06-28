let inputs = document.getElementsByTagName("input");
let selectInput = document.getElementById("id_category");
var filterDiv = document.getElementById('filters-div');
var pTags = filterDiv.querySelectorAll('p');

for (let j = 0; j < pTags.length; j++){
    pTags[j].classList.add("col");
}

for (let i = 0; i < inputs.length; i++) {
    inputs[i].classList.add("form-control");
    inputs[i].classList.add("w-1/2");
}

selectInput.classList.add("form-control");
selectInput.classList.add("w-1/2");