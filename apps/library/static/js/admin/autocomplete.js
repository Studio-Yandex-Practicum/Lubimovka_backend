$(document).ready(function() {
    $("#id_common_event").select2({
        placeholder: "Выберите событие",
        allowClear: true,
        width: "180px",
    });
    $(".field-achievement select").select2({
        placeholder: "Выберите достижение",
        allowClear: true,
        width: "180px",
    });
    $(".field-play select").select2({
        placeholder: "Выберите пьесу",
        allowClear: true,
        width: "180px",
    });
    $(".field-author select").select2({
        placeholder: "Выберите человека",
        allowClear: true,
        width: "180px",
    });
    $(".field-person select").select2({
        placeholder: "Выберите человека",
        allowClear: true,
        width: "180px",
    });
    $(".field-role select").select2({
        placeholder: "Выберите роль",
        allowClear: true,
        width: "180px",
    });
    $(".field-image select").select2({
        placeholder: "Выберите изображение",
        allowClear: true,
        width: "180px",
    });

    $('tbody').bind("DOMNodeInserted",function(event){
        let el = event.target.querySelector("select");
        var obj = {
            "author": "человека",
            "achievement": "достижение",
            "play": "пьесу",
            "image": "изображение",
            "person": "человека",
            "role": "роль",
            "content_type": "тип объкта",
        };
        if (el) {
            let lastWord = el.id.split("-").slice(-1);
            if (lastWord in obj) {
                placeHolderWord = obj[lastWord]
                }
            else {
                placeHolderWord = "..."
            }
            $("#"+el.id).select2({
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
