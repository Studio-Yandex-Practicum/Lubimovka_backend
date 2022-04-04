// function adds select2
function setSelect2($, $objectId, $placeHolder) {
    const $addAllowClear = true;
    const $addWidth = "180px";
    return $($objectId).select2({
        placeholder: $placeHolder,
        allowClear: $addAllowClear,
        width: $addWidth,
    })
};

$(document).ready(function() {
    setSelect2($, "select#id_project", "Выберите проект");
    setSelect2($, "select#id_person", "Выберите человека");
    setSelect2($, "select#id_performance", "Выберите спектакль");
    setSelect2($, "select#id_program", "Выберите программу");
    setSelect2($, "select#id_festival", "Выберите фестиваль");
    setSelect2($, "select#id_play", "Выберите пьесу");
    setSelect2($, "select#id_type", "Выберите тип");
    setSelect2($, "select#id_button", "Выберите тип кнопки");
    setSelect2($, "#id_common_event", "Выберите событие");
    setSelect2($, "#id_Author_achievements-0-achievement", "Выберите достижение");
    setSelect2($, "select#id_Author_plays-0-play", "Выберите пьесу");
    setSelect2($, "select#id_Author_plays-2-0-play", "Выберите пьесу");
    setSelect2($, "select#id_social_networks-0-name", "Выберите соцсеть");
    setSelect2($, "select#id_Author_plays-0-author", "Выберите человека");
    setSelect2($, "select#id_Author_plays-1-author", "Выберите человека");
    setSelect2($, "select#id_volunteers-0-person", "Выберите человека");
    setSelect2($, "select#id_Performance_images_in_block-0-image", "Выберите изображение");
    setSelect2($, "select#id_Festival_images-0-image", "Выберите изображение");

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
                    width: "180px",
                });
            }
        }
    });
});
