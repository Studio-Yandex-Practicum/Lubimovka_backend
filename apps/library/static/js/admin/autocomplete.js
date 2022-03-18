// autocomplete for Event
$(document).ready(function() {
    $("#id_common_event").select2({
        placeholder: "Выберите событие",
        allowClear: true
    });
// autocomplete for Person
    $("#id_person").select2({
        placeholder: "Выберите человека",
        allowClear: true
    });
// autocomplete for Project
    $("#id_project").select2({
        placeholder: "Выберите проект",
        allowClear: true
    });
// autocomplete for Performance
    $("#id_performance").select2({
        placeholder: "Выберите спектакль",
        allowClear: true,
        width: "200px",
    });
// autocomplete for Program
    $("#id_program").select2({
        placeholder: "Выберите программу",
        allowClear: true,
        width: "180px",
    });
// autocomplete for Festival
    $("#id_festival").select2({
        placeholder: "Выберите фестиваль",
        allowClear: true,
        width: "180px",
    });
// autocomplete for Play
    $("#id_play").select2({
        placeholder: "Выберите пьесу",
        allowClear: true,
        width: "180px",
    });

});
