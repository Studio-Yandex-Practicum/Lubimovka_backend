// Variables naming convention:
//  - names of the jQuery object always start with `$`
//  - variables without jQuery functionality don't have `$` sigh in names
//  - Exact `$` variable is basic jQuery object

const imageSrc = "/static/admin/img/icon-changelink.svg";
const imageAlt = "Изменить";
const linkClass = "related-widget-wrapper-link change-related";

function removeLinks($, $object) {
    let prefixes = ["change_", "delete_"]
    if ($object.val() != "") {
        prefixes.push("add_")
    };
    prefixes.forEach(function(item, index, array) {
        let linkName = item + $object.attr("id");
        let $link = $("#" + linkName);
        $link.remove();
    });
};

function createLink(linkId) {
    let $image = $("<img>", { src: imageSrc, alt: imageAlt });
    let $link = $("<a>", { id: linkId, href: "#", class: linkClass });

   return $image.wrap($link).parent();
};

function addLinkAction ($link, $object) {
    $link.click(function (event) {
        event.preventDefault();
        event.stopPropagation();
        $object.css({
            "pointer-events": "auto",
            "touch-action": "auto",
            "background": "",
        });
    });
};

function appendChangeButton($object) {
    const objectId = $object.attr("id");
    var linkId = "change_" + objectId;
    $link = createLink(linkId)
    $object.after($link);
    addLinkAction($link, $object);
};

function appendChangeButtonForSelect2($object) {
    var lable = $object.attr("aria-labelledby")
    const foreignKeyFieldId = lable.split("-")[1]
    var $parentSpan = $object.parent().parent()
    var linkId = "change_" + foreignKeyFieldId;
    $link = createLink(linkId)
    $parentSpan.after($link);
    addLinkAction($link, $object);
};

function getLableName($object) {
    // Return lable attribute for select2 <span>
    const objectId = $object.attr("id");
    return '[aria-labelledby="select2-' + objectId + '-container"]';
};

function disableField($object) {
    $object.css({
        "pointer-events": "none",
        "touch-action": "none",
        "background": "#eee"
    });
};

jQuery(document).ready(function () {
    const $foreignKeyClass = $(".foreign-key-field");
    const add_edit_button = $("#change_button_for_foreign_key").attr("value") === "true";
    var is_selec2 = false;

    $foreignKeyClass.each(function () {
        let lable = getLableName($( this ))
        let $element = $(lable).eq(0)
        removeLinks($, $( this ));
        if ($( this ).val() != "") {
            if ($element.length > 0) {
                disableField($element)
                is_selec2 = true;
            } else {
                disableField($( this ))
                is_selec2 = false;
            }
            if (add_edit_button) {
                if (is_selec2) {
                    appendChangeButtonForSelect2($element);
                } else {
                    appendChangeButton($( this ));
                }
            };
        };
    });
});
