from django import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Prequalification


@receiver(post_save, sender=Prequalification)
def create_job_instance_in_core(sender, instance, **kwargs):
    company_id = instance.company_id
    activity_id = ContentType.objects.filter(model='prequalification').first()
    apps.apps.get_model('core', 'Job').objects.update_or_create(
        company_id=company_id, title=instance.title,
        sourcing_activity=activity_id, target_id=instance.id,
        defaults={
            "unique_reference": instance.unique_reference,
        }
    )
