// // Variables naming convention:
// //  - names of the jQuery object always start with `$`
// //  - variables without jQuery functionality don't have `$` sigh in names
// //  - Exact `$` variable is basic jQuery object

function hideAddButton(objectId) {
    const addButtonId = "#add_" + objectId;
    const addButton = $(addButtonId);
    addButton.css({"display": "none"});
}

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

function enableObject($object) {
    $object.css({
        "pointer-events": "auto",
        "touch-action": "auto",
        "background": "",
        "filter": "",
    });
}

function addButtonAction ($link, $editButton, $fieldObject, $additionalField) {
    $link.click(function (event) {
        event.preventDefault();
        event.stopPropagation();

        enableObject($editButton);
        enableObject($fieldObject);
        if ($additionalField) {
            enableObject($additionalField);
        }
        $link.remove();
    });
}

function createLink(linkId) {
    const imageSrc = "/static/unlock.svg";
    const imageAlt = "Разблокировать редактирование";
    const linkClass = "related-widget-wrapper-link change-related";
    let $image = $("<img>", { src: imageSrc, alt: imageAlt });
    let $link = $("<a>", { id: linkId, href: "#", class: linkClass });

    return $image.wrap($link).parent();
}

function unlockChangeButton(elementId, $editButton, $fieldObject, $additionalField) {
    var linkId = "unlock_" + elementId;
    $link = createLink(linkId)
    if ($editButton.length) {
        $editButton.after($link);
    } else {
        $fieldObject.after($link);
    }
    addButtonAction($link, $editButton, $fieldObject, $additionalField);
}

function disableAndAddUnlockButton($selectElement, url) {
    if ($selectElement.val()) {
        let elementId = $selectElement.attr("id");
        let lable = getLableName(elementId);
        let $select2Element = $(lable).eq(0);
        let $editButton = $('#change_' + elementId);
        let $select = $select2Element.length ? $select2Element : $selectElement;

        hideAddButton($selectElement.attr("id"));
        disableField($select);
        let $additionalField = null;
        if (url.includes("event")) {
            $additionalField = $("#id_type");
            disableField($additionalField);
        }
        if ($editButton) {
            disableButton($editButton);
            unlockChangeButton(elementId, $editButton, $select, $additionalField);
        }
    }
}

function limitChangeForDropdowns() {
    const relatedWidgets = $(".related-widget-wrapper");
    const $deleteButtons = relatedWidgets.find("[id^=delete_id_]");
    const url = $(location).attr('href').split("/");
    const excludePages = ["add", "users"];
    let isExcluded = url.filter(value => excludePages.includes(value)).length;

    $deleteButtons.each(function () {
        $( this ).css({"display": "none"});
    })

    if (isExcluded) {
        return
    }

    const $dropdowns = relatedWidgets.find("[id^=id_]");

    $dropdowns.each(function () {
        disableAndAddUnlockButton($( this ), url);
    })
    if (url.includes("partner")) {
        let $typeField = $("#id_type")
        disableAndAddUnlockButton($typeField, url);
    }
}

jQuery(window).on("load", function () {
    setTimeout(() => {
    // setTimeout for correct work in Firefox
        limitChangeForDropdowns()
    }, 0)
})
