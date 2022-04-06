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
        let $link = $(document.getElementById(linkName));
        $link.remove();
    });
};

function setAttributes(el, attrs) {
    for(var key in attrs) {
        el.setAttribute(key, attrs[key]);
    };
};

function appendLink($, $object) {
    const objectId = $object.attr("id");

    var linkId = "change_" + objectId;

    let $image = $("<img>", { src: imageSrc, alt: imageAlt });
    let $link = $("<a>", { id: linkId, href: "#", class: linkClass });

    $link = $image.wrap($link).parent();
    $object.after($link);

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

function appendLinkForSelect2(object) {
    var lable = object.getAttribute('aria-labelledby')
    const foreignKeyFieldId = lable.split("-")[1]
    const parentSpan = object.parentElement.parentElement

    var linkId = "change_" + foreignKeyFieldId;

    let image = document.createElement('img')
    setAttributes(image, {"src": imageSrc, "alt": imageAlt})
    let link = document.createElement('a');
    setAttributes(link, {"id": linkId, "href": "#", 'class': linkClass});
    link.insertAdjacentElement("beforeend", image)

    parentSpan.after(link);

    link.onclick = function (event) {
        event.preventDefault();
        event.stopPropagation();
        object.style.cssText = 'pointer-events:auto;touch-action:auto;background:""';
    };
};

function getLableName($object) {
    // Return lable attribute for select2 <span>
    const objectId = $object.attr("id");
    return '[aria-labelledby="select2-' + objectId + '-container"]';
}

jQuery(document).ready(function ($) {
    const foreignKeyClass = $(".foreign-key-field");
    const add_edit_button = $("#change_button_for_foreign_key").attr("value") === "true";
    var is_selec2 = false;

    foreignKeyClass.each(function () {
        let lable = getLableName($( this ))
        let element = document.querySelector(lable)
        removeLinks($, $( this ));
        if ($( this ).val() != "") {
            if (element) {
                element.style.cssText = "pointer-events:none;touch-action:none;background:rgb(238, 238, 238)";
                is_selec2 = true;
            } else {
                $( this ).css({
                    "pointer-events": "none",
                    "touch-action": "none",
                    "background": "#eee"
                });
                is_selec2 = false;
            }
            if (add_edit_button) {
                if (is_selec2) {
                    appendLinkForSelect2(element);
                } else {
                    appendLink($, $( this ));
                }
            };
        };
    });
});
