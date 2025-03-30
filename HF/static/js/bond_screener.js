let form = document.getElementById('main_form');
let button = document.getElementById('reset-button');

button.addEventListener('click', () => form.reset());

var win_wigth = window.screen.width;
alert("Hello world");

if (win_wigth > 900) {
    const collection = document.getElementsByClassName("pc-only");
    alert(collection.length);
    while(collection.length) {
        collection[0].remove();
    }
}