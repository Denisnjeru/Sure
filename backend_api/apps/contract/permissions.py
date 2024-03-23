from rest_framework import permissions


class isQedorBuyer(permissions.BasePermission):

    edit_methods = ("GET",)

    def has_permission(self, request, view):
        if request.user.company:
            return True
