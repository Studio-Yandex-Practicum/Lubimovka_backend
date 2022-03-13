

document.write('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>');
document.write('<script type="text/javascript" src="../jquery.slugit.js"></script>')
//<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
//<script type="text/javascript" src="../jquery.slugit.js"></script>
jQuery(document).ready(function ($) {
    let personSelectField = $("#id_person");
    // #result_list > tbody > tr:nth-child(1) > td.field-slug
    var a = $('#id_person option:selected').text();
    //alert(a);
    //let translateText(text) = $(function(){
    //    $(text).slugIt();
    //});
    var b = $(function(){
        $('кто').slugIt();
    });
    alert(a);
    alert(b.val());
    //alert(translateText('кто'));
    //alert(translateText(a));
    personSelectField.change(function () {
        $('#id_slug').val($('#id_person option:selected').text());
        //$('#id_slug').val(translateText(a));
    });
});
