from typing import Dict, Tuple


def abstract_content_delete_generic_related_items(object) -> Tuple[int, Dict[str, int]]:
    """Delete generic related items.

    Model's delete method has to return amount and dict of deleted objects.
    Return 0 and empty dict if no related item is found.
    """
    item = object.item
    count_item_deleted, dict_item_deleted = 0, dict()
    if item is not None:
        count_item_deleted, dict_item_deleted = item.delete()
    return count_item_deleted, dict_item_deleted
