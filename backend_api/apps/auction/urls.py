from django.urls import path, include
from rest_framework.routers import DefaultRouter

from  . import views

app_name = "auction"
router = DefaultRouter()

router.register(r'', views.AuctionView, basename='AuctionView')
router.register(r'items/(?P<auction_id>\d+)', views.AuctionItemView, basename='AuctionItemsView')
router.register(r'supplier/list_retrieve', views.AuctionSupplierView, basename='AuctionSupplierView')
router.register(r'supplier/submit/advanced_auction/(?P<supplier_id>\d+)/(?P<auction_id>\d+)', 
    views.SupplierAdvancedAuctionView, basename='AuctionSupplierAdvancedView')

urlpatterns = [
    path('', include(router.urls)),
]