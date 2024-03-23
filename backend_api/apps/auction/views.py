import datetime
from django import apps
from django.core.files import File
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework import viewsets, status, mixins, filters
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework_datatables import pagination as dt_pagination
from django_filters.rest_framework import DjangoFilterBackend
from  rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser, FileUploadParser
from rest_framework.response import Response
from .models import (
    Auction, AuctionItemImage, AuctionItems, AuctionInvitee, AuctionItemResponses, AuctionItemResponsesTracking, AuctionTotalItemResponse

)
from .serializers import (
    AuctionCreateSerializer, AuctionListSerializer, AuctionRetrieveSerializer, AuctionItemCreateSerializer, AuctionItemRetrieveSerializer,SupplierAuctionListSerializer,
    SupplierAuctionRetrieveSerializer, AuctionAdvancedSupplierResponseSerializer, ParticipantSerializer, AuctionOpenSerializer, AuctionItemsExcelSerializer, AuctionItemImagesSerializer
)
from celery.result import AsyncResult
from .emails import (
    send_participation_acknowledgment,
    send_bid_responses,
)
from .tasks import (
    download_auction_bids_import, 
    submit_auction, 
    invite_suppliers_auction,
    import_auction_items,
    download_auction_items_template_import
)
from .utils import (
    convertfiletobase64, 
    convertbase64tofile,
    NullStringToNone,
    ValidateIfInMemoryUploadedFile
)
from apps.common.utils import timezone_aware_time

from apps.auction import serializers

def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404

class AuctionView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser,FileUploadParser,)
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter,)
    pagination_class = dt_pagination.DatatablesLimitOffsetPagination

    search_fields = ['auction_type',]
    filter_fields = ['auction_type',]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AuctionListSerializer
        if self.action == 'retrieve':
            return AuctionRetrieveSerializer
        else:
            return AuctionCreateSerializer

    def get_queryset(self):
        return Auction.objects.filter(company_id=self.request.auth['company_id'])

    def create(self, request, *args, **kwargs):

        data = request.data.copy()

        #Add created_by and Company_id
        data['created_by'] = request.user.id
        data['company'] = request.auth.payload['company_id']

        print(data)
        print(dir(request))

        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, *args, **kwargs):
        NullStringToNone(request)
        print(request.data)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(
        methods=["get"],
        detail=False,
        url_path="download/auction_bids/template/(?P<auction_id>\d+)",
    )
    def download_auction_bids_template(self, request, auction_id, *args, **kwargs):
        auction = Auction.objects.filter(id=auction_id).first()
        if auction is not None:
            file_download = download_auction_bids_import.delay(
                auction_id=auction.id,
                auction_type=auction.auction_type
            )
            file_context = {"task_id": file_download.task_id}
            res = AsyncResult(file_context["task_id"])
            task_result = res.get()
            if task_result["result"] == "success":
                context = {
                    "response_message": task_result["response_message"],
                    "filepath": task_result["filepath"],
                    "task_id": file_context["task_id"],
                }
                return Response(context, status=status.HTTP_200_OK)
            elif task_result["result"] == "error":
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["get"],
        detail=False,
        url_path="download/auction_items/template/(?P<auction_id>\d+)",
    )
    def download_auction_items_template(self, request, auction_id, *args, **kwargs):
        auction = Auction.objects.filter(id=auction_id).first()
        if auction is not None:
            print('Auction Items Template Import')
            file_download = download_auction_items_template_import.delay(
                auction_id=auction.id,
                auction_type=auction.auction_type
            )
            file_context = {"task_id": file_download.task_id}
            res = AsyncResult(file_context["task_id"])
            task_result = res.get()
            if task_result["result"] == "success":
                context = {
                    "response_message": task_result["response_message"],
                    "filepath": task_result["filepath"],
                    "task_id": file_context["task_id"],
                }
                return Response(context, status=status.HTTP_200_OK)
            elif task_result["result"] == "error":
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False, url_path="participants/(?P<auction_id>\d+)")
    def participants(self, request, category_id, **kwargs):
        suppliers = []
        responses = AuctionItemResponses.objects.filter(auction_item__auction_id=self.id).values_list(
            "supplier_id", flat=True
        )
        if responses.count() == 0:
            for response in responses:
                supplier = response.supplier
                if supplier not in suppliers:
                    suppliers.append(supplier)
            partcipants = set(suppliers)
        else:
            partcipants = apps.get_model("suppliers", "Supplier").objects.filter(id__in=responses.only("supplier_id").values("supplier_id"))

        response_serializer = ParticipantSerializer(partcipants, many=True)
        return Response(response_serializer.data)

    @action(
        methods=["post"], detail=False, url_path="invite_suppliers/(?P<auction_id>\d+)"
    )
    def invite_suppliers(self, request, auction_id, *args, **kwargs):
        data = request.data
        supplier_emails = data["emails"].split(",")

        for supplier_email in supplier_emails:
            try:
                if (
                    AuctionInvitee.objects.filter(
                        auction_id=auction_id, email=supplier_email
                    ).count()
                    < 1
                ):
                    supplier = (
                        apps.get_model("suppliers", "Supplier")
                        .objects.filter(email=supplier_email.replace(" ", ""))
                        .first()
                    )

                    if supplier is not None:
                        AuctionInvitee.objects.update_or_create(
                            auction_id=auction_id,
                            supplier=supplier,
                            email=supplier_email,
                        )
                    else:
                        AuctionInvitee.objects.update_or_create(
                            auction_id=auction_id,
                            email=supplier_email,
                        )
            except Exception as e:
                error = {"error": str(e)}


        invite_suppliers_auction(auction_id)

        context = {"response_message": "Suppliers invite emails sent successfully"}
        return Response(context, status=status.HTTP_201_CREATED)
    
    @action(
        methods=["get"], detail=False, url_path="close/(?P<auction_id>\d+)"
    )
    def close_auction(self, request, auction_id):
        auction = Auction.objects.filter(id=auction_id).first()

        if auction is not None:
            if auction.status_open:
                try:
                    auction.status_open = False
                    auction.closing_date = timezone_aware_time()
                    auction.save()
                    if auction.participants["count"] > 0:
                        send_bid_responses.delay(auction_id)

                    # generate auction report
                    # remember run asynchronously
                    context = {"message": "Auction closed successfuly"}
                    return Response(context, status=status.HTTP_201_CREATED)
                except Exception as e:
                    context = {"message": str(e)}
                    return Response(context, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                context = {"message": "Auction already closed"}
                return Response(context, status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["post"], detail=False, url_path="open/(?P<auction_id>\d+)"
    )
    def open_auction(self, request, auction_id):
        data_copy = request.data.copy()
        data_copy["id"] = auction_id
        serializer = AuctionOpenSerializer(data=data_copy)

        auction = Auction.objects.filter(id=data_copy["id"]).first()

        if auction is not None:
            if serializer.is_valid():
                serializer.save()
                context = {
                    "message": "Auction opened successfully",
                    "data": serializer.data,
                }
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context = {"message": "Invalid data"}
                return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {"message": "Auction is open"}
            return Response(context, status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['post'], detail=False, url_path='upload/auction/items/(?P<auction_id>\d+)')
    def upload_auction_items(self, request, auction_id):
        instance = Auction.objects.filter(
            company_id=self.request.auth.payload['company_id'], id=auction_id
        ).first()
        serializer = AuctionItemsExcelSerializer(data=request.data)
        if serializer.is_valid():
            print('validated successfully')
            file_object =  request.FILES["excel_file"]
            base64_str = convertfiletobase64(file_object)
            file_upload = import_auction_items.delay(auction_id, instance.auction_type, base64_str)

            file_context = {"task_id": file_upload.task_id}
            res = AsyncResult(file_context["task_id"])
            task_result = res.get()
            if task_result["result"] == "success":
                context = {
                    'task_id': file_context["task_id"],
                    "response_message": task_result["response_message"],
                }
                return Response(context, status=status.HTTP_200_OK)
            elif task_result["result"] == "error":
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            context = {
                "response_message": "Error uploading template"
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuctionItemView(viewsets.ModelViewSet):
    
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    days = 14

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuctionItemRetrieveSerializer
        if self.action == 'update_item_images':
            return AuctionItemImagesSerializer
        return AuctionItemCreateSerializer
    
    def get_queryset(self):
        return AuctionItems.objects.filter(auction_id = self.kwargs['auction_id'])

    def create(self, request, *args, **kwargs):

        data = request.data.copy()

        #Add created_by and Company_id and Auction Id
        data['auction'] = kwargs['auction_id'] # is valid throws error if auction_id is empty
        data['created_by'] = request.user.id
        
        # Update item images
        self.update_item_images(request, data['images'])
        data.pop('images')

        print(data)
        print(dir(request))

        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        NullStringToNone(request)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        today = make_aware(datetime.datetime.today())
        dateslist = [(today - datetime.timedelta(days = day)).date() for day in reversed(range(self.days))]
        start_date = today - datetime.timedelta(self.days)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        response_data['dateslist'] = dateslist
        response_data['count'] = 10
        print(response_data)
        return Response(response_data)
    
    def update_item_images(self, request, images, *args, **kwargs):
        print(type(images))
        
        try:
            serializer = self.get_serializer(data=images)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return None
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return error


class AuctionSupplierView(viewsets.ModelViewSet):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter,)
    search_fields = ['auction_type',]
    filter_fields = ['auction_type',]

    def get_serializer_class(self):
        if self.action == 'list':
            return SupplierAuctionListSerializer
        if self.action == 'retrieve':
            return SupplierAuctionRetrieveSerializer
        else:
            return SupplierAuctionListSerializer

    def get_invites(self):
        return AuctionInvitee.objects.filter(supplier_id=self.request.auth['user_id'])
    
    def invited_auctions(self):
        invited_auctions = []
        for invite in self.get_invites():
            invited_auctions.append(invite.auction.id)
        
        return invited_auctions

    def get_queryset(self):
        auctions = Auction.objects.all()
        for auction in  auctions:
            if auction.invite_only:
                if not auction.id in  self.invited_auctions():
                    auctions.exclude(id=auction.id)
        
        return auctions

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class SupplierAdvancedAuctionView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,FormParser,FileUploadParser,)

    def get_serializer_class(self):
        return AuctionAdvancedSupplierResponseSerializer
    
    def get_queryset(self):
        supplier_auction_responses = AuctionTotalItemResponse.objects.filter(
            auction_id=self.kwargs["auction_id"],
            supplier_id=self.kwargs["supplier_id"],
        )
        return supplier_auction_responses

    def create(self, request, *args, **kwargs):
        supplier_id = kwargs["supplier_id"]
        auction_id = kwargs["auction_id"]
        price_template = request.FILES["excel_url"]
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        supplier = apps.get_model("suppliers", "Supplier").objects.filter(id=supplier_id).first()
        auction = Auction.objects.filter(id=auction_id).first()

       
        if supplier is not None and auction is not None:
            sup_response,created = AuctionTotalItemResponse.objects.update_or_create(
                supplier_id=supplier_id, auction_id=auction_id,defaults={"excel_url":price_template}
            )
            if sup_response:
                suplier_res = submit_auction.delay(sup_response.auction_id, sup_response.supplier_id, sup_response.document_url.url)
                s_context = {"task_id": suplier_res.task_id}
                res = AsyncResult(s_context["task_id"])
                task_result = res.get()
                if task_result["result"]== "success":
                    if created:
                        send_participation_acknowledgment.delay(
                            supplier_id=supplier, auction_id=auction, created=True
                        )
                    else:
                        send_participation_acknowledgment.delay(
                            supplier_id=supplier, auction_id=auction
                        )
                    context = {
                        "response_message": task_result["response_message"],
                        "task_id": s_context["task_id"],
                    }
                    return Response(context, status=status.HTTP_200_OK)
                elif task_result["result"] == "error":
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)