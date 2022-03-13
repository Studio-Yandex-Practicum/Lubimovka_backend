window.onload = function() {
    document.getElementsByClassName("current-app")[0].scrollIntoView();
    var searchbar = document.getElementById("searchbar");
    if (searchbar) {
        searchbar.placeholder = "Введите данные для поиска";
    }
};
