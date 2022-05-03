// // Variables naming convention:
// //  - names of the jQuery object always start with `$`
// //  - variables without jQuery functionality don't have `$` sigh in names
// //  - Exact `$` variable is basic jQuery object

function getLableName(elementId) {
    // Return lable attribute for select2 <span>
    return '[aria-labelledby="select2-' + elementId + '-container"]';
}

function disableField($object) {
    $object.css({
        "pointer-events": "none",
        "touch-action": "none",
        "background": "#eee"
    });
}

function disableButton($object) {
    $object.css({
        "pointer-events": "none",
        "touch-action": "none",
        "filter": "grayscale(100%)"
    });
}

function addCss($object) {
    $object.css({
        "pointer-events": "auto",
        "touch-action": "auto",
        "background": "",
        "filter": "",
    });
}

function addButtonAction ($link, $editButton, $fieldObject) {
    $link.click(function (event) {
        event.preventDefault();
        event.stopPropagation();
        let objects = [$editButton, $fieldObject]
        addCss($editButton);
        addCss($fieldObject);
    });
};

function createLink(linkId) {
    const imageSrc = "/static/admin/img/icon-viewlink.svg";
    const imageAlt = "Разблокировать редактирование";
    const linkClass = "related-widget-wrapper-link change-related";
    let $image = $("<img>", { src: imageSrc, alt: imageAlt });
    let $link = $("<a>", { id: linkId, href: "#", class: linkClass });

   return $image.wrap($link).parent();
};

function unlockChangeButton(elementId, $editButton, $fieldObject) {
    // const objectId = $object.attr("id");
    var linkId = "unlock_" + elementId;
    $link = createLink(linkId)
    $editButton.after($link);
    addButtonAction($link, $editButton, $fieldObject);
};

jQuery(window).on("load", function () {
    setTimeout(() => {
    // setTimeout for correct work in Firefox
        $(".related-widget-wrapper > [id^=add_id_]").remove();
        $(".related-widget-wrapper > [id^=delete_id_]").remove();
        const $dropdowns = $(".related-widget-wrapper > [id^=id_]")

        $dropdowns.each(function () {
            let elementId = $( this ).attr("id");
            let lable = getLableName(elementId);
            let $select2Element = $(lable).eq(0);
            let $editButton = $('#change_' + elementId)
            if ($( this ).val() != "" && $( this ).val() != null) {

                if (elementId === "id_play") {
                    console.log($( this ).val())
                    console.log("up")
                }

                if ($select2Element.length > 0) {
                    disableField($select2Element)
                } else {
                    disableField($( this ))
                }
                if ($editButton) {
                    disableButton($editButton)
                    if ($select2Element.length > 0) {
                        unlockChangeButton(elementId, $editButton, $select2Element);
                    } else {
                        unlockChangeButton(elementId, $editButton, $( this ));
                    }
                }
            }
        });
    }, 0)
});
