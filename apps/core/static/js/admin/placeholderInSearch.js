window.onload = function() {
    document.getElementById("searchbar").placeholder = "Введите данные для поиска";
    items = document.getElementsByClassName("collapse-toggle");
    for (i = 0; i < items.length; i++) {
        items[i].click();
    }
};
