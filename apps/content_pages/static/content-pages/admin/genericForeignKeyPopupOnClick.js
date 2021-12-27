function genericForeignKeyPopupOnClick($, element, event) {

    function getCommonPrefix(id) {
        return id.replace("add_id_", "").replace("change_id_", "")
    }

    function getContentTypeFieldId(id, contentTypeFieldName) {
        var prefix = getCommonPrefix(id);
        prefix = prefix.substring(0, prefix.lastIndexOf("-") + 1);
        return prefix + contentTypeFieldName;
    }

    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    const contentTypeFieldName = JSON.parse(document.getElementById("content_type_field_name").textContent);

    var $this = $(element);
    var id = $this.attr('id');
    var commonPrefix = getCommonPrefix(id)
    var urls = JSON.parse(document.getElementById(commonPrefix + "_urls").textContent);

    var contentTypeFieldNameId = getContentTypeFieldId(id, contentTypeFieldName);

    var selected = $('select[name="' + contentTypeFieldNameId + '"]').find('option:selected');
    var contentTypeId = selected.val();
    var contentType = selected.text();

    if (!contentType) {
        alert('No content type found for GenericForeignKey lookup.');
        return false;
    }

    if (!contentTypeId) {
        alert('You must select: ' + contentTypeFieldNameId + '.');
        return false;
    }

    $this.attr('href', urls[contentTypeId]);
    return showRelatedObjectPopup(element);
};
