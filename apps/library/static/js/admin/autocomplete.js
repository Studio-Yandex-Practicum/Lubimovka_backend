// function adds select2

function setSelect2($, $objectId, $lastWord) {
    const $addAllowClear = true;
    const $addWidth = "400px";
    $("select#"+$objectId).select2({
        placeholder: "Выберите " + $lastWord,
        allowClear: $addAllowClear,
        width: $addWidth,
    })
};
// for connect new autocomplete: add to dir object last word of your select id
function filterSelect(element) {
    var object = {
        "author": "человека",
        "performance": "спектакль",
        "play": "пьесу",
        "person": "человека",
        "event": "событие",
    };
    let lastWord = element.id.split(/_|-/).slice(-1);
    if (lastWord in object && !(element.id.includes("__prefix__"))) {
        return [
            element.id,
            object[lastWord]
            ];
        };
    }

$(document).ready(function() {
    const elementsSelect = document.getElementsByTagName("select");
    const hasCollapse = document.getElementsByClassName("js-inline-admin-formset inline-group");
    if (elementsSelect.length && elementsSelect[0].id || hasCollapse.length) {
        for (element of elementsSelect) {
            let remainElement = filterSelect(element);
            if (remainElement) {
                setSelect2($, remainElement[0], remainElement[1]);
            }
        }
        // trigger to add new elements to tree house
        $('tbody').bind("DOMNodeInserted",function(event){
            let elements = event.target.querySelectorAll("select");
            if (elements) {
                for (element of elements) {
                    let remainElement = filterSelect(element);
                    if (remainElement) {
                        setSelect2($, remainElement[0], remainElement[1]);
                    }
                }
            }
        });
    }
});
