function genericForeignKeyPopupOnClick($, element, event) {
    
    function getContentTypeFieldId(id, contentTypeFieldName) {
        var prefix = id.substring(0, id.lastIndexOf("-") + 1)
        prefix = prefix.replace("id_href_", "")
        return prefix + contentTypeFieldName
    }
    
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    const contentTypeFieldName = JSON.parse(document.getElementById("content_type_field_name").textContent);

    var $this = $(element);
    var id = $this.attr('id');
    var contentTypeFieldNameId = getContentTypeFieldId(id, contentTypeFieldName)
    var urls = JSON.parse(document.getElementById(id + "_urls").textContent);

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
