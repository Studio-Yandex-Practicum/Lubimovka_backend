def content_delete_generic_related_items(content_module, super_delete_result) -> tuple[int, dict[str, int]]:
    """Take deleted `ContentModule` and delete generic related item. Return updated delete() result.

    DjangoModel's delete method has to return a tuple of amount and the dict of deleted objects.
    """
    count_deleted, dict_deleted = super_delete_result
    generic_related_item = content_module.item

    if generic_related_item is not None:
        count_generic_deleted, dict_generic_deleted = generic_related_item.delete()
        count_deleted += count_generic_deleted
        dict_deleted.update(dict_generic_deleted)

    return count_deleted, dict_deleted
