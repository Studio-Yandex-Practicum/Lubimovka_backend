$(document).ready(function() {
    $("#id_common_event").select2({
        placeholder: "Выберите событие",
        allowClear: true,
        width: "180px",
    });
    $("#id_Author_achievements-0-achievement").select2({
        placeholder: "Выберите достижение",
        allowClear: true,
        width: "180px",
    });
    $("#id_Author_plays-0-play").select2({
        placeholder: "Выберите пьесу",
        allowClear: true,
        width: "180px",
    });
    $("#id_Author_plays-2-0-play").select2({
        placeholder: "Выберите пьесу",
        allowClear: true,
        width: "180px",
    });
    $("#id_social_networks-0-name").select2({
        placeholder: "Выберите соцсеть",
        allowClear: true,
        width: "180px",
    });
    $("#id_Author_plays-0-author").select2({
        placeholder: "Выберите человека",
        allowClear: true,
        width: "180px",
    });
    $("#id_Author_plays-1-author").select2({
        placeholder: "Выберите человека",
        allowClear: true,
        width: "180px",
    });
    $("#id_volunteers-0-person").select2({
        placeholder: "Выберите человека",
        allowClear: true,
        width: "180px",
    });
    $(".field-role select").select2({
        placeholder: "Выберите роль",
        allowClear: true,
        width: "180px",
    });
    $("#id_Performance_images_in_block-0-image").select2({
        placeholder: "Выберите изображение",
        allowClear: true,
        width: "180px",
    });
    $("#id_Festival_images-0-image").select2({
        placeholder: "Выберите изображение",
        allowClear: true,
        width: "180px",
    });

    // trigger to add new elements to tree house
    $('tbody').bind("DOMNodeInserted",function(event){
        let element = event.target.querySelector("select");
        var obj = {
            "author": "человека",
            "achievement": "достижение",
            "play": "пьесу",
            "name": "соцсеть",
            "image": "изображение",
            "person": "человека",
            "role": "роль",
            "content_type": "тип объкта",
        };
        if (element) {
            let lastWord = element.id.split("-").slice(-1);
            if (lastWord in obj) {
                placeHolderWord = obj[lastWord]
                }
            else {
                placeHolderWord = "..."
            }
            $("#"+element.id).select2({
                placeholder: "Выберите " + placeHolderWord,
                allowClear: true,
                width: "180px",
            });
        }
    });
    $("#id_project").select2({
        placeholder: "Выберите проект",
        allowClear: true,
        width: "180px",
    });
    $("#id_person").select2({
        placeholder: "Выберите человека",
        allowClear: true,
        width: "180px",
    });
    $("#id_performance").select2({
        placeholder: "Выберите спектакль",
        allowClear: true,
        width: "180px",
    });
    $("#id_program").select2({
        placeholder: "Выберите программу",
        allowClear: true,
        width: "180px",
    });
    $("#id_festival").select2({
        placeholder: "Выберите фестиваль",
        allowClear: true,
        width: "180px",
    });
    $("#id_play").select2({
        placeholder: "Выберите пьесу",
        allowClear: true,
        width: "180px",
    });
    $("#id_type").select2({
        placeholder: "Выберите тип",
        allowClear: true,
        width: "180px",
    });
    $("#id_button").select2({
        placeholder: "Выберите тип кнопки",
        allowClear: true,
        width: "180px",
    });
});
