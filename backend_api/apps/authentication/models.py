from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel

# Create your models here.

User = get_user_model()

class VerificationCode(BaseModel):
    user = models.ForeignKey(
        User,
        related_name="user_verification_code",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    code = models.IntegerField()

    class Meta:
        verbose_name = "Verification Code"
        verbose_name_plural = "Verification Codes"

    def __str__(self):
        return f'{self.user.email} - {self.code}'


class UserVisit(BaseModel):
    """
    Record of a user visiting the site on a given day.
    This is used for tracking and reporting
    """

    user = models.ForeignKey(
        User,
        related_name="user_visit",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    url = models.TextField(help_text="Url visited by user")
    session_key = models.CharField(help_text="Django session identifier", null=True, max_length=40)
    remote_addr = models.CharField(
        help_text=(
            "Client IP address (from X-Forwarded-For HTTP header, "
            "or REMOTE_ADDR request property)"
        ),
        max_length=100,
        blank=True,
    )
    ua_string = models.TextField(
        "User agent (raw)",
        help_text="Client User-Agent HTTP header",
        blank=True,
    )