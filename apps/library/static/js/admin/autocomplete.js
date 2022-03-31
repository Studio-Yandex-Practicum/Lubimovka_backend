$(document).ready(function() {
    $("#id_common_event").select2({
        placeholder: "Выберите событие",
        allowClear: true,
        width: "180px",
    }); // class="form-row dynamic-Author_achievements"
    //$(function () {
    //    Suit.after_inline.register('init_select2', function(inline_prefix, row){
    //        $(row).find('select').select2();
    //    });
    //}(Suit.$));
    //$(".field-achievement").select2({
    //    placeholder: "Выберите событие",
    //    allowClear: true,
    //    width: "180px",
    //});
    $("#id_person").select2({
        placeholder: "Выберите человека",
        allowClear: true,
        width: "180px",
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
