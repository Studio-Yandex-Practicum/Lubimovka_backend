def journalist_has_not_perms(request, obj):
    return request.user.groups.filter(name="journalist").exists() and request.user != obj.creator
