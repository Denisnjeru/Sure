from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.suppliers.models import SupplierCompany, SupplierCompanyProfile

# Signals for Automatically  creating a supplier profile on  user signup
@receiver(post_save, sender=SupplierCompany)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        SupplierCompanyProfile.objects.create(supplier_company=instance)


@receiver(post_save, sender=SupplierCompany)
def save_user_profile(sender, instance, **kwargs):
    supplier_company_obj = SupplierCompany.objects.filter(id=instance.id).first()
    SupplierCompanyProfile.objects.get(supplier_company=supplier_company_obj).save()
