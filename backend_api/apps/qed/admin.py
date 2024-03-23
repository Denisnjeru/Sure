from django import apps
from django.contrib import admin

from .models import Qed, QedPrivilege, QedRole, QedRolePrivilege


@admin.register(Qed)
class QedAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "qed_role",
    ]

@admin.register(QedPrivilege)
class QedPrivilegeAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
    ]


@admin.register(QedRole)
class QedRoleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
    ]
    list_filter = ["name"]

@admin.register(QedRolePrivilege)
class QedRolePrivilegeAdmin(admin.ModelAdmin):
    list_display = [
        "qed_role",
        "qed_privilege",
    ]
    list_filter = ["qed_privilege"]