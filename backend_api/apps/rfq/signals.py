from django import apps
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.rfq.models import Category, SupplierRfqTotal, Rfq
from apps.rfq.reports import supplier_rfq_pdf_report
from apps.rfq.tasks import create_rfq_items


@receiver(post_save, sender=Category)
def create_items(sender, instance, created, **kwargs):
    """
    Create RFQ Items from category
    """
    if created:
        print(instance)
        # call async task to create items
        create_rfq_items(instance.id)
    # else:
    #     print(instance)
    #     cat_obj=instance
    #     create_rfq_items(cat_obj.id)


@receiver(post_save,sender=SupplierRfqTotal)
def create_rfq_summary_pd(sender, instance, created, **kwargs):
    """
    Create supplier PDF response on submit
    """
    if created:
        supplier_rfq_pdf_report.delay(instance.supplier_id,instance.category_id)
    else:
        supplier_rfq_pdf_report.delay(instance.supplier_id,instance.category_id)  


@receiver(post_save, sender=Rfq)
def create_job_instance_in_core(sender, instance, **kwargs):
    company_id = instance.company_id
    activity_id = ContentType.objects.filter(model='rfq').first()
    apps.apps.get_model('core', 'Job').objects.update_or_create(
        company_id=company_id, title=instance.title,
        sourcing_activity=activity_id, target_id=instance.id,
        defaults={
            "unique_reference": instance.unique_reference,
        }
    )