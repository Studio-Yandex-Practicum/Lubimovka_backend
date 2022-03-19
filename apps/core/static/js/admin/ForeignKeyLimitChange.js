// Variables naming convention:
//  - names of the jQuery object always start with `$`
//  - variables without jQuery functionality don't have `$` sigh in names
//  - Exact `$` variable is basic jQuery object

function removeLinks($, $object) {
    let prefixes = ["change_", "delete_"]
    if ($object.val() != "") {
        prefixes.push("add_")
    };
    prefixes.forEach(function(item, index, array) {
        let linkName = item + $object.attr("id");
        let $link = $(document.getElementById(linkName));
        $link.remove();
    });
};

function appendLink($, $object) {
    const objectIdValue = $object.val();
    const objectId = $object.attr("id");

    if (objectIdValue != "") {
        var linkId = "change_" + objectId;
        var imageSrc = "/static/admin/img/icon-changelink.svg";
        var imageAlt = "Изменить";
        var linkClass = "related-widget-wrapper-link change-related";
    };

    let $image = $("<img>", { src: imageSrc, alt: imageAlt });
    let $link = $("<a>", { id: linkId, href: "#", class: linkClass });

    $link = $image.wrap($link).parent();
    $object.after($link);

    $link.click(function (event) {
        event.preventDefault();
        event.stopPropagation();
        $object.prop("disabled", false);
        $object.css({
            "pointer-events": "auto",
            "touch-action": "auto",
            "background": "",
        });
    });
};

jQuery(document).ready(function ($) {
    const foreignKeyClass = $(".foreign-key-field");

    foreignKeyClass.each(function () {
        if ($( this ).val() != "") {
            $( this ).css({
                "pointer-events": "none",
                "touch-action": "none",
                "background": "#eee"
            });
        };
        removeLinks($, $( this ));
        appendLink($, $( this ));
    });
});
