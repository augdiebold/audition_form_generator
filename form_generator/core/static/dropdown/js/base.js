// Show an element
var show = function (elem) {
	elem.style.display = 'block';
};

// Hide an element
var hide = function (elem) {
	elem.style.display = 'none';
};

function toggleChoices(id){
    let choiceId = id.replace('field_type', 'choices'),
        fieldType = document.getElementById(id).value,
        choicesField = document.getElementById(choiceId);

        if (fieldType === 'ChoiceField') {
            show(choicesField);
        } else {
            hide(choicesField);
        }
};