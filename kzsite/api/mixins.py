from .permission import IsStaffEditorPermission

from rest_framework import permissions


class StaffEditorPermissionMixin:
    permission_classses = [permissions.IsAdminUser, IsStaffEditorPermission]
    