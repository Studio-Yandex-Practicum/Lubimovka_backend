function disableNotSelectedOptions(func_variable) {
    if (func_variable.val() != "") {
        func_variable.find(":not(:selected)").prop('disabled', true);
    };
};

function getLinkAndClick($, $link, contentTypeIdValue, objectIdValue, link_type) {
    $.ajax({
        url: "/api/v1/content-pages/get-content-type-link/",
        data: {
            link_type: link_type,
            model_id: contentTypeIdValue,
            object_id: objectIdValue,
        },
        success: function (response) {
            $link.attr("href", response.url);
            $link.off("click");
            $link.click();
        },
        error: function (response) {
            console.log(response);
            alert("Не удалось получить ссылку 😞");
            $link.removeAttr("href");
        }
    });
};

function addLink($, $contentTypeId, $objectId) {
    const contentTypeIdValue = $contentTypeId.val();
    const objectIdValue = $objectId.val();
    const objectId = $objectId.attr("id");

    if (contentTypeIdValue === "") {
        return;
    };

    if (contentTypeIdValue != "" && objectIdValue == "") {
        var linkType = "add";
        var linkId = "add_" + objectId;
        var imageSrc = "/static/admin/img/icon-addlink.svg";
        var imageAlt = "Добавить";
        var linkClass = "related-widget-wrapper-link add-related";
    };
    if (contentTypeIdValue != "" && objectIdValue != "") {
        var linkType = "change";
        var linkId = "change_" + objectId;
        var imageSrc = "/static/admin/img/icon-changelink.svg";
        var imageAlt = "Изменить";
        var linkClass = "related-widget-wrapper-link change-related";
    };

    let $image = $("<img>", { src: imageSrc, alt: imageAlt });
    let $link = $("<a>", { id: linkId, href: "#", class: linkClass });

    $link = $image.wrap($link).parent();
    $contentTypeId.after($link);

    $link.click(function (event) {
        event.preventDefault();
        event.stopPropagation();
        getLinkAndClick($, $link, contentTypeIdValue, objectIdValue, linkType);
    });
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
    const contentTypeClass = $(".content-pages-content-type");
    const objectIdClass = $(".content-pages-object-id")

    objectIdClass.change(function () {
        const $objectId = $(this);
        const $contentTypeId = getContentTypeId($, $objectId);
        removeAddLink($, $objectId);
        addLink($, $contentTypeId, $objectId);
    });

    contentTypeClass.change(function () {
        const $contentTypeId = $(this);
        const $objectId = getObjectId($, $contentTypeId);
        disableNotSelectedOptions($contentTypeId);
        addLink($, $contentTypeId, $objectId);
    });

    contentTypeClass.change();

});
