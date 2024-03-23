from django.db import models
from apps.authentication.models import User

from apps.core.models import BaseModel


class QedPrivilege(BaseModel):
    """
    QED Admin User Privileges
    """

    privilege_codes = {
        "MANAGE_USER": "User Management",
        "MANAGE_CRETERIA": "Criteria management",
        "MANAGE_CATEGORY": "Category management",
        "VIEW_REPORT": "View Reports",
        "SEND_PARTICIPANT_LIST": "Participant communication",
        "MANAGE_JOB": "Job management",
        "CREATE_DOCUMENTS": "Document Management",
        "CREATE_REPORT": "Generate Reports",
    }

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "QED Privilege"
        verbose_name_plural = "QED Privileges"

    def __str__(self) -> str:
        return f"{self.title}"


class QedRole(BaseModel):
    """
    QED Admin Roles
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "QED Role"
        verbose_name_plural = "QED Roles"

    def __str__(self) -> str:
        return f"{self.name}"


class QedRolePrivilege(BaseModel):
    """
    QED User Role privileges
    """

    qed_role = models.ForeignKey(
        QedRole, related_name="qed_super_role", on_delete=models.CASCADE
    )
    qed_privilege = models.ForeignKey(
        QedPrivilege, related_name="qed_privilege", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "QED Role Privilege"
        verbose_name_plural = "QED Role Privileges"
        unique_together = (('qed_role', 'qed_privilege',),)


class Qed(User):
    """
    QED admin users, inherits Django User
    """

    qed_role = models.ForeignKey(
        QedRole, related_name="system_admin", on_delete=models.CASCADE
    )
    password_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = " QED Admin"
        verbose_name_plural = "QED Admins"
