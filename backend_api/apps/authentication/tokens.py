from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.buyer.models import Buyer
from apps.suppliers.models import Supplier, SupplierCompany


def get_user_type(user_id):
    if Supplier.objects.filter(id=user_id).exists():
        user_type = "supplier"
    elif Buyer.objects.filter(id=user_id).exists():
        user_type = "buyer"
    else:
        user_type = "qed"

    return user_type


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        user_type = get_user_type(user.id)

        token["user_id"] = user.id
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["user_type"] = user_type
        if user_type == "buyer":
            buyer = Buyer.objects.filter(id=user.id).first()
            token["company_id"] = buyer.company.id
            token["company_name"] = buyer.company.company_name
            token["company_logo"] = buyer.company.company_logo_url.url if buyer.company.company_logo_url else ""
        if user_type == "supplier":
            # supplier = SupplierCompany.objects.filter(
            #     admin_supplier=user
            # ).first()
            supplier = Supplier.objects.filter(id=user.id).first()
            token["company_name"] = supplier.supplier_company.company_name
            token["company_id"] = supplier.supplier_company.id
            # SupplierCompany.objects.filter(
            #     admin_supplier=user
            # ).values_list("id", flat=True)[0]

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
