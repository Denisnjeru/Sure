from django.utils.translation import gettext_lazy as _
import pytz
import traceback
from datetime import datetime
from rest_framework.utils import model_meta
from rest_framework import serializers
from django.core.exceptions import ValidationError
from apps.core.models import CategoryType
from .models import (
    Auction, AuctionInvitee, AuctionItems, AuctionItemImage,
    AuctionItemResponses, AuctionItemResponsesTracking, AuctionTotalItemResponse
)
from apps.suppliers.models import Supplier
from .utils import (
    ValidateIfInMemoryUploadedFile
)

def validate_date(opening_date, closing_date):
    # Validating the opening and closing dates 
    utc = pytz.UTC
    open_date = opening_date
    close_date = closing_date
    time_now = utc.localize(datetime.now())
        
    if time_now > close_date or close_date < open_date:
        raise ValidationError(
            _("The opening date, closing date and today's date dont compare well."),
        )
    elif close_date > open_date < time_now:
        return True
    elif close_date > open_date > time_now:
        return False


class AuctionOpenSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Auction
        fields = [
            "id",
            "closing_date",
        ]

    def create(self, validated_data):
        auction = Auction.objects.filter(id=validated_data["id"]).first()
        if not auction.status_open:
            auction.status_open = True
            auction.closing_date = validated_data["closing_date"]
            auction.save()
        return auction

class AuctionCreateSerializer(serializers.ModelSerializer):
    category_type = serializers.PrimaryKeyRelatedField(queryset=CategoryType.objects.all(), 
        required=False, allow_null=True, default=None)

    class Meta:
        model = Auction
        fields = (
            'id',
            'name',
            'company',
            'auction_type',
            'pricing_method',
            'opening_date',
            'closing_date',
            'closed_auction',
            'category_type',
            'overtime_count',
            'overtime_duration',
            'supporting_document',
            'excel_template',
            'is_open',
            'created_by'
        )
        read_only_fields = ('id', )
    
    def create(self, validated_data):

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            validated_data['is_open'] = validate_date(validated_data['opening_date'], validated_data['closing_date'])
            instance = ModelClass._default_manager.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

class AuctionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = (
            'id',
            'name',
            'company',
            'auction_type',
            'opening_date',
            'closing_date',
            'closed_auction',
            'category_type',
            'overtime_count',
            'overtime_duration',
            'is_open',
            'created_by',
            'items',
            'has_bidding_activity'
        )
        read_only_fields = ('id', )

class AuctionItemListSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField('get_currency')
    class Meta:
        model = AuctionItems
        fields = (
            'id',
            'name',
            'description',
            'short_description',
            'reserve_price',
            'currency',
            'minimum_price',
            'minimum_increment',
            'minimum_decrement',
            'best_bid_price',
            'has_bidding_activity',
            'best_bidder'
        )

    def get_currency(self, obj):
        if obj.currency:
            return f'{obj.currency.initials}'
        else:
            return ''

class AuctionRetrieveSerializer(serializers.ModelSerializer):
    auction_items = AuctionItemListSerializer(many=True)
    created_by = serializers.SerializerMethodField('get_created_by')
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    excel_template = serializers.SerializerMethodField()
    supporting_document = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = (
            'id',
            'name',
            'company',
            'auction_type',
            'opening_date',
            'closing_date',
            'closed_auction',
            'category_type',
            'overtime_count',
            'excel_template',
            'supporting_document',
            'overtime_duration',
            'is_open',
            'created_by',
            'created_at',
            'auction_items'
        )
        read_only_fields = ('id', )
    
    def get_created_by(self, obj):
        if obj:
            return f'{obj.created_by.username}'
        else:
            return ''
    
    def get_opening_date(self, obj):
        return obj.opening_date.strftime("%Y-%m-%dT%H:%M")

    def get_closing_date(self, obj):
        return obj.closing_date.strftime("%Y-%m-%dT%H:%M")

    def get_excel_template(self, obj):
        if obj.excel_template:
            return obj.excel_response_url
        else:
            return None

    def get_supporting_document(self, obj):
        if obj.supporting_document:
            return obj.supporting_document_response_url
        else:
            return None

class AuctionItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuctionItems
        fields = (
            'id',
            'name',
            'auction',
            'description',
            'short_description',
            'reserve_price',
            'minimum_price',
            'minimum_increment',
            'minimum_decrement',
            'main_image'
        )
        read_only_fields = ('id', )

        def create(self, validated_data):

            ModelClass = self.Meta.model

            # Remove many-to-many relationships from validated_data.
            # They are not valid arguments to the default `.create()` method,
            # as they require that the instance has already been saved.
            info = model_meta.get_field_info(ModelClass)
            many_to_many = {}
            for field_name, relation_info in info.relations.items():
                if relation_info.to_many and (field_name in validated_data):
                    many_to_many[field_name] = validated_data.pop(field_name)

            try:
                validated_data.pop('auction')
                auc = Auction.objects.get(id=self.kwargs['auction_id'])
                validated_data['auction'] = auc
                instance = ModelClass._default_manager.create(**validated_data)
            except TypeError:
                tb = traceback.format_exc()
                msg = (
                    'Got a `TypeError` when calling `%s.%s.create()`. '
                    'This may be because you have a writable field on the '
                    'serializer class that is not a valid argument to '
                    '`%s.%s.create()`. You may need to make the field '
                    'read-only, or override the %s.create() method to handle '
                    'this correctly.\nOriginal exception was:\n %s' %
                    (
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        self.__class__.__name__,
                        tb
                    )
                )
                raise TypeError(msg)

            # Save many-to-many relationships after the instance is created.
            if many_to_many:
                for field_name, value in many_to_many.items():
                    field = getattr(instance, field_name)
                    field.set(value)

            return instance

class AuctionItemResponsesTrackingSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()

    class Meta:
        model = AuctionItemResponsesTracking
        fields = (
            'supplier',
            'bid',
            'created_at',
            'auction_item_response'
        )

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%dT%H:%M")
    
    def get_supplier(self, obj):
        if obj.auction_item_response:
            return f'{obj.auction_item_response.supplier_name}'
        else:
            return ''

class AuctionItemResponsesSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    auction_item_response_tracking = AuctionItemResponsesTrackingSerializer(many=True)

    class Meta:
        model = AuctionItemResponses
        fields = (
            'supplier',
            'bid_price',
            'rank',
            'created_at',
            'auction_item_response_tracking'
        )

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%dT%H:%M")
    
    def get_supplier(self, obj):
        if obj.supplier:
            return f'{obj.supplier_name}'
        else:
            return ''

class AuctionItemRetrieveSerializer(serializers.ModelSerializer):
    main_image = serializers.FileField()
    currency = serializers.SerializerMethodField('get_currency')
    auction_item_responses = AuctionItemResponsesSerializer(many=True)

    class Meta:
        model = AuctionItems
        fields = (
            'id',
            'name',
            'description',
            'short_description',
            'reserve_price',
            'currency',
            'minimum_price',
            'minimum_increment',
            'minimum_decrement',
            'best_bid_price',
            'created_by',
            'created_by_email',
            'main_image',
            'item_opening_time',
            'item_closing_time',
            'item_status',
            'auction_item_responses'
        )
    
    def get_currency(self, obj):
        if obj.currency:
            return f'{obj.currency.initials}'
        else:
            return ''


class SupplierAuctionListSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField('get_company_name')
    created_by = serializers.SerializerMethodField('get_created_by')
    class Meta:
        model =  Auction
        fields = (
            'id',
            'name',
            'company',
            'auction_type',
            'opening_date',
            'closing_date',
            'closed_auction',
            'category_type',
            'overtime_count',
            'overtime_duration',
            'is_open',
            'created_by',
            'created_at',
            'items'
        )
        read_only_fields = ('id', )
    
    def get_created_by(self, obj):
        if obj:
            return f'{obj.created_by.username}'
        else:
            return ''
    
    def get_company_name(self, obj):
        if obj:
            return f'{obj.company.company_name}'
        else:
            return ''

class AuctionItemImagesSerializer(serializers.Serializer):
    image = serializers.FileField()
    thumbnail = serializers.FileField()
    class Meta:
        model = AuctionItemImage
        fields = (
            'id',
            'item',
            'image',
            'thumbnail'
        )
        read_only_fields = ('id', 'thumbnail')


class SupplierAuctionItemSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField('get_currency')
    main_image = serializers.SerializerMethodField('get_main_image')
    auction_item_images = AuctionItemImagesSerializer(many=True)
    class Meta:
        model = AuctionItems
        fields = (
            'id',
            'name',
            'description',
            'short_description',
            'reserve_price',
            'currency',
            'quantity',
            'minimum_price',
            'minimum_increment',
            'minimum_decrement',
            'best_bid_price',
            'main_image',
            'auction_item_images'
        )

    def get_currency(self, obj):
        if obj.currency:
            return f'{obj.currency.initials}'
        else:
            return ''
    
    def get_main_image(self, obj):
        request = self.context.get('request')
        if obj.main_image == '':
            return None
        main_image_url = obj.main_image.url
        return request.build_absolute_uri(main_image_url)

class SupplierAuctionRetrieveSerializer(serializers.ModelSerializer):
    auction_items = SupplierAuctionItemSerializer(many=True)
    created_by = serializers.SerializerMethodField('get_created_by')
    company = serializers.SerializerMethodField('get_company_name')
    class Meta:
        model = Auction
        fields = (
            'id',
            'company',
            'name',
            'auction_type',
            'pricing_method',
            'opening_date',
            'closing_date',
            'closed_auction',
            'category_type',
            'overtime_count',
            'overtime_duration',
            'is_open',
            'created_by',
            'created_at',
            'auction_items'
        )
    
    def get_created_by(self, obj):
        if obj:
            return f'{obj.created_by.username}'
        else:
            return ''
    
    def get_company_name(self, obj):
        if obj:
            return f'{obj.company.company_name}'
        else:
            return ''

class AuctionItemConsumerSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField('get_currency')
    class Meta:
        model = AuctionItems
        fields = (
            'id',
            'name'
            'description'
            'short_description',
            'reserve_price',
            'currency',
            'minimum_price',
            'minimum_increment',
            'minimum_decrement',
            'best_bid_price'
        )
    
    def get_currency(self, obj):
        if obj:
            return f'{obj.currency.initials}'
        else:
            return ''

class AuctionInviteeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionInvitee 
        fields = (
            'id',
            'auction',
            'supplier' 
        )
        read_only_fields = ('id', )

class AuctionInviteeConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionInvitee
        fields = (
            'id',
            'auction',
            'supplier'
        )
        read_only_fields = ('id', )

class AuctionSupplierConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ['unsubscribe', 'password_date']

class AuctionConsumerSerializer(serializers.ModelSerializer):
    # invitee_auction = AuctionInviteeConsumerSerializer(many=True)
    class Meta:
        model = Auction
        fields = (
            'id',
            'name',
            'auction_type',
            'opening_date',
            'closing_date',
            'overtime_count',
            'overtime_counter',
            'status_open',
            'is_open',
            'invite_only'
        )
        read_only_fields = ('id', )

class AuctionItemConsumerSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField('get_currency')
    class Meta:
        model = AuctionItems
        fields = (
            'id',
            'name',
            'description',
            'short_description',
            'reserve_price',
            'currency',
            'quantity',
            'minimum_price',
            'minimum_increment',
            'minimum_decrement',
            'best_bid_price'
        )

    def get_currency(self, obj):
        if obj.currency:
            return f'{obj.currency.initials}'
        else:
            return ''

class AuctionItemResponsesTrackingConsumerSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    class Meta:
        model = AuctionItemResponsesTracking
        fields = (
            'supplier',
            'bid',
            'created_at',
            'auction_item_response',
        )

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%dT%H:%M")
    
    def get_supplier(self, obj):
        if obj.auction_item_response:
            return f'{obj.auction_item_response.supplier_name}'
        else:
            return ''

class SupplierAuctionBid(serializers.ModelSerializer):
    class Meta:
        model = AuctionItemResponses
        fields = (
            'id',
            'auction_item',
            'supplier',
            'bid_price'
        )
        read_only_fields = ('id', )

class AuctionAdvancedSupplierResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionTotalItemResponse
        fields = ["id", "supplier", "auction", "excel_url"]

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "company_name", "contact_name", "phone_number"]

class AuctionItemsExcelSerializer(serializers.Serializer):
    excel_file = serializers.FileField()

    def validate(self, attrs):
        print('Validating')
        print(attrs)
        try:
            auction_template = attrs["excel_file"]
            # validate that auction template end with xlsx
            if len(auction_template) < 3:
                raise serializers.ValidationError("The file field cannot be empty", 401)

        except Exception as e:
            raise serializers.ValidationError(
                "The uploaded file must saved in the .xlsx format", 401
            )

        return super().validate(attrs)