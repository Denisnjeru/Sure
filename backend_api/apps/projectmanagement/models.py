from django.db import models
from apps.core.models import BaseModel, Job
from django.core.validators import FileExtensionValidator
from backend.storage_backends import PrivateMediaStorage

# Create your models here.
def gant_charts(instance, filename):
    return "%s/%s/%s" % (
        "gant_charts",
        instance.company.company_name.replace(" ", "_"),
        filename,
    )

class Timeline(BaseModel):
    """
    Job timelines including gant charts
    """
    company = models.ForeignKey('buyer.Company', related_name="company_timelines", on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_timelines")
    approved_gantt_chart = models.FileField(
        upload_to=gant_charts,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "xlsx",
                    "xls",
                    "zip",
                    "rar",
                ]
            )
        ],
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )
    actual_gantt_chart = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = "Project Timeline"
        verbose_name_plural = "Projects Timelines"
        ordering = ('-id',)

    def __str__(self) -> str:
        return f"{self.job.job_title} Project Timeline"

def meeting_files(instance, filename):
    return "%s/%s/%s" % (
        "meeting_files",
        instance.company.company_name.replace(" ", "_"),
        filename,
    )

class Meeting(BaseModel):
    """
    QED/Client Meetings
    """
    company = models.ForeignKey('buyer.Company', related_name="company_meetings", on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_meetings")
    meeting_minutes = models.FileField(
        upload_to=meeting_files,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "xlsx",
                    "xls",
                    "zip",
                    "rar",
                ]
            )
        ],
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )
    date = models.DateField()

    class Meta:
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"
        ordering = ('-id',)

    def __str__(self) -> str:
        return f"{self.job.job_title} Meeting Minutes"