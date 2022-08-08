def journalist_has_not_perms(request, obj):
    return request.user != obj.creator and request.user.groups.filter(name="journalist").exists()
