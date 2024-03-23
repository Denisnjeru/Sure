from django.contrib import admin
from .models import (
 Auction, AuctionItems, AuctionItemImage, AuctionInvitee, AuctionItemResponses, AuctionTotalItemResponse,
 AuctionItemResponsesTracking
)

class AuctionItemsInline(admin.TabularInline):
    model = AuctionItems
    fk_name = "auction"
    extra = 1

class AuctionInviteesInline(admin.TabularInline):
    model = AuctionInvitee
    fk_name = "auction"
    extra = 1

class AuctionTotalItemResponseInline(admin.TabularInline):
    model = AuctionTotalItemResponse
    fk_name = "auction"
    extra = 1

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "auction_type",
        "opening_date",
        "closing_date",
        "closed_auction"
    ]

    list_filter = [
        "auction_type",
        "category_type__name",
        "pricing_method"
    ]

    search_fields = [
        "auction_type",
        "category_type__name",
        "pricing_method"
    ]

    inlines = [AuctionItemsInline, AuctionInviteesInline, AuctionTotalItemResponseInline, ]


class AuctionItemImageInline(admin.TabularInline):
    model = AuctionItemImage
    fk_name = "item"
    extra = 1

class AuctionItemResponsesInline(admin.TabularInline):
    model = AuctionItemResponses
    fk_name = "auction_item"
    extra = 1

class AuctionItemResponsesTrackingInline(admin.TabularInline):
    model = AuctionItemResponsesTracking
    fk_name = "auction_item_response"
    extra = 1

@admin.register(AuctionItems)
class AuctionItemsAdmin(admin.ModelAdmin):
    list_display = [
        "auction",
        "name",
        "description",
        "short_description",
        "reserve_price",
        "minimum_price",
        "minimum_increment",
        "minimum_decrement",
        "best_bid_price"
    ]

    list_filter = [
        "auction__name",
        "name",
        "reserve_price"
    ]

    search_fields = [
        "auction__name",
        "name",
        "reserve_price"
    ]

    inlines = [AuctionItemImageInline, AuctionItemResponsesInline]


@admin.register(AuctionItemResponses)
class AuctionItemsAdmin(admin.ModelAdmin):
    list_display = [
        "auction_item",
        "supplier",
        "bid_price"
    ]

    list_filter = [
        "auction_item",
        "supplier",
        "bid_price"
    ]

    search_fields = [
        "auction_item",
        "supplier",
        "bid_price"
    ]

    inlines = [AuctionItemResponsesTrackingInline,]

@admin.register(AuctionItemImage)
class AuctionItemImageAdmin(admin.ModelAdmin):
    list_display = [
        "item",
        "image",
        "thumbnail"
    ]

    list_filter = [
        "item",
    ]

    search_fields = [
        "item",
        "image"
    ]