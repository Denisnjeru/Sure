from unicodedata import category
from django import apps, template

from apps.rfq.models import Category, SupplierRfqTotal


register = template.Library()


@register.filter(name="supplier_rfq_total")
def supplier_rfq_total(supplier_id, category_id):
    supplier = (
        apps.apps.get_model("suppliers", "Supplier")
        .objects.filter(id=supplier_id)
        .first()
    )
    rfq = Category.objects.filter(id=category_id).first()
    if supplier is not None and rfq is not None:
        response = SupplierRfqTotal.objects.filter(
            supplier=supplier, category=rfq
        ).first()
        if response is not None:
            return round(response.score, 2)
    return "N/A"


@register.filter(name="supplier_rfq_responses")
def supplier_rfq_responses(supplier_id, category_id):
    responses = apps.apps.get_model("rfq", "RFQItemResponse").objects.filter(
        supplier_id=supplier_id, rfq_item__category_id=category_id
    )
    if responses.count() > 0:
        return responses
    return None


@register.filter(name="supplier_rfq_rank")
def supplier_rfq_rank(supplier_id, category_id):
    rfq_score = (
        apps.apps.get_model("rfq", "SupplierRfqTotal")
        .objects.filter(category_id=category_id, supplier_id=supplier_id)
        .first()
    )
    return rfq_score.rank
