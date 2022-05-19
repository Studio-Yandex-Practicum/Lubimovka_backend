// // Variables naming convention:
// //  - names of the jQuery object always start with `$`
// //  - variables without jQuery functionality don't have `$` sigh in names
// //  - Exact `$` variable is basic jQuery object

function hideAddButton(objectId) {
    const addButtonId = "#add_" + objectId;
    const addButton = $(addButtonId);
    addButton.attr("hidden", true);
}

function getSelect2Element(elementId) {
    // Return select2 <span>
    const lable = '[aria-labelledby="select2-' + elementId + '-container"]';
    return $(lable).eq(0)
}

function addButtonAction ($link, $editButton, $fieldObject, $additionalField) {
    $link.click(function (event) {
        event.preventDefault();
        event.stopPropagation();

        $editButton.removeClass("disabled-button");
        $fieldObject.removeClass("disabled-field");
        if ($additionalField) {
            $additionalField.removeClass("disabled-field");
        }
        $link.remove();
    });
}

function createLink(elementId) {
    const linkId = "unlock_" + elementId;
    const imageSrc = "/static/unlock-fill.svg";
    const title = "Разблокировать редактирование";
    const linkClass = "related-widget-wrapper-link change-related";
    let $image = $("<img>", { src: imageSrc, title: title, height: "20px" });
    let $link = $("<a>", { id: linkId, href: "#", class: linkClass });

    return $image.wrap($link).parent();
}

function unlockChangeButton(elementId, $editButton, $fieldObject, $additionalField) {
    $link = createLink(elementId)
    if ($editButton.length) {
        $editButton.after($link);
    } else {
        $fieldObject.after($link);
    }
    addButtonAction($link, $editButton, $fieldObject, $additionalField);
}

function disableAndAddUnlockButton($defaultSelectField, url) {
    if ($defaultSelectField.val()) {
        let fieldId = $defaultSelectField.attr("id");
        let $select2Element = getSelect2Element(fieldId);
        // If $select2Element is empty use default <select> tag - $defaultSelectField
        let $select = $select2Element.length ? $select2Element : $defaultSelectField;
        hideAddButton($defaultSelectField.attr("id"));
        $select.addClass("disabled-field");

        let $additionalField = null;
        if (url.includes("event")) {
            $additionalField = $("#id_type");
            $additionalField.addClass("disabled-field");
        }

        let $editButton = $('#change_' + fieldId);
        $editButton.addClass("disabled-button");
        unlockChangeButton(fieldId, $editButton, $select, $additionalField);
    }
}

function limitChangeForDropdowns() {
    const $relatedWidgets = $(".related-widget-wrapper");
    const $deleteButtons = $relatedWidgets.find("[id^=delete_id_]");
    const url = $(location).attr('href').split("/");
    const excludePages = ["add", "users"];

    $deleteButtons.each(function () {
        $( this ).attr("hidden", true);
    })

    // For users app pages and pages for creation new record limits are disabled
    let isExcluded = url.filter(value => excludePages.includes(value)).length;
    if (isExcluded) {
        return
    }

    const $dropdowns = $relatedWidgets.find("[id^=id_]");
    $dropdowns.each(function () {
        disableAndAddUnlockButton($( this ), url);
    })
    // Explicitly disable type field on Partners page
    if (url.includes("partner")) {
        let $typeField = $("#id_type");
        disableAndAddUnlockButton($typeField, url);
    }
}

jQuery(window).on("load", function () {
    setTimeout(() => {
    // setTimeout for correct work in Firefox
        limitChangeForDropdowns();
    }, 0)
})
