// Show an element
var show = function (elem) {
	elem.style.display = 'block';
};

// Hide an element
var hide = function (elem) {
	elem.style.display = 'none';
};

// Hide and show the target field based on select
function toggleChoices(){
    let selectField = document.getElementById('field_id').value,
        targetField = document.getElementById('field_id').value;

        if (selectField === 'ValueYouWant') {
            show(targetField);
        } else {
            hide(targetField);
        }
};

// Run the function when the page is loaded
window.onload = function(){
    toggleChoices();
}

