def check_journalist_perms(request, obj, journalist=None):
    """Journalist can edit only own items."""
    visitor = request.user
    journalist = journalist or visitor.is_staff
    if journalist and visitor != obj.creator:
        return 0
    return 1
