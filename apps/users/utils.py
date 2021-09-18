class _Perms:
    """
    Base class for permissions checker
    """

    def has_add_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_change_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_delete_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_view_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_module_permission(self, request):
        return True


class AdminOnlyPermissionsMixin(_Perms):
    """
    Give all rights for admin
    """

    def check_perm(self, user_obj):
        if user_obj.is_anonymous:
            return False
        if user_obj.is_admin or user_obj.is_superuser:
            return True
        return False


class EditorAndAdminPermissionsMixin(_Perms):
    """
    Give all rights for editor and admin
    """

    def check_perm(self, user_obj):
        if user_obj.is_anonymous:
            return False
        if user_obj.is_superuser or user_obj.is_admin or user_obj.is_editor:
            return True
        return False
