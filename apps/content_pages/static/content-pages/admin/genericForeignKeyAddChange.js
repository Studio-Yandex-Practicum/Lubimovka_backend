function disableNotSelectedOptions(func_variable) {
    if (func_variable.val() != "") {
        func_variable.find(":not(:selected)").prop('disabled', true);
    };
};

function getAPILink($, $link, contentTypeIdValue, objectIdValue, link_type) {
    $.ajax({
        url: "/api/v1/content-pages/get-content-type-link/",
        data: {
            link_type: link_type,
            model_id: contentTypeIdValue,
            object_id: objectIdValue,
        },
        success: function (response) {
            console.log(response.url);
            $link.attr('href', response.url);
        },
        errors: function (response) {
            console.log("error")
        }
    })
};

function addLink($, $contentTypeId, $objectId) {
    const contentTypeIdValue = $contentTypeId.val();
    const objectIdValue = $objectId.val();
    const objectId = $objectId.attr("id");

    if (contentTypeIdValue != "" && objectIdValue == "") {
        const addLinkId = "add_" + objectId;
        const $image = $("<img>", {
            src: "/static/admin/img/icon-addlink.svg",
            alt: "Добавить",
        })
        let $addLink = $("<a>", {
            id: addLinkId,
            href: "#",
            class: "related-widget-wrapper-link add-related",
        });
        $addLink = $image.wrap($addLink).parent();
        $contentTypeId.after($addLink);
        getAPILink($, $addLink, contentTypeIdValue, objectIdValue, "add");
    };
    if (contentTypeIdValue != "" && objectIdValue != "") {
        const changeLinkId = "change_" + objectId;
        const $image = $("<img>", {
            id: changeLinkId + "_image",
            src: "/static/admin/img/icon-changelink.svg",
            alt: "Изменить",
        })
        let $changeLink = $("<a>", {
            id: changeLinkId,
            href: "#",
            class: "related-widget-wrapper-link change-related",
        });
        $changeLink = $image.wrap($changeLink).parent();
        $contentTypeId.after($changeLink);
        getAPILink($, $changeLink, contentTypeIdValue, objectIdValue, "change");
    };
};

function getPrefix($this) {
    let id = $this.attr("id");
    let prefix = id.substring(0, id.lastIndexOf("-") + 1);
    return prefix
};

function getObjectIdFieldName($this) {
    let prefix = getPrefix($this);
    return prefix + "object_id";
};

function getObjectId($, $this) {
    const objectIdFieldName = getObjectIdFieldName($this);
    return $(document.getElementById(objectIdFieldName));
};

function getContentTypeIdFieldName($this) {
    let prefix = getPrefix($this);
    return prefix + "content_type";
};

function getContentTypeId($, $this) {
    const contentTypeIdFieldName = getContentTypeIdFieldName($this);
    return $(document.getElementById(contentTypeIdFieldName));
};

function getAddLinkFieldName($this) {
    const objectFieldName = getObjectIdFieldName($this);
    return "add_" + objectFieldName;
};

function removeAddLink($, $objectId) {
    const addLinkFieldName = getAddLinkFieldName($objectId);
    const $addLinkId = $(document.getElementById(addLinkFieldName));
    $addLinkId.remove();
};

jQuery(document).ready(function ($) {
    const contentTypeFields = $(".content-pages-content-type");
    const objectIDFields = $(".content-pages-object-id")

    objectIDFields.change(function () {
        const $objectId = $(this);
        const $contentTypeId = getContentTypeId($, $objectId);
        removeAddLink($, $objectId);
        addLink($, $contentTypeId, $objectId);
    });

    contentTypeFields.change(function () {
        const $contentTypeId = $(this);
        const $objectId = getObjectId($, $contentTypeId);
        disableNotSelectedOptions($contentTypeId);
        addLink($, $contentTypeId, $objectId);
    });

    contentTypeFields.change()

});
