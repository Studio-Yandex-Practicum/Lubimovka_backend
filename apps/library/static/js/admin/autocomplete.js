// function adds select2
function setSelect2($, $objectId, $placeHolder) {
    const $addAllowClear = true;
    const $addWidth = "250px";
    //const $excludeSelect = $(".form-row.empty-form select").attr('id');
    //const $exSelect = $('select').not("[id!="+$excludeSelect+"]")

    //return $($objectId+$exSelect).select2({
    return $($objectId).select2({
        sorter: function(results) {
            return results.sort((a, b) => a.text.toLowerCase().localeCompare(b.text.toLowerCase()))
        },
        placeholder: $placeHolder,
        allowClear: $addAllowClear,
        width: $addWidth,
    })
};

$(document).ready(function() {

    setSelect2($, ".field-achievement select", "Выберите достижение");
    setSelect2($, ".field-play select", "Выберите пьесу");
    setSelect2($, ".field-name select", "Выберите соцсеть");
    setSelect2($, ".field-author select", "Выберите человека");
    setSelect2($, ".field-image select", "Выберите изображение");
    setSelect2($, ".field-person select", "Выберите человека");
    setSelect2($, ".field-role select", "Выберите роль");
    setSelect2($, ".field-content_type select", "Выберите тип");
    setSelect2($, "select#id_performance", "Выберите спектакль");
    setSelect2($, "select#id_program", "Выберите программу");
    setSelect2($, "select#id_festival", "Выберите фестиваль");
    setSelect2($, "select#id_button", "Выберите тип кнопки");
    setSelect2($, "select#id_common_event", "Выберите событие");

    // trigger to add new elements to tree house
    $('tbody').bind("DOMNodeInserted",function(event){
        let elements = event.target.querySelectorAll("select");
        var $obj = {
            "author": "человека",
            "achievement": "достижение",
            "play": "пьесу",
            "name": "соцсеть",
            "image": "изображение",
            "person": "человека",
            "role": "роль",
            "content_type": "тип объкта",
        };
        var element;
        if (elements) {
            for (element of elements) {
                let lastWord = element.id.split("-").slice(-1);
                if (lastWord in $obj) {
                    placeHolderWord = $obj[lastWord]
                    }
                else {
                    placeHolderWord = "..."
                }
                $("select#"+element.id).select2({
                    placeholder: "Выберите " + placeHolderWord,
                    allowClear: true,
                    width: "250px",
                });
            }
        }
    });
});
