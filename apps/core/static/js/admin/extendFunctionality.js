// add place holder in search field
// add autoscrolling to side panel
window.onload = function() {
    document.getElementsByClassName("current-app")[0].scrollIntoView();
    var searchbar = document.getElementById("searchbar");
    if (searchbar) {
        searchbar.placeholder = "Введите данные для поиска";
    }
};
