$(document).ready(function() {
    $("#id_common_event").select2({
        placeholder: "Выберите событие",
        allowClear: true
    });
    $("#id_person").select2({
        placeholder: "Выберите человека",
        allowClear: true,
    });
    $("#id_project").select2({
        placeholder: "Выберите проект",
        allowClear: true
    });
    $("#id_performance").select2({
        placeholder: "Выберите спектакль",
        allowClear: true,
        width: "200px",
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
});
