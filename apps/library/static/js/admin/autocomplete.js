// function adds select2

function setSelect2($, $objectId, $lastWord) {
    let $placeHolderWord = "..."
    const $addAllowClear = true;
    const $addWidth = "400px";
    // for connect new autocomplete: add to dir $obj last word of your select id
    var $obj = {
        "author": "человека",
        "performance": "спектакль",
        "play": "пьесу",
        "person": "человека",
        "event": "событие",
    };
    if ($lastWord in $obj) {
        $placeHolderWord = $obj[$lastWord];
    }
    if ($lastWord in $obj && !($objectId.includes("__prefix__"))) {
        $("select#"+$objectId).select2({
            sorter: function(results) {
                return results.sort((a, b) => a.text.toLowerCase().localeCompare(b.text.toLowerCase()))
            },
            placeholder: "Выберите " + $placeHolderWord,
            allowClear: $addAllowClear,
            width: $addWidth,
        })
    }
};

$(document).ready(function() {
    const elementsSelect = document.getElementsByTagName("select");
    const hasCollapse = document.getElementsByClassName("js-inline-admin-formset inline-group");
    if (elementsSelect.length && elementsSelect[0].id || hasCollapse.length) {
        for (element of elementsSelect) {
            let lastWord = element.id.split(/_|-/).slice(-1);
            setSelect2($, element.id, lastWord);
        }
        // trigger to add new elements to tree house
        $('tbody').bind("DOMNodeInserted",function(event){
            let elements = event.target.querySelectorAll("select");
            if (elements) {
                for (element of elements) {
                    let lastWord = element.id.split(/_|-/).slice(-1);
                    setSelect2($, element.id, lastWord);
                }
            }
        });
    }
});
